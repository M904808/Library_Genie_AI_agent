
import os
import re
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from groq import Groq

# 1. Page configuration
st.set_page_config(
    page_title="LibraryGenie",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LibraryGenie")
st.write("Ask questions about the library in English or Roman Urdu.")

# 2. Locate the database
DB_PATH = Path(__file__).with_name("library.db")

# 3. Read-only database function
def run_sql(sql):
    sql = sql.strip()

    # Allow only one SELECT statement
    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    # Remove one optional trailing semicolon
    sql = sql.rstrip(";").strip()

    if ";" in sql or "--" in sql or "/*" in sql:
        raise ValueError("Only a single, simple SELECT query is allowed.")

    # Open the database in read-only mode
    connection = sqlite3.connect(
        DB_PATH.resolve().as_uri() + "?mode=ro",
        uri=True
    )

    try:
        connection.execute("PRAGMA query_only = ON")
        cursor = connection.execute(sql)
        rows = cursor.fetchall()
        columns = [item[0] for item in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        connection.close()

# 4.
import os
import streamlit as st
from groq import Groq

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found.")
    st.stop()

client = Groq(api_key=api_key)
# 5. Ask the student a question
question = st.text_input(
    "Enter your question",
    placeholder="Example: Show the 5 most borrowed books"
)

if st.button("Ask LibraryGenie", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not DB_PATH.exists():
        st.error("library.db was not found. Run create_library_db.py first.")
    else:
        try:
            with st.spinner("Understanding your question..."):

                # 6. Ask Groq to generate SQL
                sql_response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are LibraryGenie, an assistant for a school library.

The SQLite database contains one table: books.
Its columns are:
book_id, title, author, category,
available_copies, times_borrowed.

Convert the user's question into ONE SQLite SELECT query.
Use only the books table and the columns listed above.
Questions may be in English or Roman Urdu.
Return only the SQL query, without Markdown or explanation.
Never generate INSERT, UPDATE, DELETE, DROP, or other write queries.
"""
                        },
                        {"role": "user", "content": question}
                    ],
                    temperature=0
                )

                sql = sql_response.choices[0].message.content.strip()
                sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
                sql = re.sub(r"\s*```$", "", sql).strip()

            # 7. Show the generated SQL
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # 8. Execute SQL and display actual database results
            with st.spinner("Reading the library database..."):
                result = run_sql(sql)

            st.subheader("Results")
            st.dataframe(result, use_container_width=True)

            # 9. Ask AI to explain the actual results
            with st.spinner("Preparing a simple explanation..."):
                explanation_response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Explain database results simply. "
                                "Use English or Roman Urdu to match "
                                "the user's question. Use only the "
                                "provided results. Never invent facts."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Question: {question}\n"
                                f"Database results: "
                                f"{result.to_dict(orient='records')}\n"
                                "Explain what these results mean."
                            )
                        }
                    ],
                    temperature=0
                )

            st.subheader("AI Explanation")
            st.write(
                explanation_response.choices[0].message.content
            )

            # 10. Required source label
            st.caption("Source: books table")

        except Exception as error:
            st.error(f"Unable to answer this question: {error}")
