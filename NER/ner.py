import os
import re
import json
import pandas as pd
from dotenv import load_dotenv

from google.cloud import firestore
from vertexai.preview.language_models import TextGenerationModel
import vertexai

load_dotenv()  # Load environment variables from .env file

# Constants – configure these for your GCP project
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your_project_id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "indictments")
MODEL = os.getenv("VERTEX_AI_MODEL", "gemini-1.5-flash-001")
# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Assume this function is defined elsewhere and returns a List[float]
# def get_embeddings(text: str) -> List[float]:
#     here you would implement the logic to get embeddings for the text


def process_excel_and_store(file_path: str, sheet_name: str):
    # Initialize Firestore client
    db = firestore.Client(project=PROJECT_ID)

    # Load the pre-trained Gemini model
    ner_model = TextGenerationModel.from_pretrained(MODEL)

    # Read the specified sheet into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    for _, row in df.iterrows():
        # --- 1) Clean and convert column B to integer ---
        raw_id = row.get('B')  # or use row.iloc[1] if no header
        id_str = str(raw_id) if raw_id is not None else ""
        digits = re.sub(r'\D', "", id_str)
        if not digits:
            continue
        try:
            indictment_id = int(digits)
        except ValueError:
            continue

        # --- 2) Extract text from column J ---
        text = row.get('J')  # or row.iloc[9]
        if not isinstance(text, str) or not text.strip():
            continue

        # --- 3) Call Gemini (Vertex AI) for NER ---
        prompt = (
            "Extract all named entities from the following text. "
            "Return a JSON object whose keys are entity types (e.g. Person, Organization, Location, etc.) "
            "and whose values are the entity text. DO NOT include any other text in the response.\n\n"
            f"Text:\n\"\"\"\n{text}\n\"\"\"\n"
        )
        response = ner_model.predict(prompt=prompt)
        try:
            entities = json.loads(response.text)
        except json.JSONDecodeError:
            # skip rows we can't parse
            continue

        # --- 4) Get embedding vector ---
        embedding = get_embeddings(text)  # List[float]

        # --- 5) Build Firestore document ---
        # Use the embedding (stringified) as the document key
        doc_key = str(embedding)
        doc_data = {
            "embedding": embedding,
            "entities": {
                **entities,
                "indictment": indictment_id
            }
        }

        # --- 6) Store in Firestore ---
        db.collection(FIRESTORE_COLLECTION).document(doc_key).set(doc_data)

    print("Done processing and storing all valid rows.")


if __name__ == "__main__":
    # Example usage
    try:
        process_excel_and_store("example.xlsx", "Sheet1")
    except Exception as e:
        print(f"An error occurred: {e}")
