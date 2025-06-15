import sys
import os
from pathlib import Path
import re

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    from database.db_setup import get_db_connection
except ImportError:
    try:
        import database.db_setup as db_setup
        get_db_connection = db_setup.get_db_connection
    except ImportError:
        sys.path.insert(0, str(current_dir))
        from db_setup import get_db_connection

try:
    from controller.extractor import extract_cv_content_direct
except ImportError:
    try:
        import controller.extractor as extractor
        extract_cv_content_direct = extractor.extract_cv_content_direct
    except ImportError:
        def extract_cv_content_direct(pdf_path, use_regex=False):
            return f"Mock content from {pdf_path}"
        
from model.encryptor import Encryptor
from model.regex import extract_information_group, generate_summary, extract_education, extract_job_history, extract_skill


class CVDataManager:
    def __init__(self):
        self.cv_cache = {} 
        self.applicant_cache = {}  
        self.skills_cache = {}
        self.encryptor = Encryptor("SIGNHIRE")
        
    def get_cv_paths(self) -> dict:
        try:
            conn = get_db_connection()
            if not conn:
                print("Database connection failed")
                return {}
                
            cur = conn.cursor(prepared=True)
            cur.execute("""
                SELECT detail_id, cv_path
                FROM ApplicationDetail
            """)
            
            result = cur.fetchall()
            
            formatted_result = {}
            for row in result:
                detail_id = row[0]
                cv_path = row[1] 
                formatted_result[f"cv_{detail_id}"] = cv_path
            
            if cur:
                cur.close()
            if conn:
                conn.close()
                
            print(f"Loaded {len(formatted_result)} CV paths from database")
            return formatted_result
            
        except Exception as e:
            print(f"Error getting CV paths: {e}")
            return {}

    def get_applicant_data(self, detail_ids: list) -> dict:
        if not detail_ids:
            return {}
            
        try:
            placeholder = ','.join(['%s'] * len(detail_ids))
            conn = get_db_connection()
            if not conn:
                print("Database connection failed")
                return {}
                
            cur = conn.cursor(prepared=True)
            cur.execute(f"""
                SELECT ad.detail_id, first_name, last_name, date_of_birth, 
                       address, phone_number, application_role
                FROM ApplicantProfile ap 
                JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
                WHERE ad.detail_id IN ({placeholder})
            """, detail_ids)
            
            result = cur.fetchall()
            
            formatted_result = {}
            for row in result:
                detail_id = row[0]
                dob = row[4]
                dob_str = dob.strftime("%d %B %Y") if dob else "N/A"
                
                # Decrypt the encrypted fields
                first_name = self.encryptor.decrypt(row[1]) if row[1] else ""
                last_name = self.encryptor.decrypt(row[2]) if row[2] else ""
                # email = self.encryptor.decrypt(row[3]) if row[3] else ""
                address = self.encryptor.decrypt(row[4]) if row[4] else ""
                phone = self.encryptor.decrypt(row[5]) if row[5] else ""
                role = row[6] if row[6] else ""  # applicant_role is not encrypted

                formatted_result[detail_id] = {
                    "name": f"{first_name} {last_name}".strip(),
                    # "email": email,
                    "date_of_birth": dob_str,
                    "address": address,
                    "phone_number": phone,
                    "role": role
                }
            
            if cur:
                cur.close()
            if conn:
                conn.close()
                
            self.applicant_cache.update(formatted_result)
            return formatted_result
            
        except Exception as e:
            print(f"Error getting applicant data: {e}")
            return {}

    def extract_cv_content(self, cv_path: str, use_regex: bool = False) -> str:
        try:
            if not os.path.isabs(cv_path):
                possible_roots = [
                    project_root,
                    project_root.parent,
                    Path.cwd()
                ]
                
                full_path = None
                for root in possible_roots:
                    test_path = root / cv_path
                    if test_path.exists():
                        full_path = test_path
                        break
                
                if full_path is None:
                    print(f"CV file not found in any location: {cv_path}")
                    return f"CV file not found: {cv_path}"
            else:
                full_path = Path(cv_path)
            
            if not full_path.exists():
                print(f"CV file not found: {full_path}")
                return f"CV file not found: {cv_path}"
            
            try:
                content = extract_cv_content_direct(full_path, use_regex)
                return content
            except Exception as extract_error:
                print(f"Extraction failed, trying file-based extraction: {extract_error}")

        except Exception as e:
            print(f"Error extracting CV content from {cv_path}: {e}")
            return f"Error extracting CV: {str(e)}"

    def get_cv_database_for_search(self, use_regex: bool = False) -> dict:
        cv_paths = self.get_cv_paths()
        cv_database = {}
        
        if not cv_paths:
            print("No CV paths found in database")
            return {}
        
        print(f"Extracting content from {len(cv_paths)} CVs...")
        
        for cv_id, cv_path in cv_paths.items():
            cache_key = f"{cv_id}_{use_regex}"
            if cache_key in self.cv_cache:
                cv_database[cv_id] = self.cv_cache[cache_key]
                continue
            
            content = self.extract_cv_content(cv_path, use_regex)
            
            self.cv_cache[cache_key] = content
            cv_database[cv_id] = content
            
            # print(f"Extracted {cv_id}: {len(content)} characters")
        
        print(f"CV database ready with {len(cv_database)} CVs")
        return cv_database

    def get_applicant_summary_data(self, detail_id: int) -> dict:
        applicant_data = self.get_applicant_data([detail_id])
        
        if detail_id not in applicant_data:
            return self.get_fallback_summary_data()
        
        data = applicant_data[detail_id]
        
        if detail_id in self.skills_cache:
            return self.skills_cache[detail_id]
        
        cv_paths = self.get_cv_paths()
        cv_id = f"cv_{detail_id}"
        
        if cv_id not in cv_paths:
            return []
        
        info_groups = self.extract_cv_content_and_process(cv_paths[cv_id], use_regex=True)
        
        print("DEBUG: get info groups done")
        print(info_groups)
        
        skills = info_groups['skill']
        job_history = info_groups['experience']
        education = info_groups['education']
        
        formatted_data = {
            "name": data["name"],
            "birthdate": data["date_of_birth"],
            "address": data["address"],
            "phone": data["phone_number"],
            # "email": data["email"],
            "role": data["role"],
            "skills": skills,
            "job_history": job_history,
            "education": education
        }
        
        print(formatted_data)
        
        return formatted_data

    def extract_cv_content_and_process(self, cv_path: str, use_regex: bool = False) -> dict:
        try:
            content = self.extract_cv_content(cv_path, use_regex)
            
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_filename = temp_file.name
            
            try:
                info_groups = extract_information_group(temp_filename)
                return info_groups
            finally:
                import os
                try:
                    os.unlink(temp_filename)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error processing CV content: {e}")
            return {}

    def get_default_job_history(self) -> list:
        return [
            {
                "title": "Software Engineer",
                "period": "2020 - Present",
                "description": "Developed and maintained software applications using modern technologies."
            }
        ]

    def get_default_education(self) -> list:
        return [
            {
                "degree": "Bachelor of Computer Science",
                "period": "2016 - 2020"
            }
        ]

    def get_cv_file_path(self, detail_id: int) -> str:
        cv_paths = self.get_cv_paths()
        cv_id = f"cv_{detail_id}"
        return cv_paths.get(cv_id)

    def get_fallback_summary_data(self) -> dict:
        return {
            "name": "Applicant",
            "birthdate": "N/A",
            "address": "N/A",
            "phone": "N/A",
            # "email": "N/A",
            "role": "N/A",
            "skills": ["Technical Skills"],
            "job_history": self.get_default_job_history(),
            "education": self.get_default_education()
        }

    def clear_cache(self):
        self.cv_cache.clear()
        self.applicant_cache.clear()
        self.skills_cache.clear()
        print("Cache cleared")

cv_data_manager = CVDataManager()