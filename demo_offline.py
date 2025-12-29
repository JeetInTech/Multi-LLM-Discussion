"""
Offline Demo - Multi-LLM Group Chat Discussion
===============================================

This demo shows the output format without requiring API keys.
It uses pre-generated responses to demonstrate the system.

Run: python demo_offline.py
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def run_demo():
    """Run an offline demonstration of the discussion format"""
    
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🗣️ Multi-LLM Group Chat Discussion[/bold cyan]\n"
        "[dim]DEMO MODE - Showing pre-generated example[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Example user input
    user_input = "Should companies adopt a 4-day work week?"
    
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
    
    # Pre-generated discussion
    transcript = [
        # Round 1
        ("🧠", "Logical Thinker", "blue", 1,
         "Let's break this down. The 4-day work week typically means 32 hours paid as 40, or 4x10-hour days. Studies from Microsoft Japan and Perpetual Guardian in New Zealand showed productivity increases of 20-40%. But we need to separate correlation from causation here."),
        
        ("🎨", "Creative Thinker", "magenta", 1,
         "What if we're thinking about this wrong? Maybe it's not about the number of days at all, but about giving people autonomy over their time. The best ideas I've ever had came when I wasn't 'at work'. That extra day could unlock so much creative potential."),
        
        ("🤔", "Skeptical Thinker", "yellow", 1,
         "Hold on though - those studies are mostly from knowledge work sectors. What about healthcare, retail, manufacturing? A hospital can't just close on Fridays. I think we're generalizing from a narrow set of industries."),
        
        ("🔧", "Practical Thinker", "green", 1,
         "That's a good point. Implementation is everything here. You'd need to think about customer coverage, shift scheduling, and whether clients in other countries are okay with you being unavailable 3 days a week. The logistics aren't trivial."),
        
        # Round 2
        ("🧠", "Logical Thinker", "blue", 2,
         "I think the Skeptic raises a valid concern. But maybe the question isn't 'should ALL companies' but rather 'which companies and roles.' Different contexts need different solutions. A blanket policy either way seems too simplistic."),
        
        ("🎨", "Creative Thinker", "magenta", 2,
         "Ooh I love that reframe! What if companies offered it as an option? Like, some people might prefer 5 shorter days for family reasons. The real innovation might be flexibility itself, not a specific schedule."),
        
        ("🤔", "Skeptical Thinker", "yellow", 2,
         "Flexibility sounds nice but creates coordination problems. If half your team works Monday-Thursday and half works Tuesday-Friday, when do you meet? I've seen 'flexible' policies create more stress, not less."),
        
        ("🔧", "Practical Thinker", "green", 2,
         "We actually tried flexible Fridays at my old company. The key was having 3 'core days' where everyone overlapped. The other 2 were flexible. It worked, but it required really clear documentation and async communication skills."),
        
        # Round 3
        ("🧠", "Logical Thinker", "blue", 3,
         "So we're converging on: it depends on the industry, role, and implementation. The evidence suggests benefits in specific contexts, but universal adoption isn't feasible. That seems like a reasonable conclusion."),
        
        ("🎨", "Creative Thinker", "magenta", 3,
         "I still think the bigger shift is cultural. Whether it's 4 days or flexible hours, the underlying change is trusting employees to manage their output rather than their time. That's the real conversation we should be having."),
        
        ("🤔", "Skeptical Thinker", "yellow", 3,
         "Fair, but trust requires verification. How do you measure 'output' for a manager? Or a culture lead? Some jobs are inherently hard to quantify. I'm not saying don't try, just that it's harder than it sounds."),
        
        ("🔧", "Practical Thinker", "green", 3,
         "I'd recommend any company considering this start with a 3-month pilot in one department. Measure before/after carefully. That gives you real data instead of vibes, and it's reversible if it fails."),
        
        ("⚖️", "Neutral Synthesizer", "cyan", 3,
         "Interesting discussion. We've got strong support for the idea in principle, but legitimate concerns about universal applicability. The emerging consensus seems to be: context matters, pilots are wise, and flexibility might be the real goal behind the 4-day framing."),
    ]
    
    current_round = 0
    for emoji, name, color, round_num, content in transcript:
        if round_num != current_round:
            current_round = round_num
            console.print(f"[dim]─── Round {current_round} ───[/dim]")
            console.print()
        
        console.print(f"[bold {color}]{emoji} {name}[/bold {color}]")
        console.print(f"  {content}")
        console.print()
    
    # Section 2: Summary
    console.print(Panel.fit(
        "[bold]Section 2: Discussion Summary[/bold]",
        border_style="green"
    ))
    console.print()
    
    summary = """
**Key Points by Participant:**

• **Logical Thinker**: Cited productivity research, emphasized need for context-specific analysis, helped reframe from universal to selective adoption
• **Creative Thinker**: Focused on autonomy and trust as underlying values, suggested flexibility as the real innovation
• **Skeptical Thinker**: Raised industry applicability concerns, coordination challenges, and measurement difficulties
• **Practical Thinker**: Shared real-world implementation experience, recommended pilot approach with core overlap days

**Main Disagreements:**
- Universal vs. selective adoption
- Whether flexibility creates or reduces stress
- How to measure output in non-quantifiable roles

**Areas of Agreement:**
- Context and industry matter significantly
- Implementation details are crucial
- A pilot approach reduces risk
- The deeper issue may be trust and autonomy
"""
    console.print(Markdown(summary))
    console.print()
    
    # Section 3: Takeaway
    console.print(Panel.fit(
        "[bold]Section 3: Final Synthesized Takeaway[/bold]",
        border_style="yellow"
    ))
    console.print()
    
    takeaway = """
The 4-day work week is neither a universal solution nor a gimmick—it's a tool that works well in specific contexts. Evidence supports productivity benefits in knowledge-work settings, but service industries and roles requiring continuous coverage face genuine implementation challenges.

Rather than asking "should we do this?", companies might better ask "what problem are we solving?" If the goal is employee wellbeing and sustainable performance, a 4-day week is one path—but flexible scheduling, async-first culture, or results-based work policies might achieve similar outcomes with fewer coordination costs.

For organizations considering this change: start small with a reversible pilot, measure outcomes rigorously, and be honest about which roles can and cannot adapt. The companies that succeed will be those that treat this as an operational experiment rather than a cultural statement.
"""
    console.print(Markdown(takeaway))
    console.print()
    
    console.print("[dim]─── Demo Complete ───[/dim]")
    console.print()
    console.print("[bold]To run with real LLMs, configure your API key in config.py and run:[/bold]")
    console.print("  python main.py")
    console.print()

if __name__ == "__main__":
    run_demo()
