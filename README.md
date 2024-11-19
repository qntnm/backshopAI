# Technical Manual Assistant AI

Handy dandy tool to help repairmen in their daily work going through manuals, repairing components and filling out logs.

## Installation Instructions

1. Install [Ollama](https://ollama.com):
    - Download any model you want to work with.
    - This repo uses `llama3.2:1b`

2. Install all python dependencies in your environment.
    - local virtual environment instructions for Windows:

        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

    - `pip install -r requirements.txt`

## Usage

1. Launch backend:

    ```bash
    uvicorn backend:app --reload
    ```

2. Load the HTML into a browser tab
3. Launch Ollama
    a. The Ollama server can be launched in the background by clicking on the app.
    b. You can also launch the Ollama server by typing `Ollama serve` in a new terminal.
4. You can now use the app!

## Known Issues

1. The prompts need more working.
