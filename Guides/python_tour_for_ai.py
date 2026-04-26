# -*- coding: utf-8 -*-
"""
================================================================================
  PYTHON FOR AI AGENTS — Quick Guide for C/Java Developers
================================================================================
  PART 1: Python concepts you NEED for building AI agents with CrewAI
  PART 2: CrewAI framework — Agent, Task, Crew explained + working examples

  This file complements python_tour.py (basic syntax).
  Here we focus ONLY on what matters for your first AI agent.
================================================================================
"""

# ═══════════════════════════════════════════════════════════════════
# PART 1 — PYTHON TOOLS YOU NEED FOR AI AGENT DEVELOPMENT
# ═══════════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────────────────────────
# 1. pip — Python's Package Manager (like Maven/npm)
# ─────────────────────────────────────────────────────────────────
# In C/Java you manually download libraries or use Maven/Gradle.
# In Python, you use pip from the terminal:
#
#   pip install crewai            ← install a package
#   pip install crewai[tools]     ← install with optional extras
#   pip install ollama            ← install ollama client
#   pip list                      ← see installed packages
#   pip freeze > requirements.txt ← save dependencies to file
#   pip install -r requirements.txt ← install from file
#
# VIRTUAL ENVIRONMENTS (isolate project dependencies):
#   python -m venv myenv          ← create virtual env
#   myenv\Scripts\activate        ← activate on Windows
#   source myenv/bin/activate     ← activate on Mac/Linux
#   deactivate                    ← leave the virtual env


# ─────────────────────────────────────────────────────────────────
# 2. Environment Variables & .env Files
# ─────────────────────────────────────────────────────────────────
# AI agents need API keys. NEVER hardcode them in your code!
# Use environment variables instead.

import os

def demo_env_variables():
    """Show how to work with environment variables."""
    print("\n" + "═"*60)
    print("  ENV VARIABLES & API KEYS")
    print("═"*60)

    # ── Reading env variables (built-in) ──────────────────────
    # Set in terminal:  set OPENAI_API_KEY=sk-xxx  (Windows)
    #                   export OPENAI_API_KEY=sk-xxx (Linux/Mac)
    api_key = os.environ.get("OPENAI_API_KEY", "not-set")
    print(f"  OPENAI_API_KEY = {api_key[:10]}..." if len(api_key) > 10 else f"  OPENAI_API_KEY = {api_key}")

    # ── Using python-dotenv (pip install python-dotenv) ───────
    # Create a .env file in your project root:
    #   OPENAI_API_KEY=sk-your-key-here
    #   SERPER_API_KEY=your-serper-key
    #
    # Then in Python:
    #   from dotenv import load_dotenv
    #   load_dotenv()  # loads .env into os.environ
    #   key = os.environ.get("OPENAI_API_KEY")
    print("  TIP: Use .env file + python-dotenv for API keys")
    print("  TIP: Add .env to .gitignore so keys stay private!")


# ─────────────────────────────────────────────────────────────────
# 3. Pydantic — Data Validation (used heavily by CrewAI)
# ─────────────────────────────────────────────────────────────────
# Pydantic = like Java's data classes + validation combined.
# CrewAI uses Pydantic models everywhere. You MUST understand this.

def demo_pydantic():
    """Show Pydantic basics — the backbone of CrewAI's data layer."""
    print("\n" + "═"*60)
    print("  PYDANTIC — Structured Data with Validation")
    print("═"*60)

    from pydantic import BaseModel, Field
    from typing import List, Optional

    # ── Define a model (like a Java class with validation) ────
    # C/Java: public class AgentConfig { String role; int maxIter; }
    # Python + Pydantic:
    class AgentConfig(BaseModel):
        role: str                              # required field
        goal: str                              # required field
        max_iter: int = 20                     # default value
        tools: List[str] = []                  # default empty list
        backstory: Optional[str] = None        # optional (can be None)
        verbose: bool = Field(default=False, description="Enable logging")

    # ── Create instances ──────────────────────────────────────
    config = AgentConfig(
        role="Researcher",
        goal="Find latest AI news"
    )
    print(f"  Config: {config}")
    print(f"  Role: {config.role}")
    print(f"  Max iter: {config.max_iter}")  # uses default

    # ── Validation happens automatically ──────────────────────
    try:
        bad = AgentConfig(role=123, goal="test")  # role should be str
        print(f"  (Pydantic coerced int to str: {bad.role})")
    except Exception as e:
        print(f"  Validation error: {e}")

    # ── Convert to dict / JSON ────────────────────────────────
    print(f"  As dict: {config.model_dump()}")
    print(f"  As JSON: {config.model_dump_json()}")

    # WHY THIS MATTERS FOR CREWAI:
    # - Agent, Task, Crew are all Pydantic models
    # - You can define output_pydantic on Tasks to get structured output
    # - Flow state uses Pydantic BaseModel
    print("\n  → CrewAI's Agent, Task, Crew all inherit from BaseModel")


