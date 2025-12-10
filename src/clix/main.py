# App lives here 

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from pathlib import Path
from dotenv import load_dotenv
import json # Need this to persist chat history in .json files is required by user
import typer # For the CLI

# Rich - Markdown language and colors
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.table import Table

# LiteLLM - One lib to access any llm 
from litellm import completion

load_dotenv()


# Initliazining app
app = typer.Typer()
console = Console()

# MACROS
CHAT_HISTORY = Path.home() / ".clix_chat_history.json"
MODEL_NAME = "groq/llama-3.1-8b-instant"  # Using this for now, later implement customizability


# Helper functions
def load_history():
    """ Loads chat history from the file if exists """  # Called Docstrings, easy to find function function
    if CHAT_HISTORY.exists():
        try:
            with open(CHAT_HISTORY , "r") as file:
                return json.load(file) # Returns the chat history
        except json.JSONDecodeError:
            return []

    return []


def save_history(messages):
    """Saves the current session to disk for persistence"""
    with open(CHAT_HISTORY, "w") as file:
        json.dump(messages , file)


def delete_history():
    """Deletes the chat history"""
    if CHAT_HISTORY.exists():
        os.remove(CHAT_HISTORY)


######################
# THE MAIN CHAT LOOP #
#######################

@app.command()
def chat(
    model: str = typer.Option(MODEL_NAME, "--model", "-m", help="Model to use"),
):
    # Check for API Key
    if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        console.print("[bold red]Error:[/bold red] No API Key found in .env file.")
        raise typer.Exit()

    # Load history
    messages = load_history()
    if messages:
        console.print("[dim green]↻ Resuming previous session...[/dim green]")
        console.print("[bold green] Session Restored! [/bold green]")
    
    console.print("[bold cyan]Clix Online.[/bold cyan]")

    
    
    while True:
        try:

            user_input = console.input("[bold green]You > [/bold green]")
            
            # If "/exit" , session history isn't saved -> Chat gets deleted
            if user_input.strip() == "/exit":
                delete_history()
                console.print("[bold red]Session deleted. Peace![/bold red]")
                break
            
            # if "/exit-v" , session history is saved -> Chat is stored
            if user_input.strip() == "/exit-v":
                save_history(messages)
                console.print("[bold green]Session saved. Peace![/bold green]")
                break


            # Saving each chat
            messages.append({"role": "user", "content": user_input})


            response_text = ""
            # console.print("[bold blue]Clix > [/bold blue]", end="")
            
            # We use a Live display to handle the streaming Markdown
            with Live(Markdown(""), refresh_per_second=10, console=console) as live:
                response = completion(
                    model=model,
                    messages=messages,
                    stream=True
                )
                
                for chunk in response:
                    content = chunk.choices[0].delta.content or ""
                    response_text += content

                    # Table grid for better printin
                    grid = Table.grid(padding=(0, 1)) 
                    grid.add_column()  # Col1 : Clix > 
                    grid.add_column()  # Col2 : Streaming markdown
                    
                    # Add the row with both pieces of content
                    grid.add_row(
                        "[bold blue]Clix >[/bold blue]", 
                        Markdown(response_text)
                    )
                    
                    # Update the screen with the whole grid
                    live.update(grid)
            

            # Append response to history
            messages.append({"role": "assistant", "content": response_text})
            console.print() # Add a newline for spacing

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[yellow]Exiting without saving...[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()