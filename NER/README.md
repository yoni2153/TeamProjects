# Named Entity Recognition (NER) Pipeline with Google Vertex AI & Firestore

This project provides a Python script (`ner.py`) to process an Excel file, extract named entities from text using Google Vertex AI's Gemini model, generate embeddings, and store the results in Google Firestore.

## Features

- Reads data from a specified Excel sheet
- Cleans and extracts IDs and text from each row
- Uses Vertex AI's Gemini model for Named Entity Recognition (NER)
- Generates text embeddings (requires implementation of `get_embeddings`)
- Stores results (entities, embeddings, and IDs) in a Firestore collection

## Requirements

- Python 3.11+
- Google Cloud account with Vertex AI and Firestore enabled
- Service account credentials with appropriate permissions
- Required Python packages:
  - `google-cloud-firestore`
  - `vertexai`
  - `pandas`
  - `openpyxl` (for Excel support)

## Setup

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies:**
   ```bash
   pip install google-cloud-firestore vertexai pandas openpyxl
   ```
3. **Set up Google Cloud credentials:**
   - Export your service account key:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
     ```
4. **Configure constants in `ner.py`:**

   - `PROJECT_ID`: Your GCP project ID
   - `LOCATION`: Vertex AI region (e.g., `us-central1`)
   - `FIRESTORE_COLLECTION`: Name of your Firestore collection
   - `MODEL`: Vertex AI model name (e.g., `gemini-2-flash`)

5. **Implement the `get_embeddings` function** in `ner.py` to generate embeddings for your text. (This is left as a placeholder for you to fill in.)

## Usage

Run the script with your Excel file and sheet name:

```bash
python ner.py
```

By default, the script processes `path_to_your_excel_file.xlsx` and `Sheet1`. Update these values in the `if __name__ == "__main__":` block or modify as needed.

## Notes

- The script expects column 'B' to contain the ID and column 'J' to contain the text for NER.
- Only rows with valid integer IDs and non-empty text are processed.
- The Firestore document key is the stringified embedding vector.
- The script skips rows where NER output is not valid JSON.
