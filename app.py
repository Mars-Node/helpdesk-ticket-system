
import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Connect to the SQLite database
conn = sqlite3.connect('helpdesk.db')
cursor = conn.cursor()

st.title("🎫 Help Desk Ticketing System")

# Section: View all tickets
st.header("📋 All Tickets")
tickets = pd.read_sql_query("SELECT * FROM tickets", conn)
st.dataframe(tickets)

# Section: Filter tickets by status
st.subheader("🔍 Filter by Status")
status_options = ["All"] + tickets['status'].dropna().unique().tolist()
status_filter = st.selectbox("Select status", status_options)

if status_filter != "All":
    filtered = pd.read_sql_query("SELECT * FROM tickets WHERE status = ?", conn, params=(status_filter,))
    st.dataframe(filtered)

# Section: Metrics
st.subheader("📊 Metrics")
avg_days_query = """
    SELECT AVG(julianday(resolved_at) - julianday(created_at)) AS avg_days
    FROM tickets
    WHERE status = 'Closed'
"""
avg_days = pd.read_sql_query(avg_days_query, conn)
if avg_days['avg_days'][0] is not None:
    st.metric("Average Resolution Time (Days)", round(avg_days['avg_days'][0], 2))
else:
    st.write("No closed tickets to calculate average resolution time.")

# Section: Add a new ticket
st.header("➕ Submit a New Ticket")
with st.form("ticket_form"):
    user_id = st.number_input("User ID", step=1)
    tech_id = st.number_input("Technician ID", step=1)
    issue_description = st.text_area("Issue Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    created_at = st.date_input("Created At", value=date.today())
    resolved_at = st.date_input("Resolved At (optional)", value=date.today())

    submitted = st.form_submit_button("Submit Ticket")
    if submitted:
        resolved_value = resolved_at if status == "Closed" else None
        cursor.execute(
            "INSERT INTO tickets (user_id, tech_id, issue_description, status, priority, created_at, resolved_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, tech_id, issue_description, status, priority, created_at, resolved_value)
        )
        conn.commit()
        st.success("Ticket submitted!")

# Close DB connection on app shutdown
st.write("ℹ️ Data is fetched from helpdesk.db")