# ─────────────────────────────────────────────────────────────────
# 4. Type Hints & typing module (used in CrewAI signatures)
# ─────────────────────────────────────────────────────────────────

def demo_type_hints():
    """Type hints you'll see in CrewAI code."""
    print("\n" + "═"*60)
    print("  TYPE HINTS (what you'll see in CrewAI)")
    print("═"*60)

    from typing import List, Dict, Optional, Union, Any

    # ── Basic type hints (Python 3.5+) ────────────────────────
    # These are NOT enforced at runtime — they're documentation
    # Java: String name = "Ali";  →  Python: name: str = "Ali"

    name: str = "Ali"
    age: int = 21
    scores: List[int] = [85, 90, 78]
    config: Dict[str, Any] = {"key": "value", "count": 5}
    maybe_name: Optional[str] = None       # str or None
    id_val: Union[str, int] = "abc-123"    # str OR int

    # ── Function with type hints ──────────────────────────────
    def create_agent(role: str, goal: str, verbose: bool = False) -> dict:
        return {"role": role, "goal": goal, "verbose": verbose}

    result = create_agent("Writer", "Write articles")
    print(f"  create_agent result: {result}")

    # ── You'll see these patterns in CrewAI ───────────────────
    # def researcher(self) -> Agent:     ← returns Agent object
    # tools: List[BaseTool] = []         ← list of tool objects
    # llm: Optional[str] = None          ← optional string
    print("  → Type hints help you understand CrewAI's API")


# ─────────────────────────────────────────────────────────────────
# 5. Decorators Review — CrewAI uses them heavily
# ─────────────────────────────────────────────────────────────────

def demo_decorators_for_crewai():
    """Decorators you'll use in CrewAI."""
    print("\n" + "═"*60)
    print("  DECORATORS — Used by CrewAI (@agent, @task, @crew)")
    print("═"*60)

    # Quick recap: decorator = function that wraps another function
    # Java analogy: like @Override, @Autowired annotations

    # ── Simple decorator example ──────────────────────────────
    def register(func):
        """A decorator that registers a function."""
        print(f"  Registered: {func.__name__}")
        return func

    @register
    def my_agent():
        return "I'm an agent"

    # ── CrewAI uses decorators like this: ─────────────────────
    # @CrewBase          ← marks a class as a crew base
    # @agent             ← marks method as agent definition
    # @task              ← marks method as task definition
    # @crew              ← marks method as crew definition
    # @before_kickoff    ← runs before crew starts
    # @after_kickoff     ← runs after crew finishes
    #
    # Example:
    #   @agent
    #   def researcher(self) -> Agent:
    #       return Agent(config=self.agents_config['researcher'])
    print("  → @agent, @task, @crew tell CrewAI what each method does")


# ─────────────────────────────────────────────────────────────────
# 6. YAML Files — CrewAI Configuration
# ─────────────────────────────────────────────────────────────────

