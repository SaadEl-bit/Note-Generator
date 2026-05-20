# Agents-Project — AI Note Structuring Agent

## Overview

Agents-Project is an AI-powered note structuring tool that transforms messy, unstructured text notes into professionally formatted Word documents (`.docx`). It uses the Groq API (powered by Llama models) to intelligently parse, classify, and reorganize raw notes into clean, structured documents with proper headings, lists, tables, and formatting.

## What It Does

The system takes raw `.txt` files containing messy notes and automatically:

1. **Classifies** the note type (meeting, idea, todo, Q&A, or default/research)
2. **Extracts** structured data using AI (Groq API)
3. **Validates** the extracted data against required fields
4. **Renders** a formatted `.docx` document with appropriate styling

## Architecture

### Pipeline Flow

```
Raw Note (.txt) → Classifier → Template Selection → API Call → JSON Parsing → Validation → Renderer → Output (.docx)
```

### Core Components

#### 1. Entry Point (`main.py`)
- Scans the `notes/` directory for `.txt` files
- Orchestrates the full processing pipeline for each note
- Outputs `.docx` files to the `output/` directory

#### 2. Classifier (`src/classifier/`)
Two-stage classification system:

- **Heuristic Classifier** (`heuristic.py`): Rule-based keyword matching with confidence scoring. Zero API cost, instant results. Supports English and French keywords.
- **API Classifier** (`api_classifier.py`): AI-powered fallback when heuristic confidence is low (< 0.3). Uses Groq API to intelligently determine note type.

Supported note types:
| Type | Description |
|------|-------------|
| `meeting` | Meeting notes with attendees, agenda, decisions |
| `idea` | Brainstorming, proposals, concepts |
| `todo` | Task lists with priorities and deadlines |
| `qa` | Questions and answers |
| `default` | Research notes, study material, mixed content |

#### 3. API Layer (`src/apis/`)
- **Groq API** (`groq.py`): Integrates with Groq's `llama-3.1-8b-instant` model
  - System prompt enforces JSON-only output
  - Built-in retry logic with exponential backoff for network errors
  - Configurable temperature (0.2) and max tokens (4096)

#### 4. Template System (`templates/`)
JSON-based templates define:
- The prompt sent to the AI (with `{raw_note}` placeholder)
- Required fields for validation

Available templates:
| Template | Purpose |
|----------|---------|
| `meeting.json` | Meeting notes structure |
| `idea.json` | Idea/proposal structure |
| `todo.json` | Task list structure |
| `qa.json` | Q&A document structure |
| `default.json` | Academic/research notes structure |
| `question_only.json` | Single question structure |

#### 5. Extractors (`src/extractors/`)
- **Prompt Builder** (`prompt_builder.py`): Loads templates and injects raw notes into prompts. Returns the complete prompt string and list of required fields.

#### 6. Validators (`src/validator.py`)
- Sanitizes API responses
- Ensures all required fields exist
- Fills missing values with appropriate defaults (empty lists, "N/A", null)
- Converts non-list values to lists where expected

#### 7. Renderers (`src/renderers/`)
Convert structured JSON data into formatted `.docx` files:

| Renderer | Features |
|----------|----------|
| `meeting.py` | Title, date, participants, agenda, decisions (green), action items (with owner/due date), summary, tags |
| `idea.py` | Title, problem statement, solution (blue/bold), impact, resources, next steps (green), tags |
| `todo.py` | Title, categories, task table with 4 columns (Task, Priority, Due Date, Status), color-coded priority and status |
| `qa.py` | Title, confidence badge (color-coded), question (blue/bold), answer, sources, follow-up questions, tags |
| `default.py` | Title, subject, summary (italic/gray), sections with content/key points/examples, key definitions, Q&A, takeaways, study actions, tags |

All renderers share common utilities from `base.py` (title, meta lines, headings, bullet/numbered lists).

## Project Structure

