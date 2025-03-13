# AI Home Design Generator

This project is a **Streamlit-based** application that generates **home design layouts** using **Google Gemini AI** and fetches design inspiration from **Lexica.art**.

## Available Scripts

In the project directory, you can run:

### `streamlit run app.py`

Runs the app in development mode.\
Open [http://localhost:8501](http://localhost:8501) to view it in your browser.

The app will automatically reload when you make changes.

### `pip install -r requirements.txt`

Installs all dependencies required for the project.

### `python app.py`

Runs the core backend logic manually (without Streamlit UI).

## API Configuration

To use the AI features, replace `YOUR_API_KEY_HERE` in `app.py`:

```python
api_key = "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)
