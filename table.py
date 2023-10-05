import sqlite3

# Function to fetch data from the SQLite database
def fetch_data(start_date, end_date):

    conn = sqlite3.connect(r"Crash Statistics Victoria.db")
    cursor = conn.cursor()

    # Replace 'your_table_name' with the actual name of your table
    query = "SELECT OBJECTID, ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ALCOHOL_RELATED, ACCIDENT_TYPE, SEVERITY, REGION_NAME FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ?;"
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    conn.close()
    
    return data




