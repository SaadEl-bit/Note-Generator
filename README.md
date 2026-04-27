# Agents-Project

Creating our first crew of AI agents that can transfer your messy notes into structured document





# How does the project work ?

###### \## 1. Create Virtual Environment \& Install Libraries



powershell

\# Create virtual environment

python -m venv venv



\# Activate it

.\\\\venv\\\\Scripts\\\\Activate.ps1



\# Install all required packages

pip install -r requirements.txt





\-------------------------------------------



###### \## 2. Get Their Own Groq API Key



1\. Go to \[console.groq.com](https://console.groq.com/)

2\. Sign up with email or Google account

3\. Click \*\*API Keys\*\* in the left sidebar

4\. Click \*\*Create API Key\*\*

5\. Copy the key (starts with `gsk\_...`)



\-------------------------------------------



###### \## 3. Create `.env` File



1\. In the project root folder (`ai-note-agent/`), create a new file named exactly `.env`

2\. Paste their key inside:





GROQ\_API\_KEY=gsk\_their\_actual\_key\_here





1\. Save the file



\-------------------------------------------



###### \## 4. Verify Everything Works



Run the test script:

powershell

python test\_apis.py





Expected result:

GROQ API: SUCCESS

Response: Groq is working





\-------------------------------------------



###### \## 5. How the Agent Works (Current Phase 1)



| Step | Action | Location |

| ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |

| \*\*1. Put raw note\*\* | Create or paste a `.txt` file with messy meeting notes | `notes/` folder |

| \*\*2. Run the agent\*\* | `python main.py` | PowerShell, project root |

| \*\*3. Find output\*\* | Formatted `.docx` file appears | `output/` folder |

| \*\*4. Open result\*\* | Double-click the `.docx` file | Microsoft Word |



###### \## 6. Folder Structure 



ai-note-agent/

├── .env                  ← they create this (their API key)

├── .gitignore

├── main.py               ← entry point

├── requirements.txt

├── notes/                ← put raw .txt notes here

├── output/               ← .docx files appear here

├── src/

│   ├── apis/

│   │   └── groq.py

│   ├── extractors/

│   ├── renderers/

│   └── config.py

└── templates/

&#x20;   └── meeting.json





