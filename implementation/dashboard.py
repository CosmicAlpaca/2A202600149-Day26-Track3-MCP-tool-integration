import streamlit as st
import db
import json
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SQLite MCP Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Glassmorphism card */
    .stCard {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    .log-container {
        background: #000000;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
        padding: 10px;
        border-radius: 5px;
        height: 200px;
        overflow-y: auto;
        font-size: 12px;
    }

    .header-text {
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGGING UTILITY ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

def add_log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {msg}")

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color: #60a5fa;'>MCP Control</h1>", unsafe_allow_html=True)
    option = st.radio(
        "Navigate to:",
        ["🔍 Search Records", "➕ Insert Data", "📊 Aggregate Stats", "📜 Database Schema"],
        index=0
    )
    st.divider()
    if st.button("Clear Logs"):
        st.session_state.logs = []
        st.rerun()

# --- HEADER ---
st.markdown("<h1 class='header-text'>SQLite Lab Demo</h1>", unsafe_allow_html=True)

# --- MAIN CONTENT ---
col1, col2 = st.columns([2, 1])

with col1:
    if option == "🔍 Search Records":
        st.subheader("Search Records")
        with st.form("search_form"):
            table = st.selectbox("Select Table", ["students", "courses", "enrollments"])
            filter_col = st.text_input("Filter Column (optional)", placeholder="e.g. cohort")
            filter_val = st.text_input("Filter Value (optional)", placeholder="e.g. A1")
            order_by = st.text_input("Order By (optional)", placeholder="e.g. score DESC")
            limit = st.slider("Limit", 1, 50, 10)
            
            submitted = st.form_submit_button("Search")
            if submitted:
                add_log(f"Initiating search on {table}...")
                try:
                    filters = {filter_col: filter_val} if filter_col and filter_val else None
                    results = db.search_records(table, filters, order_by, limit)
                    st.success(f"Found {len(results)} records")
                    st.dataframe(pd.DataFrame(results), use_container_width=True)
                    add_log(f"Search successful. {len(results)} rows returned.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    add_log(f"ERROR: {str(e)}")

    elif option == "➕ Insert Data":
        st.subheader("Insert New Student")
        with st.form("insert_form"):
            name = st.text_input("Name")
            cohort = st.text_input("Cohort")
            score = st.number_input("Score", 0.0, 100.0, 90.0)
            
            submitted = st.form_submit_button("Insert Student")
            if submitted:
                add_log(f"Inserting new student: {name}...")
                try:
                    res = db.insert_record('students', {'name': name, 'cohort': cohort, 'score': score})
                    st.success("Student added successfully!")
                    st.json(res)
                    add_log(f"Insert successful. Assigned ID: {res.get('id')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    add_log(f"ERROR: {str(e)}")

    elif option == "📊 Aggregate Stats":
        st.subheader("Run Aggregates")
        with st.form("agg_form"):
            table = st.selectbox("Select Table", ["students", "courses", "enrollments"], key="agg_table")
            func = st.selectbox("Function", ["count", "avg", "sum", "min", "max"])
            column = st.text_input("Column (use '*' for count)", value="score")
            
            submitted = st.form_submit_button("Calculate")
            if submitted:
                add_log(f"Calculating {func}({column}) on {table}...")
                try:
                    res = db.aggregate_records(table, func, column if column != '*' else None)
                    st.metric(label=f"{func.upper()} of {column}", value=res)
                    add_log(f"Aggregation result: {res}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    add_log(f"ERROR: {str(e)}")

    elif option == "📜 Database Schema":
        st.subheader("Database Schema Inspection")
        tab1, tab2 = st.tabs(["Full Schema", "Per-Table Details"])
        
        with tab1:
            if st.button("Fetch Full Schema"):
                add_log("Fetching full database schema...")
                schema = db.get_schema()
                st.json(schema)
                add_log("Schema retrieved successfully.")
        
        with tab2:
            table_name = st.selectbox("Select Table to Inspect", ["students", "courses", "enrollments"])
            if st.button(f"Fetch {table_name} Schema"):
                add_log(f"Fetching schema for table: {table_name}...")
                schema = db.get_table_schema(table_name)
                st.table(pd.DataFrame(schema))
                add_log(f"Table schema for {table_name} retrieved.")

with col2:
    st.subheader("Console Logs")
    log_text = "\n".join(st.session_state.logs[::-1])
    st.markdown(f'<div class="log-container">{log_text.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 **Pro-Tip:** Use the Gemini CLI commands from README.md to see how the AI agent uses these tools in the background!")

# --- FOOTER ---
st.caption("SQLite MCP Lab | Built with ❤️ by Antigravity")
