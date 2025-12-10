# clix-cli

## Project Overview
`clix-cli` is a terminal-based AI companion built in Python. It provides an interactive chat interface in the console, leveraging `litellm` to communicate with various LLM providers (currently configured for Groq/Llama). It features rich text formatting, session persistence, and streaming responses.

## Tech Stack
*   **Language:** Python (>=3.10)
*   **CLI Framework:** `typer`
*   **LLM Abstraction:** `litellm`
*   **UI/Formatting:** `rich`
*   **Configuration:** `python-dotenv` (via `.env`)
*   **Build System:** `setuptools` (via `pyproject.toml`)

## Project Structure
*   **`src/clix/main.py`**: The core application logic. Contains the `typer` app definition, chat loop, history management (`load_history`, `save_history`), and streaming response handling.
*   **`pyproject.toml`**: Defines project metadata, dependencies, and the `clix` console script entry point.
*   **`test.py`**: A simple standalone script to verify LLM connectivity and API key configuration using `litellm`.
*   **`.env`**: Stores API keys (e.g., `GROQ_API_KEY`, `GEMINI_API_KEY`).
*   **`venv/`**: Python virtual environment.

## Usage & Commands

### Setup
1.  **Environment:** Ensure `GROQ_API_KEY` or `GEMINI_API_KEY` is set in your `.env` file.
2.  **Installation:**
    ```bash
    pip install .
    ```

### Running the App
Once installed, you can run the CLI using the command defined in `pyproject.toml`:
```bash
clix
```
Alternatively, for development:
```bash
python -m src.clix.main
```

### Chat Commands
Inside the chat interface:
*   **`/exit`**: Exits the application and **deletes** the session history.
*   **`/exit-v`**: Exits the application and **saves** the session history to `~/.clix_chat_history.json`.

## Development Conventions
*   **Dependencies:** Managed via `pyproject.toml`.
*   **Formatting:** The project uses `rich` for outputting Markdown and styled text to the console.
*   **State Management:** Chat history is stored locally in a JSON file in the user's home directory.
