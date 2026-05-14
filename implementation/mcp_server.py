from mcp.server.fastmcp import FastMCP
import db
import json

mcp = FastMCP("sqlite-lab")

@mcp.resource("schema://database")
def get_full_schema() -> str:
    """Get the full database schema in JSON format."""
    return json.dumps(db.get_schema(), indent=2)

@mcp.resource("schema://table/{table_name}")
def get_single_table_schema(table_name: str) -> str:
    """Get the schema for a specific table in JSON format."""
    schema = db.get_table_schema(table_name)
    if not schema:
        raise ValueError(f"Table not found: {table_name}")
    return json.dumps(schema, indent=2)

@mcp.tool()
def search(table: str, filters: dict = None, order_by: str = None, limit: int = 10, offset: int = 0) -> str:
    """
    Search records in a table with optional filters, ordering, and pagination.
    Example filters: {"cohort": "A1"} or {"score": {">": 90}}
    """
    try:
        results = db.search_records(table, filters, order_by, limit, offset)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def insert(table: str, data: dict) -> str:
    """
    Insert a new record into a table.
    Example data: {"name": "Eve", "cohort": "C3", "score": 85.0}
    """
    try:
        result = db.insert_record(table, data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def aggregate(table: str, agg_func: str, column: str = None) -> str:
    """
    Compute an aggregate function over a table.
    agg_func: one of 'count', 'avg', 'sum', 'min', 'max'.
    column: column name to aggregate over (can be omitted for 'count').
    """
    try:
        result = db.aggregate_records(table, agg_func, column)
        return json.dumps({"result": result}, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