def demo_yaml():
    """YAML is how CrewAI configures agents and tasks."""
    print("\n" + "═"*60)
    print("  YAML — CrewAI's Config Language")
    print("═"*60)

    # YAML = human-readable data format (like JSON but cleaner)
    # CrewAI uses agents.yaml and tasks.yaml files

    yaml_example = """
    # agents.yaml example:
    researcher:
      role: >
        {topic} Senior Researcher
      goal: >
        Find cutting-edge info about {topic}
      backstory: >
        You're an expert researcher who finds the best info.

    # tasks.yaml example:
    research_task:
      description: >
        Research {topic} thoroughly.
      expected_output: >
        A markdown report with key findings.
      agent: researcher
      output_file: report.md
    """
    print(yaml_example)

    # ── YAML syntax basics ────────────────────────────────────
    # key: value           ← like JSON {"key": "value"}
    # key: >               ← multi-line string (folded)
    # items:               ← start a list
    #   - item1
    #   - item2
    # {topic}              ← placeholder, replaced at runtime
    #
    # NOTE: Indentation matters (like Python itself)!
    print("  → {topic} gets replaced when you call crew.kickoff(inputs={'topic': 'AI'})")


# ═══════════════════════════════════════════════════════════════════
# PART 2 — CREWAI FRAMEWORK: BUILD YOUR FIRST AI AGENT
# ═══════════════════════════════════════════════════════════════════
# CrewAI has 3 core building blocks:
#   1. Agent  — WHO does the work (the AI worker)
#   2. Task   — WHAT needs to be done (the job description)
#   3. Crew   — The TEAM that coordinates agents + tasks


def explain_crewai_concepts():
    """Explain the 3 pillars of CrewAI with analogies."""
    print("\n" + "═"*60)
    print("  CREWAI — THE 3 BUILDING BLOCKS")
    print("═"*60)

    print("""
  Think of it like a COMPANY:
  ┌──────────────────────────────────────────────────┐
  │  CREW = The Company / Team                       │
  │  ┌────────────────────────────────────────────┐  │
  │  │  AGENT 1: Researcher                       │  │
  │  │  - role: "Senior Researcher"               │  │
  │  │  - goal: "Find the best information"       │  │
  │  │  - tools: [SearchTool, WebScraper]         │  │
  │  └────────────────────────────────────────────┘  │
  │  ┌────────────────────────────────────────────┐  │
  │  │  AGENT 2: Writer                           │  │
  │  │  - role: "Content Writer"                  │  │
  │  │  - goal: "Write clear, engaging articles"  │  │
  │  │  - tools: []                               │  │
  │  └────────────────────────────────────────────┘  │
  │                                                  │
  │  TASK 1: "Research AI trends" → assigned to Researcher  │
  │  TASK 2: "Write article"     → assigned to Writer      │
  │                                                  │
  │  Process: Sequential (Task1 → Task2)             │
  └──────────────────────────────────────────────────┘

  FLOW:
  1. You define Agents (who they are, what they can do)
  2. You define Tasks (what needs to be done)
  3. You put them in a Crew
  4. You call crew.kickoff() → agents work on tasks → you get results
    """)


# ─────────────────────────────────────────────────────────────────
# 7. AGENT — The AI Worker
# ─────────────────────────────────────────────────────────────────

def explain_agent():
    """What is an Agent and how to create one."""
    print("\n" + "═"*60)
    print("  AGENT — The AI Worker")
    print("═"*60)

    print("""
  An Agent = an AI persona with a specific role, goal, and personality.

  REQUIRED parameters:
    role      → Job title (e.g., "Senior Researcher")
    goal      → What the agent tries to achieve
    backstory → Personality / context (shapes how it thinks)

  OPTIONAL but useful:
    llm       → Which AI model to use (default: gpt-4)
    tools     → List of tools the agent can use
    verbose   → Print detailed logs (True/False)
    memory    → Remember past interactions (True/False)

  ─── CODE EXAMPLE ─────────────────────────────────────────
  from crewai import Agent

  researcher = Agent(
      role="Senior Data Researcher",
      goal="Find the latest developments in AI",
      backstory="You're a seasoned researcher who finds "
                "the most relevant information.",
      verbose=True,
      llm="gpt-4"   # or "ollama/gemma3" for local models
  )
  ──────────────────────────────────────────────────────────

  USING LOCAL MODELS (Ollama):
    llm="ollama/gemma3"       ← use Gemma 3 locally
    llm="ollama/llama3"       ← use Llama 3 locally
    llm="ollama/mistral"      ← use Mistral locally

  USING CLOUD MODELS:
    llm="gpt-4"               ← OpenAI (needs OPENAI_API_KEY)
    llm="gpt-4o-mini"         ← cheaper OpenAI option
    """)


