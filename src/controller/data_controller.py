'''
Fetch dan convert data (ke long string) dari database
'''
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.db_setup import get_db_connection
from model.encryptor import Encryptor

encryptor = Encryptor("SIGNHIRE")

# ini bisa diambil dari nayla
def extract_cv_long_string(filepath : str) :
    ''' extract cv to long string and save to temp .txt '''
    return

def extract_cv_regex_string(filepath : str) :
    ''' extract cv to regex string and save to temp .txt '''
    return

def extract_cv_data(cv_path : list) -> list :
    ''' pass cv_path from query, return list of txt path '''
    return []

def extract_regex_data(cv_path : list) -> list :
    ''' pass cv_path from query, return list of txt path '''
    return []

def get_cv_paths() -> list :
    ''' mengembalikan list of (id_detail, cv_path)'''
    conn = get_db_connection()
    cur = conn.cursor(prepared=True) # cek ini ngapain euy
    cur.execute("""
        SELECT detail_id, cv_path
        FROM ApplicationDetail
    """)
    
    result = cur.fetchall()
    
    formatted_result = {}
    for row in result:
        detail_id = row[0]
        formatted_result[detail_id] = row[1]
    
    # close connection
    if cur:
        cur.close()
    if conn:
        conn.close()
    return formatted_result


def get_applicant_data(id_list : list) -> map :
    ''' mengembalikan data applicant (nama, email, date_of_birth, dll)'''
    placeholder = ','.join(['%s'] * len(id_list))
    conn = get_db_connection()
    cur = conn.cursor(prepared=True)
    cur.execute(f"""
        SELECT ad.detail_id, first_name, last_name, email, date_of_birth, applicant_address, phone_number
        FROM ApplicantProfile ap JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        WHERE ad.detail_id IN ({placeholder})
    """, id_list)
    
    ''' return map{key: detail_id, val: cv_path} '''
    result = cur.fetchall()
    
    formatted_result = {}
    for row in result:
        detail_id = row[0]
        dob = row[4]
        dob_str = dob.strftime("%d %B %Y") if dob else None
        formatted_result[detail_id] = {
            "name": encryptor.decrypt(row[1]) + " " + encryptor.decrypt(row[2]),
            "email": encryptor.decrypt(row[3]),
            "date_of_birth": dob_str,
            "applicant_address": encryptor.decrypt(row[5]),
            "phone_number": encryptor.decrypt(row[6])
        }
        
    # close connection
    if cur:
        cur.close()
    if conn:
        conn.close()
    ''' return map{key:detail_id, map{key: atribut/biodata}}} '''
    return formatted_result

    
if __name__ == "__main__":
    # res = get_cv_paths()
    # print(res)
    res = get_applicant_data([1,3,7,9,100])
    print(res)