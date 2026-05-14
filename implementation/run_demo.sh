#!/bin/bash
echo "🚀 Starting Premium MCP Dashboard..."
echo "Installing streamlit if not present..."
pip install streamlit pandas
streamlit run dashboard.py