# ─────────────────────────────────────────────────────────────────
# 8. TASK — The Job Description
# ─────────────────────────────────────────────────────────────────

def explain_task():
    """What is a Task and how to create one."""
    print("\n" + "═"*60)
    print("  TASK — The Job Description")
    print("═"*60)

    print("""
  A Task = a specific piece of work assigned to an Agent.

  REQUIRED parameters:
    description     → What needs to be done (detailed instructions)
    expected_output → What the result should look like
    agent           → Which agent handles this task

  OPTIONAL but useful:
    tools           → Extra tools for this specific task
    output_file     → Save result to a file
    context         → List of other tasks whose output feeds into this one

  ─── CODE EXAMPLE ─────────────────────────────────────────
  from crewai import Task

  research_task = Task(
      description="Research the latest trends in {topic}. "
                  "Find at least 5 key developments.",
      expected_output="A bullet-point list of 5 key trends "
                      "with brief explanations.",
      agent=researcher  # the Agent object from above
  )

  write_task = Task(
      description="Write a blog post based on the research.",
      expected_output="A 500-word blog post in markdown.",
      agent=writer,
      context=[research_task],  # uses output of research_task
      output_file="blog_post.md"
  )
  ──────────────────────────────────────────────────────────

  KEY CONCEPT — context:
    context=[task_a] means "give this task the output of task_a"
    This is how tasks CHAIN together!
    """)


# ─────────────────────────────────────────────────────────────────
# 9. CREW — The Team
# ─────────────────────────────────────────────────────────────────

def explain_crew():
    """What is a Crew and how to create one."""
    print("\n" + "═"*60)
    print("  CREW — The Team That Runs Everything")
    print("═"*60)

    print("""
  A Crew = a team of Agents working on Tasks together.

  REQUIRED parameters:
    agents  → List of Agent objects
    tasks   → List of Task objects

  OPTIONAL but useful:
    process → How tasks are executed:
              Process.sequential (one after another — default)
              Process.hierarchical (manager assigns tasks)
    verbose → Print execution details

  ─── CODE EXAMPLE ─────────────────────────────────────────
  from crewai import Crew, Process

  crew = Crew(
      agents=[researcher, writer],
      tasks=[research_task, write_task],
      process=Process.sequential,
      verbose=True
  )

  # RUN THE CREW!
  result = crew.kickoff(inputs={"topic": "AI Agents"})
  print(result.raw)  # the final output as text
  ──────────────────────────────────────────────────────────

  kickoff(inputs={...}):
    - inputs dict replaces {topic} placeholders in your tasks
    - Returns a CrewOutput object with .raw, .json_dict, etc.
    """)


# ─────────────────────────────────────────────────────────────────
# 10. COMPLETE WORKING EXAMPLE — Your First Agent
# ─────────────────────────────────────────────────────────────────

def complete_example_simple():
    """
    A complete, minimal CrewAI example you can run.
    Prerequisites: pip install crewai crewai[tools]
    """
    print("\n" + "═"*60)
    print("  COMPLETE EXAMPLE — Minimal Agent (copy & run!)")
    print("═"*60)

    code = '''
# ── file: my_first_agent.py ──────────────────────────────
# SETUP: pip install crewai
# RUN:   python my_first_agent.py

from crewai import Agent, Task, Crew, Process

# ── Step 1: Create an Agent ──────────────────────────────
researcher = Agent(
    role="AI Researcher",
    goal="Explain complex AI topics in simple terms",
    backstory="You are a senior AI researcher who excels "
              "at making complex topics accessible.",
    verbose=True,
    llm="ollama/gemma3"  # ← local model via Ollama
    # llm="gpt-4"        # ← or use OpenAI (needs API key)
)

# ── Step 2: Create a Task ────────────────────────────────
explain_task = Task(
    description="Explain what an AI Agent is and how it "
                "differs from a regular chatbot. "
                "Keep it under 200 words.",
    expected_output="A clear, beginner-friendly explanation "
                    "of AI agents vs chatbots.",
    agent=researcher
)

# ── Step 3: Create a Crew ────────────────────────────────
crew = Crew(
    agents=[researcher],
    tasks=[explain_task],
    process=Process.sequential,
    verbose=True
)

# ── Step 4: Run it! ──────────────────────────────────────
result = crew.kickoff()
print("\\n" + "="*50)
print("RESULT:")
print("="*50)
print(result.raw)
'''
    print(code)


