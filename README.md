# 🗣️ Multi-LLM Group Chat Discussion

> What happens when 5 different AI models discuss the same topic?

Simulate a **human-like group chat discussion** using **5 independent Large Language Models** to analyze any topic, question, or document. Each LLM has a distinct thinking style, creating diverse perspectives that surface insights no single model would find alone.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![LLMs](https://img.shields.io/badge/LLMs-5%20Models-purple.svg)

## ✨ What It Does

Think of it as **five friends with different thinking styles discussing something in a group chat**:

- 🧠 **Logical Thinker** - Structured, fact-focused, breaks things down
- 🎨 **Creative Thinker** - Imaginative, speculative, alternative viewpoints  
- 🤔 **Skeptical Thinker** - Questions assumptions, plays devil's advocate
- 🔧 **Practical Thinker** - Real-world feasibility, cost, risks
- ⚖️ **Synthesizer** - Observes and bridges different viewpoints

## 🎯 Use Cases

- Exploring complex decisions from multiple angles
- Stress-testing ideas before presenting them
- Finding blind spots in your thinking
- Research and analysis with built-in devil's advocate
- Brainstorming with diverse AI perspectives

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/JeetInTech/Multi-LLM-Discussion.git
cd Multi-LLM-Discussion
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key (free)
# Get one at: https://console.groq.com/keys
```

### 4. Install Ollama (for local models)

Download from [ollama.com](https://ollama.com/download), then:

```bash
ollama pull llama3.2
ollama pull mistral
ollama pull phi3
```

### 5. Run a discussion

```bash
python main.py "Should AI be regulated?"
```

## 🔧 Configuration

The system uses **5 different models** for true diversity:

| Persona | Provider | Model |
|---------|----------|-------|
| 🧠 Logical | Ollama (local) | `llama3.2` |
| 🤔 Skeptical | Ollama (local) | `mistral` |
| ⚖️ Synthesizer | Ollama (local) | `phi3` |
| 🎨 Creative | Groq (cloud) | `llama-3.3-70b-versatile` |
| 🔧 Practical | Groq (cloud) | `qwen/qwen3-32b` |

### All Free LLM Options

| Provider | Cost | Setup |
|----------|------|-------|
| **Ollama** | 100% Free | Runs locally on your GPU |
| **Groq** | Free tier | [Get API key](https://console.groq.com/keys) |
| **Google Gemini** | Free tier | [Get API key](https://makersuite.google.com/app/apikey) |
| **HuggingFace** | Free tier | [Get API key](https://huggingface.co/settings/tokens) |

## 📁 Project Structure

```
Multi-LLM-Discussion/
├── main.py           # CLI entry point
├── discussion.py     # Core discussion engine
├── personas.py       # 5 persona definitions
├── llm_clients.py    # API clients (Ollama, Groq, etc.)
├── config.py         # Configuration settings
├── demo_offline.py   # Demo without API keys
├── .env.example      # Template for API keys
├── requirements.txt  # Python dependencies
└── README.md
```

## 💻 Command Line Options

```bash
python main.py [topic] [options]

Options:
  --file, -f FILE    Read topic from a file
  --rounds, -r N     Number of discussion rounds (default: 3)
  --no-synth         Disable the Neutral Synthesizer
```

## 📋 Example Output

```
[User]
Should remote work become the default?

─── Round 1 ───

[🧠 Logical Thinker]
Let's look at the data. Studies show remote workers are often 
more productive, with less commute stress...

[🎨 Creative Thinker]
What if the office isn't about work at all? Maybe it's about 
spontaneous collisions of ideas...

[🤔 Skeptical Thinker]
But those productivity studies mostly come from self-reporting. 
How do we actually measure creativity remotely?...

[🔧 Practical Thinker]
The real question is: can you maintain culture and onboard 
new people effectively?...
```

## 🔒 Safety Design

This is **NOT an autonomous agent framework**. It's a conversation simulator.

- ❌ No tool usage
- ❌ No memory persistence  
- ❌ No self-reflection loops
- ❌ No planning or execution
- ✅ Each LLM responds only to visible chat history
- ✅ Pure text generation simulation

## 🤝 Contributing

Contributions welcome! Ideas:
- Additional personas
- New LLM providers
- Export formats (Markdown, HTML, JSON)
- Web interface

## 📄 License

MIT License - Free to use for any purpose. See [LICENSE](LICENSE) file.

## 👤 Author

**JeetInTech** - [GitHub](https://github.com/JeetInTech)

---

⭐ Star this repo if you find it useful!