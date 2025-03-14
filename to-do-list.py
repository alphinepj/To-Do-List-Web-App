import streamlit as st
import pandas as pd
import datetime

# File to store tasks
TASKS_FILE = "tasks.csv"

# Load tasks from CSV
def load_tasks():
    try:
        return pd.read_csv(TASKS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Task", "Date", "Time", "Status"])

# Save tasks to CSV
def save_tasks(df):
    df.to_csv(TASKS_FILE, index=False)

# Initialize tasks
df = load_tasks()

# Streamlit UI
st.set_page_config(page_title="To-Do List", layout="centered")
st.title("✅ Modern To-Do List")

# Task input fields
task = st.text_input("Task Name", "")
date = st.date_input("Due Date", datetime.date.today())
time = st.time_input("Due Time", datetime.datetime.now().time())

if st.button("➕ Add Task"):
    if task:
        new_task = pd.DataFrame([[task, date, time, "Pending"]], columns=df.columns)
        df = pd.concat([df, new_task], ignore_index=True)
        save_tasks(df)
        st.rerun()  # Updated function
    else:
        st.warning("Task cannot be empty!")

# Display tasks
st.subheader("📋 Task List")
if not df.empty:
    for i, row in df.iterrows():
        status_color = "green" if row["Status"] == "Completed" else "red"
        st.markdown(f"<span style='color:{status_color}; font-size:16px;'>{row['Task']} - {row['Date']} {row['Time']} [{row['Status']}]</span>", unsafe_allow_html=True)

        # Buttons to complete or delete tasks
        col1, col2 = st.columns(2)
        if col1.button(f"✔️ Complete {i}", key=f"complete_{i}"):
            df.at[i, "Status"] = "Completed"
            save_tasks(df)
            st.rerun()  # Updated function

        if col2.button(f"❌ Delete {i}", key=f"delete_{i}"):
            df = df.drop(index=i).reset_index(drop=True)
            save_tasks(df)
            st.rerun()  # Updated function
else:
    st.info("No tasks added yet!")

# Run the app with `streamlit run todo_app.py`