# ─────────────────────────────────────────────────────────────────
# 11. MULTI-AGENT EXAMPLE — Two Agents Working Together
# ─────────────────────────────────────────────────────────────────

def complete_example_multi_agent():
    """A two-agent crew where one researches and one writes."""
    print("\n" + "═"*60)
    print("  MULTI-AGENT EXAMPLE — Researcher + Writer")
    print("═"*60)

    code = '''
# ── file: multi_agent_crew.py ────────────────────────────
from crewai import Agent, Task, Crew, Process

# ── Agent 1: The Researcher ──────────────────────────────
researcher = Agent(
    role="Senior Researcher",
    goal="Find the most important facts about a topic",
    backstory="Expert at finding and organizing information.",
    verbose=True,
    llm="ollama/gemma3"
)

# ── Agent 2: The Writer ──────────────────────────────────
writer = Agent(
    role="Content Writer",
    goal="Write clear, engaging content from research",
    backstory="Skilled writer who turns data into stories.",
    verbose=True,
    llm="ollama/gemma3"
)

# ── Task 1: Research ─────────────────────────────────────
research_task = Task(
    description="Research the topic: {topic}. "
                "Find 5 key facts or trends.",
    expected_output="A list of 5 bullet points with key facts.",
    agent=researcher
)

# ── Task 2: Write (uses research output) ─────────────────
write_task = Task(
    description="Write a short article about {topic} "
                "using the research provided.",
    expected_output="A 300-word article in markdown format.",
    agent=writer,
    context=[research_task],   # ← chains to research output!
    output_file="article.md"   # ← saves result to file
)

# ── Create and run the crew ──────────────────────────────
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI Agents in 2026"})
print(result.raw)
'''
    print(code)


# ─────────────────────────────────────────────────────────────────
# 12. TOOLS — Giving Agents Superpowers
# ─────────────────────────────────────────────────────────────────

def explain_tools():
    """How tools work in CrewAI."""
    print("\n" + "═"*60)
    print("  TOOLS — Give Agents Real-World Abilities")
    print("═"*60)

    print("""
  Without tools, agents can only think and write text.
  With tools, they can: search the web, read files, scrape sites, etc.

  INSTALL: pip install 'crewai[tools]'

  ─── BUILT-IN TOOLS ───────────────────────────────────────
  from crewai_tools import (
      SerperDevTool,      # Google search (needs SERPER_API_KEY)
      FileReadTool,       # Read files from disk
      FileWriterTool,     # Write files to disk
      WebsiteSearchTool,  # Search within a website
      PDFSearchTool,      # Search within PDF files
  )

  ─── USING A TOOL ─────────────────────────────────────────
  from crewai_tools import SerperDevTool

  search_tool = SerperDevTool()

  agent = Agent(
      role="Researcher",
      goal="Find information online",
      backstory="Expert web researcher",
      tools=[search_tool],    # ← give tool to agent
      verbose=True
  )

  ─── CUSTOM TOOL (create your own) ────────────────────────
  from crewai.tools import BaseTool

  class MyTool(BaseTool):
      name: str = "Calculator"
      description: str = "Performs basic math calculations"

      def _run(self, expression: str) -> str:
          return str(eval(expression))

  # Then: agent = Agent(..., tools=[MyTool()])
    """)


# ─────────────────────────────────────────────────────────────────
# 13. SETUP CHECKLIST — Everything You Need to Start
# ─────────────────────────────────────────────────────────────────