```
my_agent/
├── main.py                    # Entry point — processes all notes
├── requirements.txt           # Python dependencies
├── .env                       # API keys (GROQ_API_KEY)
├── .gitignore
│
├── notes/                     # Input: raw .txt notes go here
│   └── *.txt
│
├── output/                    # Output: formatted .docx files appear here
│   └── *_<type>.docx
│
├── templates/                 # JSON templates for each note type
│   ├── meeting.json
│   ├── idea.json
│   ├── todo.json
│   ├── qa.json
│   ├── default.json
│   └── question_only.json
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Environment config, loads .env
│   ├── validator.py           # Response validation & sanitization
│   │
│   ├── apis/
│   │   ├── __init__.py
│   │   ├── base.py            # Shared exceptions (TokenLimitError)
│   │   └── groq.py            # Groq API client with retry logic
│   │
│   ├── classifier/
│   │   ├── __init__.py
│   │   ├── heuristic.py       # Rule-based keyword classifier
│   │   └── api_classifier.py  # AI-powered fallback classifier
│   │
│   ├── extractors/
│   │   ├── __init__.py
│   │   └── prompt_builder.py  # Template loading & prompt construction
│   │
│   └── renderers/
│       ├── __init__.py
│       ├── base.py            # Shared docx utilities
│       ├── meeting.py         # Meeting note renderer
│       ├── idea.py            # Idea renderer
│       ├── todo.py            # Todo list renderer (with table)
│       ├── qa.py              # Q&A renderer
│       └── default.py         # Default/research note renderer
│
└── tests/
    ├── test_apis.py           # API connection tests
    ├── test_multple_api.py    # Multiple API tests
    ├── test_classifier.py     # Classifier tests
    └── test_extractors.py     # Extractor tests
```

## Setup & Installation

### Prerequisites
- Python 3.13+
- Groq API key (free at [console.groq.com](https://console.groq.com/))

### Step 1: Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure API Key
Create a `.env` file in the `my_agent/` directory:
```
GROQ_API_KEY=gsk_your_key_here
```

### Step 4: Verify Setup
```powershell
python tests/test_apis.py
```
Expected output: `GROQ API: SUCCESS`

## Usage

### Processing Notes

1. Place your raw `.txt` notes in the `notes/` folder
2. Run the agent:
   ```powershell
   python main.py
   ```
3. Find formatted `.docx` files in the `output/` folder

### Example Input (`notes/meeting_notes.txt`)
```
Meeting with team on Monday
John, Sarah, Mike attended
Discussed new feature launch
Decided to push to prod next week
Sarah needs to update docs by Friday
Mike will handle deployment
```

### Example Output (`output/meeting_notes_meeting.docx`)
A formatted Word document with:
- **Title**: Feature Launch Meeting
- **Date**: Monday
- **Participants**: John, Sarah, Mike
- **Agenda**: New feature launch
- **Decisions Made**: Push to production next week
- **Action Items**:
  1. Update docs — Assigned to: Sarah — Due: Friday
  2. Handle deployment — Assigned to: Mike — Due: —
- **Summary**: ...
- **Tags**: ...

## Key Features

- **Multi-language support**: Keywords in English and French
- **Two-stage classification**: Fast heuristic first, AI fallback only when needed
- **Template-driven**: Easy to add new note types by creating a JSON template + renderer
- **Retry logic**: Automatic retry with exponential backoff for API failures
- **Validation**: Ensures data integrity before rendering
- **Rich formatting**: Color-coded elements, tables, headings, bullet lists
- **Batch processing**: Processes all notes in the `notes/` folder in one run

## Dependencies

| Package | Purpose |
|---------|---------|
| `groq` | Groq API client |
| `python-docx` | Word document generation |
| `python-dotenv` | Environment variable management |
| `lxml` | XML parsing (required by python-docx) |
| `google-genai` | Google AI (reserved for future use) |

## Extending the Project

### Adding a New Note Type

1. Create `templates/newtype.json` with prompt and required fields
2. Create `src/renderers/newtype.py` with a `render_newtype(data, output_path)` function
3. Register the renderer in `main.py`:
   ```python
   from src.renderers.newtype import render_newtype
   RENDERERS["newtype"] = render_newtype
   ```
4. Add the type to `KEYWORDS` in `src/classifier/heuristic.py`
5. Add the type to `CLASSIFIER_PROMPT` in `src/classifier/api_classifier.py`

## Current Status

- **Phase 1**: Core pipeline working (classify → extract → render)
- **Classifier**: Currently forced to `default` for testing (see commented code in `heuristic.py` and `api_classifier.py`)
- **Supported types**: meeting, idea, todo, qa, default
- **API**: Groq (Llama 3.1 8B)
- **Output format**: `.docx` only

## Future Enhancements (Potential)

- Multi-API support (Gemini, OpenAI, etc.)
- PDF output format
- Web UI / CLI interface
- Note merging and cross-referencing
- Custom template editor
- Export to other formats (Markdown, HTML, Notion)
