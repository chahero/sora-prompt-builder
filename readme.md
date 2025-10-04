# Sora2 Script Builder 🎬

## About This Project

**Sora2 Script Builder** is a web application designed to help you easily create detailed JSON scripts (prompts) for AI video generation models like OpenAI's Sora. Users no longer need to write complex JSON structures by hand; instead, they can use an intuitive UI to transform their ideas into well-organized video scripts.

This app supports a workflow where users leverage their own LLMs (like ChatGPT or Gemini) to generate an initial script draft, which can then be imported into the app for detailed editing and management.

---

## 🚀 Live Demo

This application is deployed via Streamlit Community Cloud and is available for everyone to use for free.

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

**Access here: https://sora-prompt-builder.streamlit.app/**

---

## Features

- **🤖 Prompt Generator for LLMs:**
    - By inputting a few conditions like video topic, duration, and style, the app generates an **optimized instructional prompt** that ChatGPT or Gemini can best understand.
- **📋 Script Importer & Parser:**
    - When you paste a JSON-formatted script from an LLM, the app **automatically parses the content and converts it into an editable UI**.
    - It includes a **robust parsing function** to intelligently handle minor differences in key names or data formats.
- **🧠 Template Support:**
    - Provides **templates** for common script structures like 'Product Ads' or 'Film Trailers' to help you get started with a single click.
- **✍️ Intuitive Script Editor:**
    - Systematically manage the video's basic information and the detailed content of each scene.
    - Allows for the **dynamic addition, modification, and deletion** of scenes.
    - A clean layout with Tabs and Columns helps you understand complex scripts at a glance.
- **📥 Export to JSON:**
    - The completed script can be downloaded as a `.json` file, ready to be used with Sora 2.

---

## Installation & Usage

This project is built with Python and the Streamlit library.

### Prerequisites

- Python 3.8+

### Installation

1. **Clone the project:**
    
    ```bash
    git clone [<https://github.com/your-username/sora-prompt-builder.git>](<https://github.com/your-username/sora-prompt-builder.git>)
    cd sora-prompt-builder
    
    ```
    
2. **Create and activate a virtual environment:**
    
    ```bash
    # Windows
    python -m venv .venv
    .venv\\Scripts\\activate
    
    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    
    ```
    
3. **Install the required libraries:**
    
    ```bash
    pip install streamlit
    
    ```
    

### Running the App

1. From within the project folder, enter the following command in your terminal:
    
    ```bash
    streamlit run app.py
    
    ```
    
2. This command will automatically open a new tab in your web browser where the application is running.

---

## Workflow

1. **[Tab 1] Generate Prompt:** Enter your video idea in the 'Generate LLM Prompt' tab and copy the generated instructional prompt.
2. **[ChatGPT / Gemini] Create Script Draft:** Ask your preferred AI chatbot to generate a JSON script draft using the copied prompt.
3. **[Tab 2] Import and Edit Script:** Paste the JSON result from the AI into the 'Edit Script' tab and click the 'Apply' button.
4. **[Tab 2] Modify Content:** Use the UI editor to freely modify the script details as needed.
5. **[Tab 3] Review and Download:** Review the final script and download it as a `.json` file.

---

## Contributing

Contributions to this project are always welcome. For bug reports or feature suggestions, please open an issue on GitHub. To contribute code, please fork the repository and submit a pull request.