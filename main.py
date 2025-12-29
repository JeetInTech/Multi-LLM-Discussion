"""
Multi-LLM Group Chat Discussion System
=======================================

Simulates a human-like group chat discussion using 4-5 LLM personas
to analyze a user-provided topic, question, or document.

Usage:
    python main.py                    # Interactive mode
    python main.py "Your topic here"  # Direct topic input
    python main.py --file input.txt   # Read topic from file
"""

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from discussion import Discussion, generate_summary, generate_takeaway
import config

console = Console()

def print_header():
    """Print application header"""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🗣️ Multi-LLM Group Chat Discussion[/bold cyan]\n"
        "[dim]Simulating a thoughtful conversation between different thinking styles[/dim]",
        border_style="cyan"
    ))
    console.print()

def print_message(emoji: str, name: str, content: str, round_num: int):
    """Print a single chat message"""
    style_map = {
        "Logical Thinker": "blue",
        "Creative Thinker": "magenta",
        "Skeptical Thinker": "yellow",
        "Practical Thinker": "green",
        "Neutral Synthesizer": "cyan"
    }
    color = style_map.get(name, "white")
    
    console.print(f"[bold {color}]{emoji} {name}[/bold {color}]")
    console.print(f"  {content}")
    console.print()

def get_user_input() -> str:
    """Get topic from user interactively"""
    console.print("[bold]Enter your topic, question, or paste a document:[/bold]")
    console.print("[dim](Press Enter twice when done)[/dim]")
    console.print()
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
    
    return "\n".join(lines).strip()

def run_discussion(user_input: str):
    """Run the full discussion and display results"""
    
    # Display user input
    console.print(Panel(
        user_input,
        title="[bold]📝 User Input[/bold]",
        border_style="white"
    ))
    console.print()
    
    # Section 1: Group Chat Transcript
    console.print(Panel.fit(
        "[bold]Section 1: Group Chat Transcript[/bold]",
        border_style="cyan"
    ))
    console.print()
    
    # Create and run discussion
    discussion = Discussion(user_input=user_input)
    
    current_round = 0
    for message in discussion.run_discussion():
        if message.round_num != current_round:
            current_round = message.round_num
            console.print(f"[dim]─── Round {current_round} ───[/dim]")
            console.print()
        
        print_message(
            message.emoji,
            message.persona_name,
            message.content,
            message.round_num
        )
    
    # Section 2: Discussion Summary
    console.print()
    console.print(Panel.fit(
        "[bold]Section 2: Discussion Summary[/bold]",
        border_style="green"
    ))
    console.print()
    
    with console.status("[bold green]Generating summary...[/bold green]"):
        summary = generate_summary(discussion)
    
    console.print(Markdown(summary))
    console.print()
    
    # Section 3: Final Takeaway
    console.print(Panel.fit(
        "[bold]Section 3: Final Synthesized Takeaway[/bold]",
        border_style="yellow"
    ))
    console.print()
    
    with console.status("[bold yellow]Generating final takeaway...[/bold yellow]"):
        takeaway = generate_takeaway(discussion)
    
    console.print(Markdown(takeaway))
    console.print()
    
    console.print("[dim]─── Discussion Complete ───[/dim]")

def main():
    parser = argparse.ArgumentParser(
        description="Multi-LLM Group Chat Discussion System"
    )
    parser.add_argument(
        "topic",
        nargs="?",
        help="Topic or question to discuss"
    )
    parser.add_argument(
        "--file", "-f",
        help="Read topic from a file"
    )
    parser.add_argument(
        "--rounds", "-r",
        type=int,
        default=config.MAX_ROUNDS,
        help=f"Number of discussion rounds (default: {config.MAX_ROUNDS})"
    )
    parser.add_argument(
        "--no-synth",
        action="store_true",
        help="Disable the Neutral Synthesizer participant"
    )
    
    args = parser.parse_args()
    
    # Override config if needed
    if args.rounds:
        config.MAX_ROUNDS = args.rounds
    if args.no_synth:
        config.ENABLE_SYNTHESIZER = False
    
    print_header()
    
    # Check configuration for free providers
    provider = config.LLM_PROVIDER
    
    if provider == "ollama":
        # Ollama doesn't need API key, just check if it's running
        console.print("[dim]Using Ollama (local, free). Make sure Ollama is running.[/dim]")
        console.print()
    elif provider in ("groq", "google", "huggingface"):
        api_key = {
            "groq": config.GROQ_API_KEY,
            "google": config.GOOGLE_API_KEY,
            "huggingface": config.HUGGINGFACE_API_KEY
        }.get(provider, "")
        
        if not api_key:
            console.print(f"[bold red]Error:[/bold red] No API key configured for {provider}")
            console.print(f"Please set your API key in [cyan]config.py[/cyan]")
            console.print()
            console.print("[bold]Free LLM Options:[/bold]")
            console.print("  • [green]ollama[/green] - 100% free, runs locally (recommended)")
            console.print("    Install: https://ollama.com/download")
            console.print("    Then run: ollama pull llama3.2")
            console.print()
            console.print("  • [blue]groq[/blue] - Free tier, fast cloud inference")
            console.print("    Get key: https://console.groq.com/keys")
            console.print()
            console.print("  • [yellow]google[/yellow] - Free tier (15 req/min)")
            console.print("    Get key: https://makersuite.google.com/app/apikey")
            console.print()
            console.print("  • [magenta]huggingface[/magenta] - Free inference API")
            console.print("    Get key: https://huggingface.co/settings/tokens")
            sys.exit(1)
    
    # Get user input
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            user_input = f.read().strip()
    elif args.topic:
        user_input = args.topic
    else:
        user_input = get_user_input()
    
    if not user_input:
        console.print("[bold red]Error:[/bold red] No topic provided")
        sys.exit(1)
    
    # Run the discussion
    try:
        run_discussion(user_input)
    except KeyboardInterrupt:
        console.print("\n[dim]Discussion interrupted[/dim]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise

if __name__ == "__main__":
    main()
