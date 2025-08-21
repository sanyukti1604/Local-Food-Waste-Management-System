import streamlit as st
import mysql.connector
import pandas as pd

# ---------- CONFIG ---------- #
st.set_page_config(page_title="Local Food Wastage Management System", layout="centered")

# ---------- HEADER ---------- #
st.title("🍽 Local Food Wastage Management System")
st.write("Streamlit is running!")

# ---------- DB CONNECTION ---------- #
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="newpassword",
            database="food_management"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

# ---------- QUERY RUNNER ---------- #
def run_query(query):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            return pd.DataFrame(data, columns=cols)
        except Exception as e:
            st.error(f"Query failed: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()

# ---------- CONNECTION TEST ---------- #
if get_connection():
    st.success("✅ Connected to MySQL!")
else:
    st.error("❌ Failed to connect to MySQL.")

# ---------- SAMPLE DATA ---------- #
st.subheader("📊 Sample Data from Providers Table")
sample_df = run_query("SELECT * FROM providers LIMIT 10;")
if not sample_df.empty:
    st.dataframe(sample_df)
else:
    st.warning("No sample data available.")

# ---------- CUSTOM QUERY 1 ---------- #
st.subheader("🔍 Custom SQL Query - Providers")
user_query1 = st.text_area("Enter SQL query for 'providers':", "SELECT * FROM providers LIMIT 5;", key="query1")

if st.button("Run Providers Query", key="btn1"):
    df1 = run_query(user_query1)
    if not df1.empty:
        st.dataframe(df1)
    else:
        st.warning("No data returned.")

# ---------- CUSTOM QUERY 2 ---------- #
st.subheader("🔍 Custom SQL Query - Food Donations")
user_query2 = st.text_area("Enter SQL query for 'food_donations':", "SELECT * FROM receivers;", key="query2")

if st.button("Run Query", key="btn2"):
    df2 = run_query(user_query2)
    if not df2.empty:
        st.dataframe(df2)
    else:
        st.warning("No data returned.")

# ---------- OPTIONAL: SHOW TABLE DATA BUTTON ---------- #
if st.button("Show Full Providers Table", key="btn"):
    df_full = run_query("SELECT * FROM providers;")
    if not df_full.empty:
        st.dataframe(df_full)
    else:
        st.warning("Table is empty or failed to load.")
######
st.subheader("🔍 Custom SQL Query - Providers")
user_query3 = st.text_area(
    "Which type of food provider (restaurant, grocery store, etc.) contributes the most food?:", 
    '''SELECT Type AS providers_Type, COUNT(*) AS Total_Donation_Food 
FROM providers
GROUP BY providers_Type
ORDER BY Total_Donation_Food DESC;''', 
    key="query3"
)

if st.button("Run Query", key="btn3"):
    df3 = run_query(user_query3)
    if not df3.empty:
        st.dataframe(df3)
    else:
        st.warning("No data returned.")

# Food Providers & Receivers

st.subheader("🔍 Custom SQL Query - Food Providers & Receivers")
user_query4 = st.text_area(
    "What is the contact information of food providers in a specific city?", 
    '''select name as food_providers,city,Contact from providers 
order BY city;''', 
    key="query4"
)

if st.button("Run Query", key="btn4"):
    df4 = run_query(user_query4)
    if not df4.empty:
        st.dataframe(df4)
    else:
        st.warning("No data returned.")


import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="newpassword",
    database="food_management"
)
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SHOW TABLES")
tables = [t[0] for t in cursor.fetchall()]

st.sidebar.header("CRUD Operations")
selected_table = st.sidebar.selectbox("Select Table", tables)

# Get column names dynamically
cursor.execute(f"DESCRIBE {selected_table}")
columns = [col[0] for col in cursor.fetchall()]

operation = st.sidebar.radio("Select Operation", ["Create", "Read", "Update", "Delete"])

# ---- CREATE ----
if operation == "Create":
    st.subheader(f"Insert into {selected_table}")
    values = []
    for col in columns:
        val = st.text_input(f"Enter {col}")
        values.append(val)
    if st.button("Insert"):
        placeholders = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {selected_table} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(values))
        conn.commit()
        st.success("Record inserted successfully ✅")

# ---- READ ----
elif operation == "Read":
    st.subheader(f"View {selected_table}")
    cursor.execute(f"SELECT * FROM {selected_table}")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

# ---- UPDATE ----
elif operation == "Update":
    st.subheader(f"Update {selected_table}")
    id_col = columns[0]   # assume first column is primary key
    record_id = st.text_input(f"Enter {id_col} of record to update")
    updates = {}
    for col in columns[1:]:
        new_val = st.text_input(f"New {col} (leave blank to skip)")
        if new_val:
            updates[col] = new_val

    if st.button("Update"):
        set_clause = ", ".join([f"{col}=%s" for col in updates.keys()])
        sql = f"UPDATE {selected_table} SET {set_clause} WHERE {id_col}=%s"
        cursor.execute(sql, tuple(updates.values()) + (record_id,))
        conn.commit()
        st.success("Record updated successfully ✅")

# ---- DELETE ----
elif operation == "Delete":
    st.subheader(f"Delete from {selected_table}")
    id_col = columns[0]
    record_id = st.text_input(f"Enter {id_col} of record to delete")
    if st.button("Delete"):
        sql = f"DELETE FROM {selected_table} WHERE {id_col}=%s"
        cursor.execute(sql, (record_id,))
        conn.commit()
        st.success("Record deleted successfully ❌")