def setup_checklist():
    """Step-by-step setup for your first CrewAI project."""
    print("\n" + "═"*60)
    print("  SETUP CHECKLIST — Get Running in 5 Minutes")
    print("═"*60)

    print("""
  ┌─ STEP 1: Install Python 3.10+ ─────────────────────────
  │  python --version          # check your version
  └─────────────────────────────────────────────────────────

  ┌─ STEP 2: Create a virtual environment ──────────────────
  │  python -m venv agent_env
  │  agent_env\\Scripts\\activate     # Windows
  │  source agent_env/bin/activate   # Mac/Linux
  └─────────────────────────────────────────────────────────

  ┌─ STEP 3: Install CrewAI ────────────────────────────────
  │  pip install crewai 'crewai[tools]'
  └─────────────────────────────────────────────────────────

  ┌─ STEP 4: Choose your LLM ──────────────────────────────
  │
  │  OPTION A — Local with Ollama (FREE, no API key):
  │    1. Install Ollama: https://ollama.com
  │    2. Pull a model:   ollama pull gemma3
  │    3. In code:        llm="ollama/gemma3"
  │
  │  OPTION B — OpenAI (paid, needs API key):
  │    1. Get key: https://platform.openai.com/api-keys
  │    2. Set env: set OPENAI_API_KEY=sk-your-key
  │    3. In code: llm="gpt-4"
  └─────────────────────────────────────────────────────────

  ┌─ STEP 5: Create your first agent file ──────────────────
  │  Copy the "COMPLETE EXAMPLE" from section 10 above
  │  Save as: my_first_agent.py
  │  Run:     python my_first_agent.py
  └─────────────────────────────────────────────────────────
    """)


# ─────────────────────────────────────────────────────────────────
# 14. QUICK REFERENCE — CrewAI Cheat Sheet
# ─────────────────────────────────────────────────────────────────

def cheat_sheet():
    """Quick reference for CrewAI."""
    print("\n" + "═"*60)
    print("  CREWAI CHEAT SHEET")
    print("═"*60)

    print(f"""
  {"Concept":<20} {"What it is":<25} {"Java Analogy"}
  {"─"*20} {"─"*25} {"─"*25}
  {"Agent":<20} {"AI worker persona":<25} {"Worker thread / Service"}
  {"Task":<20} {"Job to complete":<25} {"Runnable / Callable"}
  {"Crew":<20} {"Team of agents":<25} {"ThreadPool / Orchestrator"}
  {"Tool":<20} {"Agent ability":<25} {"Utility class / API client"}
  {"Process":<20} {"Execution order":<25} {"Sequential / Parallel"}
  {"kickoff()":<20} {"Start the crew":<25} {"main() / run()"}
  {"Flow":<20} {"Multi-crew pipeline":<25} {"Pipeline / Workflow"}

  ─── IMPORTS YOU'LL ALWAYS USE ────────────────────────────
  from crewai import Agent, Task, Crew, Process

  ─── MINIMAL PATTERN ─────────────────────────────────────
  agent = Agent(role=..., goal=..., backstory=...)
  task  = Task(description=..., expected_output=..., agent=agent)
  crew  = Crew(agents=[agent], tasks=[task])
  result = crew.kickoff()
  print(result.raw)

  ─── COMMON MISTAKES ─────────────────────────────────────
  ✗ Forgetting to set API key env variable
  ✗ Not installing crewai[tools] for tools
  ✗ Using context=[task] before task is defined
  ✗ Forgetting expected_output (it's required!)
    """)


# ═══════════════════════════════════════════════════════════════════
# RUN ALL SECTIONS
# ═══════════════════════════════════════════════════════════════════

def run_all():
    """Run every section in sequence."""
    # Part 1: Python tools for AI
    demo_env_variables()
    demo_pydantic()
    demo_type_hints()
    demo_decorators_for_crewai()
    demo_yaml()

    # Part 2: CrewAI framework
    # explain_crewai_concepts()
    # explain_agent()
    # explain_task()
    # explain_crew()
    # complete_example_simple()
    # complete_example_multi_agent()
    # explain_tools()
    # setup_checklist()
    # cheat_sheet()

    print("\n✅  Guide complete! Now go build your first agent!")


if __name__ == "__main__":
    run_all()
