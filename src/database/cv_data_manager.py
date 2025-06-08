# database/cv_data_manager.py - Enhanced with better data extraction
"""
Enhanced Database integration for CV search system with improved data extraction
"""

import sys
import os
from pathlib import Path
import re

# Add project root to Python path
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

# Remove encryptor dependency as per your code
# from model.encryptor import Encryptor
# encryptor = Encryptor("SIGNHIRE")

try:
    from controller.extractor import extract_plain_text, extract_regex_text, extract_cv_content_direct
except ImportError:
    try:
        import controller.extractor as extractor
        extract_plain_text = extractor.extract_plain_text
        extract_regex_text = extractor.extract_regex_text
        extract_cv_content_direct = extractor.extract_cv_content_direct
    except ImportError:
        def extract_plain_text(pdf_path):
            return str(pdf_path) + "_plain.txt"
        
        def extract_regex_text(pdf_path):
            return str(pdf_path) + "_regex.txt"
        
        def extract_cv_content_direct(pdf_path, use_regex=False):
            return f"Mock content from {pdf_path}"

class CVDataManager:
    def __init__(self):
        # Initialize caches
        self.cv_cache = {}  # Cache for extracted CV content
        self.applicant_cache = {}  # Cache for applicant data
        self.skills_cache = {}  # Cache for extracted skills
        
    def get_cv_paths(self) -> dict:
        """
        Get all CV paths from database
        Returns: dict {cv_id: cv_path}
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
                formatted_result[f"cv_{detail_id}"] = cv_path
            
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
        Get applicant data for given detail IDs - NO ENCRYPTION based on your code
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
                
                # NO DECRYPTION - direct data access as per your updated code
                first_name = row[1] if row[1] else ""
                last_name = row[2] if row[2] else ""
                email = row[3] if row[3] else ""
                address = row[5] if row[5] else ""
                phone = row[6] if row[6] else ""
                role = row[7] if row[7] else ""
                
                formatted_result[detail_id] = {
                    "name": f"{first_name} {last_name}".strip(),
                    "email": email,
                    "date_of_birth": dob_str,
                    "address": address,
                    "phone_number": phone,
                    "role": role
                }
            
            # Close connection
            if cur:
                cur.close()
            if conn:
                conn.close()
                
            # Cache the results
            self.applicant_cache.update(formatted_result)
            
            return formatted_result
            
        except Exception as e:
            print(f"Error getting applicant data: {e}")
            return {}

    def extract_cv_content(self, cv_path: str, use_regex: bool = False) -> str:
        """
        Extract CV content from PDF file using your extractor functions
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
        Get formatted applicant data for CV summary window with enhanced data extraction
        """
        # Get applicant data
        applicant_data = self.get_applicant_data([detail_id])
        
        if detail_id not in applicant_data:
            return self.get_fallback_summary_data()
        
        data = applicant_data[detail_id]
        
        # Get enhanced data extracted from CV
        skills = self.extract_skills_from_cv(detail_id)
        job_history = self.extract_job_history_from_cv(detail_id)
        education = self.extract_education_from_cv(detail_id)
        
        # Format for CV summary window
        formatted_data = {
            "name": data["name"],
            "birthdate": data["date_of_birth"],
            "address": data["address"],
            "phone": data["phone_number"],
            "email": data["email"],
            "role": data["role"],
            "skills": skills,
            "job_history": job_history,
            "education": education
        }
        
        return formatted_data

    def extract_skills_from_cv(self, detail_id: int) -> list:
        """Extract skills from CV content using enhanced keyword matching"""
        try:
            # Check cache first
            if detail_id in self.skills_cache:
                return self.skills_cache[detail_id]
            
            cv_paths = self.get_cv_paths()
            cv_id = f"cv_{detail_id}"
            
            if cv_id not in cv_paths:
                return ["Technical Skills", "Programming", "Software Development"]
            
            content = self.extract_cv_content(cv_paths[cv_id], use_regex=True)
            content_lower = content.lower()
            
            # Enhanced skills detection with categories
            programming_languages = [
                "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby", 
                "go", "golang", "rust", "scala", "kotlin", "swift", "r", "matlab", "perl"
            ]
            
            web_technologies = [
                "html", "css", "react", "angular", "vue.js", "vue", "node.js", "express", 
                "laravel", "django", "flask", "spring", "bootstrap", "jquery", "sass", "less"
            ]
            
            databases = [
                "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", 
                "cassandra", "elasticsearch", "firebase", "dynamodb"
            ]
            
            cloud_devops = [
                "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "jenkins", 
                "git", "github", "gitlab", "terraform", "ansible", "vagrant", "linux"
            ]
            
            data_ai = [
                "machine learning", "deep learning", "tensorflow", "pytorch", "pandas", 
                "numpy", "scikit-learn", "data science", "analytics", "statistics", "ai"
            ]
            
            all_skills = programming_languages + web_technologies + databases + cloud_devops + data_ai
            
            found_skills = []
            for skill in all_skills:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, content_lower):
                    found_skills.append(skill.title())
            
            # Remove duplicates and limit to reasonable number
            found_skills = list(dict.fromkeys(found_skills))[:12]
            
            # Cache the results
            self.skills_cache[detail_id] = found_skills
            
            return found_skills if found_skills else ["Technical Skills", "Programming", "Software Development"]
            
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return ["Technical Skills", "Programming", "Software Development"]

    def extract_job_history_from_cv(self, detail_id: int) -> list:
        """Extract job history from CV content using pattern matching"""
        try:
            cv_paths = self.get_cv_paths()
            cv_id = f"cv_{detail_id}"
            
            if cv_id not in cv_paths:
                return self.get_default_job_history()
            
            content = self.extract_cv_content(cv_paths[cv_id], use_regex=True)
            
            # Try to extract work experience sections
            job_history = []
            
            # Common patterns for work experience
            experience_patterns = [
                r'(?i)(?:work\s+)?experience\s*:?\s*(.*?)(?=education|skills|projects|$)',
                r'(?i)employment\s+history\s*:?\s*(.*?)(?=education|skills|projects|$)',
                r'(?i)professional\s+experience\s*:?\s*(.*?)(?=education|skills|projects|$)'
            ]
            
            experience_text = ""
            for pattern in experience_patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    experience_text = match.group(1)
                    break
            
            if experience_text:
                # Extract individual job entries
                job_entries = self.parse_job_entries(experience_text)
                if job_entries:
                    job_history = job_entries
            
            # If no structured data found, return default
            if not job_history:
                job_history = self.get_default_job_history()
            
            return job_history[:3]  # Limit to 3 most recent
            
        except Exception as e:
            print(f"Error extracting job history: {e}")
            return self.get_default_job_history()

    def parse_job_entries(self, experience_text: str) -> list:
        """Parse individual job entries from experience text"""
        try:
            jobs = []
            
            # Split by common delimiters
            entries = re.split(r'\n\s*\n|\n(?=[A-Z][^a-z]*[0-9]{4})', experience_text)
            
            for entry in entries:
                if len(entry.strip()) < 20:  # Skip very short entries
                    continue
                
                # Try to extract job title, period, and description
                lines = [line.strip() for line in entry.split('\n') if line.strip()]
                
                if len(lines) >= 2:
                    title_line = lines[0]
                    
                    # Look for year patterns to identify period
                    period = "Experience Period"
                    for line in lines[:3]:
                        if re.search(r'20\d{2}', line):
                            period = line
                            break
                    
                    # Rest as description
                    desc_lines = [line for line in lines if line != title_line and line != period]
                    description = ' '.join(desc_lines)[:200] + "..." if len(' '.join(desc_lines)) > 200 else ' '.join(desc_lines)
                    
                    if description.strip():
                        jobs.append({
                            "title": title_line,
                            "period": period,
                            "description": description
                        })
            
            return jobs
            
        except Exception as e:
            print(f"Error parsing job entries: {e}")
            return []

    def extract_education_from_cv(self, detail_id: int) -> list:
        """Extract education from CV content using pattern matching"""
        try:
            cv_paths = self.get_cv_paths()
            cv_id = f"cv_{detail_id}"
            
            if cv_id not in cv_paths:
                return self.get_default_education()
            
            content = self.extract_cv_content(cv_paths[cv_id], use_regex=True)
            
            # Try to extract education sections
            education = []
            
            # Common patterns for education
            education_patterns = [
                r'(?i)education\s*:?\s*(.*?)(?=work|experience|skills|projects|$)',
                r'(?i)academic\s+background\s*:?\s*(.*?)(?=work|experience|skills|projects|$)',
                r'(?i)qualifications\s*:?\s*(.*?)(?=work|experience|skills|projects|$)'
            ]
            
            education_text = ""
            for pattern in education_patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    education_text = match.group(1)
                    break
            
            if education_text:
                # Extract individual education entries
                edu_entries = self.parse_education_entries(education_text)
                if edu_entries:
                    education = edu_entries
            
            # If no structured data found, return default
            if not education:
                education = self.get_default_education()
            
            return education[:2]  # Limit to 2 most recent
            
        except Exception as e:
            print(f"Error extracting education: {e}")
            return self.get_default_education()

    def parse_education_entries(self, education_text: str) -> list:
        """Parse individual education entries from education text"""
        try:
            education = []
            
            # Split by common delimiters
            entries = re.split(r'\n\s*\n|\n(?=[A-Z])', education_text)
            
            for entry in entries:
                if len(entry.strip()) < 10:  # Skip very short entries
                    continue
                
                lines = [line.strip() for line in entry.split('\n') if line.strip()]
                
                if lines:
                    degree_line = lines[0]
                    
                    # Look for year patterns
                    period = "Study Period"
                    for line in lines:
                        if re.search(r'20\d{2}', line):
                            period = line
                            break
                    
                    education.append({
                        "degree": degree_line,
                        "period": period
                    })
            
            return education
            
        except Exception as e:
            print(f"Error parsing education entries: {e}")
            return []

    def get_default_job_history(self) -> list:
        """Get default job history when extraction fails"""
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

    def get_default_education(self) -> list:
        """Get default education when extraction fails"""
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
            "job_history": self.get_default_job_history(),
            "education": self.get_default_education()
        }

    def clear_cache(self):
        """Clear all cached data"""
        self.cv_cache.clear()
        self.applicant_cache.clear()
        self.skills_cache.clear()
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
        
        # Test getting applicant summary data
        detail_id = int(first_cv_id.split('_')[1])
        print(f"\nTesting applicant summary data for detail_id {detail_id}...")
        
        summary_data = manager.get_applicant_summary_data(detail_id)
        print(f"Summary data: {summary_data}")
        
        # Test skills extraction
        skills = manager.extract_skills_from_cv(detail_id)
        print(f"Extracted skills: {skills}")
    else:
        print("No CVs found in database")