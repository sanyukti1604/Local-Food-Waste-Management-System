import streamlit as st
import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="food_management"
)

# Predefined queries
queries = {
    "1 What is the contact information of food providers in a specific city?": '''select name as food_providers,city,Contact from providers 
order BY city;''',
    "How many food providers and receivers are there in each city?": '''SELECT 
    city,
    SUM(provider_count) AS provider_count,
    SUM(receiver_count) AS receiver_count
FROM (
    SELECT 
        city,
        COUNT(provider_id) AS provider_count,
        0 AS receiver_count
    FROM providers
    GROUP BY city

    UNION ALL

    SELECT 
        city,
        0 AS provider_count,
        COUNT(receiver_id) AS receiver_count
    FROM receivers_data
    GROUP BY city
) AS combined
GROUP BY city
ORDER BY city;''',
    "2 All receivers": "SELECT * FROM receivers_data",
    "3 Which type of food provider (restaurant, grocery store, etc.) contributes the most food?": 
    '''select Type as providers_Type, count(*) as Total_Donation_Food 
from providers
GROUP BY providers_Type
order by Total_Donation_Food desc;''',
    "4 Which receivers have claimed the most food?": '''select r.Receiver_ID,r.Name, 
count(c.claim_ID) as  Total_Claims
from receivers_data r
left join claims_data c 
on r.Receiver_ID = c.receiver_ID 
GROUP BY r.receiver_id, r.name
order by total_claims DESC;''',
    "5 What is the total quantity of food available from all providers?":'''select f.Provider_ID, sum(f.Quantity) as Total_quantity
 from food_listings_data f
 left join providers p on f.Provider_ID = p.Provider_ID
 GROUP BY f.Provider_ID;''',
    "6 Which city has the highest number of food listings?": '''select p.city,Count(f.Food_Type) as food_listing
from food_listings_data f left join providers p on  f.Provider_ID = p.Provider_ID
GROUP BY city
order by food_listing DESC ;''',
    "7 What are the most commonly available food types?": '''select f.Food_Type, count(*) as most_available_food 
from food_listings_data f
GROUP BY Food_Type
order by most_available_food DESC;''',
    "8 How many food claims have been made for each food item?": '''select f.Food_Name,f.Food_Type,count(c.claim_ID) as Food_Claims 
from food_listings_data f
left join claims_data c on f.Food_ID = c.Food_ID
group by f.Food_Name,f.Food_Type
order by food_claims DESC ;''',
    " 9 Which provider has had the highest number of successful food claims?": '''select f.provider_ID,count(c.claim_ID) as highest_food_claims 
from food_listings_data f
left join claims_data c on f.Food_ID = c.Food_ID
group by f.provider_ID
order by highest_food_claims DESC limit 1;''',
    "10 What percentage of food claims are completed vs. pending vs. canceled?": '''SELECT 
    Status,
    COUNT(*) AS Total_Claims,
    ROUND(COUNT(*) * 100.0 / t.total_count, 2) AS Percentage
FROM claims_data
CROSS JOIN (
    SELECT COUNT(*) AS total_count
    FROM claims_data
) t
GROUP BY Status, t.total_count
ORDER BY Percentage DESC;''',
    "11. What is the average quantity of food claimed per receiver?": '''SELECT 
    c.Receiver_ID, 
    AVG(f.Quantity) AS Average_Quantity
FROM claims_data c
JOIN food_listings_data f 
    ON c.Food_ID = f.Food_ID
GROUP BY c.Receiver_ID
ORDER BY Average_Quantity DESC;''',
    "12 Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?": '''select f.Meal_Type, count(c.Claim_ID) as Most_Claimed_food 
from food_listings_data f 
left join claims_data c  on f.Food_ID = c.Food_ID
GROUP BY f.Meal_Type
ORDER BY Most_Claimed_food DESC;''',
    "13.What is the total quantity of food donated by each provider?": '''select p.Provider_ID,
sum(f.Quantity) As Total_Quantity from providers p 
left join food_listings_data f on p.provider_id = f.provider_id
GROUP BY p.Provider_ID
ORDER BY Total_Quantity;'''
}
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
            password="123456",
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
# ---------- CUSTOM QUERY 1 ---------- #
st.subheader("🔍 Custom SQL Query ")
user_query1 = st.text_area("Enter SQL query :", "SELECT * FROM providers LIMIT 5;", key="query1")

if st.button("Run Query", key="btn1"):
    df1 = run_query(user_query1)
    if not df1.empty:
        st.dataframe(df1)
    else:
        st.warning("No data returned.")

#st.title("🍽 Local Food Wastage Management System")

# Dropdown to select query
selected_query_name = st.selectbox("Select a query to run:", list(queries.keys()))

if st.button("Run Query"):
    query = queries[selected_query_name]
    df = pd.read_sql(query, conn)  # Fetch results into a DataFrame
    st.dataframe(df)  


import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
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
