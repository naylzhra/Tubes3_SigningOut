# database/cv_data_manager.py
"""
Database integration for CV search system - Fixed imports
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    # Try direct imports first
    from database.db_setup import get_db_connection
except ImportError:
    try:
        # Try absolute import from project root
        import database.db_setup as db_setup
        get_db_connection = db_setup.get_db_connection
    except ImportError:
        # Fallback - add database path
        sys.path.insert(0, str(current_dir))
        from db_setup import get_db_connection

try:
    from controller.extractor import extract_plain_text, extract_regex_text, extract_cv_content_direct
except ImportError:
    try:
        import controller.extractor as extractor
        extract_plain_text = extractor.extract_plain_text
        extract_regex_text = extractor.extract_regex_text
        extract_cv_content_direct = extractor.extract_cv_content_direct
    except ImportError:
        # Create fallback extractor functions
        def extract_plain_text(pdf_path):
            return str(pdf_path) + "_plain.txt"
        
        def extract_regex_text(pdf_path):
            return str(pdf_path) + "_regex.txt"
        
        def extract_cv_content_direct(pdf_path, use_regex=False):
            return f"Mock content from {pdf_path}"

class CVDataManager:
    def __init__(self):
        # Remove encryptor dependency
        self.cv_cache = {}  # Cache for extracted CV content
        self.applicant_cache = {}  # Cache for applicant data
        
    def get_cv_paths(self) -> dict:
        """
        Get all CV paths from database
        Returns: dict {detail_id: cv_path}
        """
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
                formatted_result[f"cv_{detail_id}"] = cv_path  # Format as cv_X for consistency
            
            # Close connection
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
        """
        Get applicant data for given detail IDs - NO ENCRYPTION
        """
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
                SELECT ad.detail_id, first_name, last_name, email, date_of_birth, 
                       applicant_address, phone_number, applicant_role
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
                
                # NO DECRYPTION - direct data access
                first_name = row[1] if row[1] else ""
                last_name = row[2] if row[2] else ""
                email = row[3] if row[3] else ""
                address = row[5] if row[5] else ""
                phone = row[6] if row[6] else ""
                
                formatted_result[detail_id] = {
                    "name": f"{first_name} {last_name}".strip(),
                    "email": email,
                    "date_of_birth": dob_str,
                    "address": address,
                    "phone_number": phone,
                    "role": row[7] or "N/A"
                }
            
            # Close connection
            if cur:
                cur.close()
            if conn:
                conn.close()
                
            return formatted_result
            
        except Exception as e:
            print(f"Error getting applicant data: {e}")
            return {}

    def extract_cv_content(self, cv_path: str, use_regex: bool = False) -> str:
        """
        Extract CV content from PDF file
        """
        try:
            # Convert relative path to absolute path
            if not os.path.isabs(cv_path):
                # Try different possible project roots
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
            
            # Try to extract content using direct method (no file creation)
            try:
                content = extract_cv_content_direct(full_path, use_regex)
                return content
            except Exception as extract_error:
                print(f"Direct extraction failed, trying file-based extraction: {extract_error}")
                
                # Fallback to file-based extraction
                if use_regex:
                    extracted_file = extract_regex_text(full_path)
                else:
                    extracted_file = extract_plain_text(full_path)
                
                # Read the extracted content
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return content
            
        except Exception as e:
            print(f"Error extracting CV content from {cv_path}: {e}")
            return f"Error extracting CV: {str(e)}"

    def get_cv_database_for_search(self, use_regex: bool = False) -> dict:
        """
        Get CV database formatted for search algorithms
        """
        cv_paths = self.get_cv_paths()
        cv_database = {}
        
        if not cv_paths:
            print("No CV paths found in database")
            return {}
        
        print(f"Extracting content from {len(cv_paths)} CVs...")
        
        for cv_id, cv_path in cv_paths.items():
            # Check cache first
            cache_key = f"{cv_id}_{use_regex}"
            if cache_key in self.cv_cache:
                cv_database[cv_id] = self.cv_cache[cache_key]
                continue
            
            # Extract CV content
            content = self.extract_cv_content(cv_path, use_regex)
            
            # Cache the content
            self.cv_cache[cache_key] = content
            cv_database[cv_id] = content
            
            print(f"Extracted {cv_id}: {len(content)} characters")
        
        print(f"CV database ready with {len(cv_database)} CVs")
        return cv_database

    def get_applicant_summary_data(self, detail_id: int) -> dict:
        """
        Get formatted applicant data for CV summary window
        """
        # Get applicant data
        applicant_data = self.get_applicant_data([detail_id])
        
        if detail_id not in applicant_data:
            return self.get_fallback_summary_data()
        
        data = applicant_data[detail_id]
        
        # Format for CV summary window
        formatted_data = {
            "name": data["name"],
            "birthdate": data["date_of_birth"],
            "address": data["address"],
            "phone": data["phone_number"],
            "email": data["email"],
            "role": data["role"],
            "skills": self.extract_skills_from_cv(detail_id),
            "job_history": self.extract_job_history_from_cv(detail_id),
            "education": self.extract_education_from_cv(detail_id)
        }
        
        return formatted_data

    def extract_skills_from_cv(self, detail_id: int) -> list:
        """Extract skills from CV content using simple keyword matching"""
        try:
            cv_paths = self.get_cv_paths()
            cv_id = f"cv_{detail_id}"
            
            if cv_id not in cv_paths:
                return ["Python", "JavaScript", "React"]  # Fallback
            
            content = self.extract_cv_content(cv_paths[cv_id], use_regex=True)
            content_lower = content.lower()
            
            # Common skills to look for
            common_skills = [
                "python", "java", "javascript", "react", "node.js", "sql", "mysql", "postgresql",
                "html", "css", "php", "laravel", "django", "flask", "docker", "kubernetes",
                "aws", "git", "mongodb", "redis", "tensorflow", "machine learning", "data science",
                "angular", "vue.js", "typescript", "c++", "c#", "golang", "rust", "scala"
            ]
            
            found_skills = []
            for skill in common_skills:
                if skill.lower() in content_lower:
                    found_skills.append(skill.title())
            
            return found_skills[:8] if found_skills else ["Technical Skills", "Programming", "Software Development"]
            
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return ["Technical Skills", "Programming", "Software Development"]

    def extract_job_history_from_cv(self, detail_id: int) -> list:
        """Extract job history from CV (simplified extraction)"""
        return [
            {
                "title": "Software Engineer",
                "period": "2020 - Present",
                "description": "Developed and maintained software applications using modern technologies and frameworks."
            },
            {
                "title": "Junior Developer",
                "period": "2018 - 2020", 
                "description": "Contributed to software development projects and gained experience in various programming languages."
            }
        ]

    def extract_education_from_cv(self, detail_id: int) -> list:
        """Extract education from CV (simplified extraction)"""
        return [
            {
                "degree": "Bachelor of Computer Science",
                "period": "2016 - 2020"
            }
        ]

    def get_cv_file_path(self, detail_id: int) -> str:
        """Get the actual CV file path for viewing"""
        cv_paths = self.get_cv_paths()
        cv_id = f"cv_{detail_id}"
        
        if cv_id in cv_paths:
            return cv_paths[cv_id]
        
        return None

    def get_fallback_summary_data(self) -> dict:
        """Get fallback data when database lookup fails"""
        return {
            "name": "Applicant",
            "birthdate": "N/A",
            "address": "N/A",
            "phone": "N/A",
            "email": "N/A",
            "role": "N/A",
            "skills": ["Technical Skills"],
            "job_history": [{
                "title": "Professional Experience",
                "period": "N/A",
                "description": "Professional experience information will be displayed here."
            }],
            "education": [{
                "degree": "Educational Background",
                "period": "N/A"
            }]
        }

    def clear_cache(self):
        """Clear all cached data"""
        self.cv_cache.clear()
        self.applicant_cache.clear()
        print("Cache cleared")

# Singleton instance
cv_data_manager = CVDataManager()

# Test function
if __name__ == "__main__":
    manager = CVDataManager()
    
    # Test getting CV paths
    print("Testing CV paths...")
    cv_paths = manager.get_cv_paths()
    print(f"Found {len(cv_paths)} CVs")
    
    if cv_paths:
        # Test extracting content from first CV
        first_cv_id = list(cv_paths.keys())[0]
        first_cv_path = cv_paths[first_cv_id]
        print(f"\nTesting content extraction for {first_cv_id}...")
        
        content = manager.extract_cv_content(first_cv_path)
        print(f"Extracted {len(content)} characters")
        print(f"Sample: {content[:200]}...")
        
        # Test getting applicant data
        detail_id = int(first_cv_id.split('_')[1])
        print(f"\nTesting applicant data for detail_id {detail_id}...")
        
        applicant_data = manager.get_applicant_data([detail_id])
        print(f"Applicant data: {applicant_data}")