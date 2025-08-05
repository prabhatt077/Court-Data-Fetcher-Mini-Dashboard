import mysql.connector

def log_to_mysql(case_type, case_number, filing_year, html_response,result_summary):
    try:
        conn = mysql.connector.connect(
            host="localhost",         # or 127.0.0.1
            user="root",
            password="root",
            database="court_data"
        )

        cursor = conn.cursor()
        query = """
            INSERT INTO case_logs (case_type, case_number, filing_year, html_response, result_summary)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (case_type, case_number, filing_year, html_response,result_summary)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Logged to MySQL successfully.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
