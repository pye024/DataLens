
# DataLens!🔎

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-ff69b4.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-blueviolet.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.3.0-success.svg)](https://plotly.com/)
[![Google Generative AI](https://img.shields.io/badge/Google%20Generative%20AI-1.38.0-orange.svg)](https://ai.google.dev/)

DataLens is a smart tool that helps you quickly understand your data. Just upload a CSV file, and DataLens will automatically create charts, summaries, and dashboards to show you what's inside. It's like having a data expert who does all the hard work for you!

**Disclaimer:** This tool is intended to aid data analysis or serve as a starting point, especially for non-technical users. It does not replace the need for a thorough and nuanced data analysis by a qualified professional.

## Features

- **Easy CSV Upload**: Just drag and drop your data file.
- **Automatic Dashboards**: Get instant charts and graphs.
- **Smart Insights**: Understand key trends and numbers at a glance.
- **Error Fixing**: If something goes wrong, DataLens can try to fix it for you.
- **Code Preview**: See the Python code that powers your dashboard.

## Demo

Here's a quick look at how DataLens works:

![DataLens Demo](assets/demo_video.mp4)

## Installation

To get started with DataLens, you'll need to have Python installed. Then, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pye024/DataLens
   cd DataLens
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Gemini API Key:**
   - Go to [Google AI for Developers](https://aistudio.google.com/app/apikey) and create an API key.
   - Create a `.env` file in the project root and add your key like this:
     ```
     GEMINI_API_KEY="YOUR_API_KEY"
     ```

## Usage

Once you've installed everything, you can run the app:

```bash
streamlit run app.py
```

This will open DataLens in your web browser. From there, you can upload your CSV file and start exploring!

## Run with Docker

Alternatively, you can run DataLens using Docker:

1. **Build the Docker image:**
   ```bash
   docker build -t datalens .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -p 8501:8501 -e GEMINI_API_KEY="YOUR_API_KEY" datalens
   ```

   Make sure to replace `"YOUR_API_KEY"` with your actual Gemini API key.

   This will start the app on `http://localhost:8501`.

## Example Dashboard

Here's an example of a dashboard created with DataLens using the World Happiness Report 2024 dataset:

| Dashboard | Code Preview |
|---|---|
| ![Example Dashboard](assets/example_code.png) | ![Example Code Preview](assets/example_code_preview.png) |

This dashboard shows key metrics like the average happiness score, the happiest and least happy countries, and how different factors like GDP and life expectancy relate to happiness.
