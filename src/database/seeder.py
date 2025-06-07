import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import itertools
import re
from pathlib import Path
from faker import Faker
from db_setup import get_db_connection
from model.encryptor import Encryptor


fake = Faker()
DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
encryptor = Encryptor("SIGNHIRE")

def clean_phone() -> str:
    digits = re.sub(r'\D', '', fake.phone_number())
    if len(digits) < 10:
        digits = digits.ljust(10, '0')
    return digits[:13]

def clean_db():
    conn = get_db_connection()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cur.execute("TRUNCATE TABLE ApplicationDetail")
    cur.execute("TRUNCATE TABLE ApplicantProfile")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()
    cur.close()
    conn.close()

def seed_applicant_profiles(n: int = 250):
    conn = get_db_connection()
    cur = conn.cursor(prepared=True)
    insert_stmt = """
        INSERT INTO ApplicantProfile
        (first_name, last_name, email, date_of_birth, applicant_address, phone_number)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    for _ in range(n):
        profile = fake.simple_profile()
        first, *last = profile["name"].split()
        cur.execute(insert_stmt, (
            encryptor.encrypt(first),
            encryptor.encrypt(" ".join(last)) if last else "",
            encryptor.encrypt(profile["mail"]),
            profile["birthdate"],
            encryptor.encrypt(profile["address"].replace("\n", ", ")),
            encryptor.encrypt(clean_phone())
        ))
    conn.commit()
    print(f"Seeded {n} ApplicantProfile rows.")
    cur.close()
    conn.close()


def seed_application_details(max_roles_per_applicant: int = 2):
    conn = get_db_connection()
    if conn is None:
        print("DB connection failed — aborting.")
        return

    cur = conn.cursor(prepared=True)
    cur.execute("SELECT applicant_id FROM ApplicantProfile ORDER BY applicant_id")
    applicants = [row[0] for row in cur.fetchall()]

    if not applicants:
        print("No ApplicantProfile rows yet — seed them first.")
        return

    app_cycle = itertools.cycle(applicants)
    roles_count = {aid: 0 for aid in applicants}

    def next_applicant() -> int:
        """Return an applicant_id that still has quota left."""
        while True:
            aid = next(app_cycle)
            if roles_count[aid] < max_roles_per_applicant:
                roles_count[aid] += 1
                return aid

    insert_stmt = """
        INSERT INTO ApplicationDetail (applicant_id, applicant_role, cv_path)
        VALUES (%s, %s, %s)
    """

    pdf_paths = sorted(DATA_ROOT.glob("*/*.pdf"))
    if not pdf_paths:
        print(f"No PDFs found under {DATA_ROOT}")
        return

    for i, pdf in enumerate(pdf_paths, start=1):
        role = pdf.parent.name.upper()
        applicant_id = next_applicant()
        cur.execute(
            insert_stmt,
            (applicant_id, role, str(pdf.relative_to(DATA_ROOT.parent)))
        )
        if i % 50 == 0:
            print(f"Inserted {i} rows…")

    conn.commit()
    print(f"Inserted total {len(pdf_paths)} ApplicationDetail rows "
          f"using {len(applicants)} applicants "
          f"(max {max_roles_per_applicant} roles each).")

    cur.close()
    conn.close()

if __name__ == "__main__":
    clean_db()
    seed_applicant_profiles(400)
    seed_application_details(2)
