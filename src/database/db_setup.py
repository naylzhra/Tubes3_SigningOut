import mysql.connector

# sementara ini db bersifat lokal krn pas mau dibikin remote gt aku butuh public key kalian buat bikin tunnel ssh nya

# cara runnya ikutin ini:
# mysql -u root -p
# masukin password
# CREATE USER 'cv_app'@'localhost' IDENTIFIED BY 'signingout';
# CREATE DATABASE cv_db;
# GRANT ALL PRIVILEGES ON cv_db.* TO 'cv_app'@'localhost';
# FLUSH PRIVILEGES;
# trs bisa lgsg jalanin file ini trs seeder.py
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='cv_app',
            password='signingout',
            database='cv_db',
            auth_plugin= 'mysql_native_password'
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
        applicant_id INT AUTO_INCREMENT PRIMARY KEY,
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
        detail_id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT NOT NULL,
        applicant_role VARCHAR(100) DEFAULT NULL,
        cv_path TEXT NOT NULL,
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()