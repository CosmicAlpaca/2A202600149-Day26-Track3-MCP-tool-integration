import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_schema() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    schema = {}
    for table in tables:
        table_name = table['name']
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema[table_name] = [dict(col) for col in columns]
    conn.close()
    return schema

def get_table_schema(table_name: str) -> Optional[List[Dict[str, Any]]]:
    schema = get_schema()
    return schema.get(table_name)

def _validate_table_and_columns(table: str, columns: List[str] = None):
    schema = get_schema()
    if table not in schema:
        raise ValueError(f"Unknown table: {table}")
    
    if columns:
        valid_columns = {col['name'] for col in schema[table]}
        for col in columns:
            if col not in valid_columns:
                raise ValueError(f"Unknown column '{col}' in table '{table}'")

def search_records(table: str, filters: Dict[str, Any] = None, order_by: str = None, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    _validate_table_and_columns(table)
    
    query = f"SELECT * FROM {table}"
    params = []
    
    if filters:
        conditions = []
        schema = get_schema()
        valid_columns = {col['name'] for col in schema[table]}
        
        for col, value in filters.items():
            if col not in valid_columns:
                raise ValueError(f"Unknown column '{col}' in filter")
            
            if isinstance(value, dict):
                for op, val in value.items():
                    if op not in ('=', '!=', '>', '<', '>=', '<=', 'LIKE'):
                        raise ValueError(f"Unsupported filter operator: {op}")
                    conditions.append(f"{col} {op} ?")
                    params.append(val)
            else:
                conditions.append(f"{col} = ?")
                params.append(value)
                
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
    if order_by:
        parts = order_by.split()
        col = parts[0]
        direction = parts[1].upper() if len(parts) > 1 else "ASC"
        
        _validate_table_and_columns(table, [col])
        if direction not in ("ASC", "DESC"):
            raise ValueError(f"Invalid order direction: {direction}")
            
        query += f" ORDER BY {col} {direction}"
        
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def insert_record(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if not data:
        raise ValueError("Empty inserts are not allowed")
        
    _validate_table_and_columns(table, list(data.keys()))
    
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    values = list(data.values())
    
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    inserted_id = cursor.lastrowid
    
    cursor.execute(f"SELECT * FROM {table} WHERE rowid = ?", (inserted_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row)

def aggregate_records(table: str, agg_func: str, column: str = None) -> Any:
    _validate_table_and_columns(table, [column] if column and column != '*' else None)
    
    valid_funcs = ('count', 'avg', 'sum', 'min', 'max')
    agg_func = agg_func.lower()
    if agg_func not in valid_funcs:
        raise ValueError(f"Invalid aggregate function: {agg_func}")
        
    if column is None:
        if agg_func == 'count':
            column = '*'
        else:
            raise ValueError(f"Column is required for aggregate function: {agg_func}")
            
    query = f"SELECT {agg_func.upper()}({column}) as result FROM {table}"
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    
    return row['result']
