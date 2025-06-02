import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='cv_db',
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_tables():
    conn = get_db_connection()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantProfile (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) DEFAULT NULL,
        last_name VARCHAR(100) DEFAULT NULL,
        email VARCHAR(100) DEFAULT NULL,
        date_of_birth DATE DEFAULT NULL,
        applicant_address VARCHAR(255) DEFAULT NULL,
        phone_number VARCHAR(20) DEFAULT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ApplicationDetail (
        id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT NOT NULL,
        applicant_role VARCHAR(100) DEFAULT NULL,
        cv_path TEXT NOT NULL,
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
