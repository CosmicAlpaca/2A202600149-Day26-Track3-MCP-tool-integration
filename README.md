# SQLite Database MCP Server

A Model Context Protocol (MCP) server built with FastMCP that exposes a SQLite database through specialized tools and resources.

## Features

- **Tools**:
  - `search`: Search records with filters, ordering, and pagination.
  - `insert`: Securely add new records to the database.
  - `aggregate`: Compute metrics like `count`, `avg`, `sum`, `min`, and `max`.
- **Resources**:
  - `schema://database`: Full database schema.
  - `schema://table/{table_name}`: Dynamic schema for a specific table.
- **Safety**: Validates table/column names and uses parameterized SQL to prevent injection.

## Project Structure

```text
implementation/
  database.sqlite    # The database file
  db.py             # Database logic layer
  init_db.py        # Database initialization script
  mcp_server.py     # FastMCP server implementation
  verify_server.py  # Smoke test script
  mcp_client_test.sh # Gemini CLI test script
  start_inspector.sh # MCP Inspector helper
  dashboard.py      # Premium Web Dashboard
  tests/
    test_server.py  # Unit tests
```

## Setup Instructions

1.  **Install dependencies**:
    ```bash
    pip install mcp[cli] fastmcp streamlit pandas
    ```

2.  **Initialize the database**:
    ```bash
    cd implementation
    python init_db.py
    ```

3.  **Run the server**:
    ```bash
    python mcp_server.py
    ```

## Web Dashboard Demo

A premium Streamlit-based dashboard is provided to interact with the database visually.

### How to Run:
```bash
cd implementation
streamlit run dashboard.py
```

Features:
- **Interactive Forms**: Test search, insert, and aggregate tools.
- **Schema Browser**: View full database or individual table structures.
- **Real-time Logs**: Monitor operations as they happen.
- **Premium UI**: Dark mode with glassmorphism effects.

## Testing and Verification

### Automated Tests
Run the unit tests to verify logic:
```bash
python -m unittest tests/test_server.py
```

### Smoke Test
Verify basic DB connectivity and operations:
```bash
python verify_server.py
```

### MCP Inspector
Test the MCP interface visually:
```bash
./start_inspector.sh
```

## Client Configuration

### Gemini CLI
You can add this server to Gemini CLI for interaction:
```bash
gemini mcp add sqlite-lab python /PATH/TO/implementation/mcp_server.py --description "SQLite lab FastMCP server"
```

### Claude Code
Add to your `.mcp.json`:
```json
{
  "mcpServers": {
    "sqlite-lab": {
      "command": "python",
      "args": ["/PATH/TO/implementation/mcp_server.py"]
    }
  }
}
```

## Example Queries for AI
- "Search all students in cohort A1"
- "Count the number of enrollments"
- "Show me the schema of the students table"
- "Insert a new student named Eve in cohort C3 with a score of 85"