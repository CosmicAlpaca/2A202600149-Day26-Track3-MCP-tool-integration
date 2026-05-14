#!/bin/bash
export GEMINI_API_KEY="AIzaSyDw06iPDrC4Be6-q7L7kQSSJgcE7LErlrY"
echo "Adding SQLite MCP server to Gemini CLI..."
gemini mcp add sqlite-lab python mcp_server.py --description "SQLite lab FastMCP server" --timeout 10000
echo "Running smoke test with Gemini CLI..."
gemini --allowed-mcp-server-names sqlite-lab --yolo -p "Use the sqlite-lab MCP server and show me the top 2 students by score."
