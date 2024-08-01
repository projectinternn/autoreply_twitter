import psycopg2
import pyodbc

def connect_postgresql():
    try:
        pg_connection = psycopg2.connect(
            dbname="stm",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL")
        return pg_connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def connect_sql_server():
    try:
        SERVER = 'DESKTOP-53R30V6\MSSQLSERVER01'  # Gunakan dua backslashes untuk escape character
        DATABASE = 'OutageABM'
        USERNAME = 'sa'
        PASSWORD = '1234'
        
        # String koneksi
        connectionString = (
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD};'
            f'Encrypt=yes;'  # Menyertakan enkripsi
            f'TrustServerCertificate=yes'  # Percaya sertifikat server
        )
        
        sql_connection = pyodbc.connect(connectionString)
        print("Connected to MS SQL Server")
        return sql_connection
    except Exception as e:
        print(f"Error connecting to MS SQL Server: {e}")
        return None

def fetch_twitter_user(screen_name, pg_connection):
    try:
        cursor = pg_connection.cursor()
        query = "SELECT * FROM customer WHERE screen_name = %s"
        cursor.execute(query, (screen_name,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            print(f"Twitter user found: {result}")
        else:
            print("No Twitter user found.")
        return result
    except Exception as e:
        print(f"Error fetching Twitter user: {e}")
        return None

def fetch_outage(subscriber_id, sql_connection):
    try:
        cursor = sql_connection.cursor()
        query = "SELECT * FROM TicketOpen_Detail WHERE CUST_ACCT = ?"
        cursor.execute(query, (10034622,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            print(f"Outage details found: {result}")
        else:
            print("No outage details found.")
        return result
    except Exception as e:
        print(f"Error fetching outage: {e}")
        return None

def main():
    pg_connection = connect_postgresql()
    sql_connection = connect_sql_server()

    if pg_connection and sql_connection:
        screen_name = "Vanni1295_"
        twitter_user = fetch_twitter_user(screen_name, pg_connection)
        
        if twitter_user:
            subscriber_id = twitter_user[2]  # Assuming subscriber_id is the 3rd column
            outage_details = fetch_outage(subscriber_id, sql_connection)
            
            if outage_details:
                estimation_done = outage_details[3]  # Assuming ESTIMATIONDONE is the 4th column
                if estimation_done:
                    message = (
                        "Hi First People, Sorry for the inconvenience, your area is currently "
                        "experiencing problems and is still being repaired. Estimation time: "
                        f"{estimation_done}."
                    )
                else:
                    message = (
                        "Hi First People, Sorry for the inconvenience, your area is currently "
                        "experiencing problems and is still being repaired. The estimated time "
                        "for repairs is around 12x6 hours."
                    )
                print(message)
            else:
                print("No outage details found.")
        else:
            print("No Twitter user found.")
        
        pg_connection.close()
        sql_connection.close()
    else:
        print("Failed to connect to one or both databases.")

if __name__ == "__main__":
    main()
