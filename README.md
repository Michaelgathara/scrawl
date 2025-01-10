# Scrawl AI Agent

## **Overview**
Scrawl AI Agents automate the process of researching trending technologies and generating example applications. It showcases the potential of AI-driven workflows for developers.

### **Key Features**
- **Research Agent**: Fetches trending technologies and AI models using APIs like GitHub, Dev.to, and Hacker News.
- **Example Builder Agent**: Generates example applications based on research results, providing reusable code snippets.
- **Database Integration**: Uses SQLite for storing research data and supports easy retrieval.
- **Testing Framework**: Implements unit and integration tests using `pytest` and `pytest-asyncio`.

---

### TODO:
- [ ] Enhance the research agent to acquire more data
- [ ] Clean example code 
- [ ] Example builder should output files
   - [ ] Example builder should automatically push examples to Github
- [ ] Testing - see [**Testing Framework**](#testing)
- [ ] Docker upgrades - get it to be robust for scale



## **Folder Structure**
```
.
├── agents
│   ├── example_builder.py       # Example builder agent
│   ├── research.py              # Research agent
│   └── __init__.py              # Package initialization
│
|── database
│   ├── db.py                    # SQLite database management
│   ├── research_data.db         # SQLite database file
│   └── __init__.py              # Package initialization
│
├── pydantic_ex
│   ├── weather.py               # Sample pydantic example agent
│   └── __init__.py              # Package initialization
│
├── testing
│   ├── test_example.py          # Tests for example builder agent
│   ├── test_research.py         # Tests for research agent
│   └── __init__.py              # Package initialization
│
├── .env                         # Environment variables (you create this)
├── .env.example                 # Example .env file
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Project configuration
├── README.md                    # Project documentation
├── uv.lock                      # Dependency lock file
└── hello.py                     # Placeholder test script
```

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.10+
- Virtual environment manager (e.g., `venv`)

### **Steps**
1. **Clone the Repository**
   ```bash
   git clone <repo-url>
   cd scrawl
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   uv sync
   ```

4. **Configure Environment Variables**
   - Copy `.env.example` to `.env` and update keys.
   ```bash
   cp .env.example .env
   ```
   - Set your OpenAI API key and other secrets in `.env`.

---

## **Usage**

### **Run Research Agent**
```bash
uv run python agents/research.py
```
Fetch trending technologies and store results in the database.

### **Run Example Builder Agent**
```bash
uv run python agents/example_builder.py
```
Generate example code snippets for the stored technologies.

---

## **Testing**
> [!IMPORTANT]
> Testing does not quite work here
- [ ] Implement unit tests for the Research Agent
- [ ] Implement unit tests for the Example Builder Agent
- [ ] Integrate testing with CI/CD pipeline

### **Run Tests**
```bash
uv run pytest testing/test_research.py -v
uv run pytest testing/test_example.py -v
```

### **Test Coverage**
For coverage reports:
```bash
pytest --cov=agents --cov-report=html
```

---

## **Customization and Extensions**

### **Add New Tools to Agents**
- Define new tools in the agent files (e.g., `research.py`).
- Use the `@agent.tool` decorator.

### **Extend Database Schema**
- Modify `db.py` to create additional tables.

### **Additional Features**
- Integrate new APIs like Google Trends.
- Expand example builder to support frameworks like React and Next.js.

---

## **Contributing**
Contributions are welcome! Please submit issues and pull requests on GitHub.

---

## **License**
This project is licensed under the AGPL 3.0 License. See the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html) for more details.