
# AI Code Review CLI

An intelligent CLI tool that reviews Git patch files using LLMs like GPT-4. It performs **staged analysis** to classify code areas (UI, API, Backend, etc.), run **targeted category-based reviews**, and output concise, structured feedback (including file, line number, and issue summary).

---

## Overview

This tool helps software engineers reduce code review fatigue by automating initial PR feedback. It works in three review stages:

1. **Scope Classification** – Categorizes the patch (e.g., UI, Backend, Security).
2. **Targeted Review** – Performs checklist-based analysis per category.
3. **Optional Deep Dive** – Deeper analysis for Security, Performance, and Edge Cases.

The output is clean JSON containing only actionable improvements with file path, line number, and short descriptions.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gunjanmodi/ai-code-reviewer.git
cd ai-code-reviewer
````

### 2. Set Up Environment

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
OPENAI_API_KEY=sk-...
```

---

## How to Use

### 🔸 Review a Patch File

```bash
python cli.py path/to/your.patch
```

This will:

* Classify the patch context (UI, Backend, etc.)
* Perform focused code review using pre-defined category checklists
* Print a JSON output with issues found

### Sample Output

```json
[
  {
    "file_path": "src/components/Button.tsx",
    "line_number": 42,
    "issue": "Hardcoded color used instead of design token."
  },
  {
    "file_path": "server/routes/user.ts",
    "line_number": 88,
    "issue": "Missing input validation for user creation route."
  }
]
```

---

## Future Roadmap
* Make the project as web application or chrome extension
* GitHub webhook integration
* Docker container and VS Code plugin
* Support for Anthropic Claude and Code Llama

---

## License
MIT License. See LICENSE file for details.

## 🙋‍♂️ Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to fork the repo and open PRs.