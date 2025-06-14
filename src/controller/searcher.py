import sys
import os
from pathlib import Path
import time

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    from model.knuth_morris_pratt import search_cvs_with_details as search_cvs_with_kmp
except ImportError as e:
    print(f"Warning: Could not import KMP algorithm: {e}")
    search_cvs_with_kmp = None

try:
    from model.aho_corasick import search_cvs_with_aho_corasick
except ImportError as e:
    print(f"Warning: Could not import Aho-Corasick algorithm: {e}")
    search_cvs_with_aho_corasick = None

try:
    from model.boyer_moore import search_cvs_boyer_moore
except ImportError as e:
    print(f"Warning: Could not import Boyer-Moore algorithm: {e}")
    search_cvs_boyer_moore = None

try:
    from model.levenshtein_distance import search_cvs_with_levenshtein
except ImportError as e:
    print(f"Warning: Could not import Levenshtein algorithm: {e}")
    search_cvs_with_levenshtein = None

try:
    from database.cv_data_manager import cv_data_manager
except ImportError as e:
    print(f"Warning: Could not import CV data manager: {e}")
    cv_data_manager = None

class SearchController:
    def __init__(self):
        self.cv_data_manager = cv_data_manager
        self.cv_database = {}
        self.applicant_data_cache = {}
        
        if self.cv_data_manager:
            self._initialize_cv_database()
        else:
            print("CV Data Manager not available - using empty database")
            
    def _initialize_cv_database(self):
        try:
            print("Initializing CV database from database...")
            self.cv_database = self.cv_data_manager.get_cv_database_for_search(use_regex=False)
            print(f"SearchController initialized with {len(self.cv_database)} CVs from database")
            
            if self.cv_database:
                detail_ids = [int(cv_id.split('_')[1]) for cv_id in self.cv_database.keys()]
                self.applicant_data_cache = self.cv_data_manager.get_applicant_data(detail_ids)
                print(f"Loaded applicant data for {len(self.applicant_data_cache)} applicants")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            self.cv_database = {}
            self.applicant_data_cache = {}
    
    def search_cvs(self, keywords_str, algorithm="KMP", top_n=5):
        start_time = time.time()
        
        keywords = self.parse_keywords(keywords_str)
        
        if not keywords or not self.cv_database:
            return self.create_empty_result()
        
        results = []
        
        if algorithm == "KMP" and search_cvs_with_kmp:
            results = search_cvs_with_kmp(self.cv_database, keywords, top_n)
        elif algorithm == "BM" and search_cvs_boyer_moore:
            results = search_cvs_boyer_moore(self.cv_database, keywords, top_n)
        elif algorithm == "Aho-Corasick" and search_cvs_with_aho_corasick:
            results = search_cvs_with_aho_corasick(self.cv_database, keywords, top_n)
        elif algorithm == "Levenshtein" and search_cvs_with_levenshtein:
            results = search_cvs_with_levenshtein(self.cv_database, keywords, top_n)
        else:
            if search_cvs_with_kmp:
                results = search_cvs_with_kmp(self.cv_database, keywords, top_n)
                algorithm = "KMP (fallback)"
            else:
                return self.create_empty_result()
        
        # Try Levenshtein as fallback if no results
        if len(results) == 0 and algorithm != "Levenshtein" and search_cvs_with_levenshtein:
            print(f"No results found with {algorithm}, trying Levenshtein distance as fallback...")
            results = search_cvs_with_levenshtein(self.cv_database, keywords, top_n)
            algorithm = f"{algorithm} → Levenshtein"
        
        end_time = time.time()
        search_time_ms = round((end_time - start_time) * 1000, 2)
        
        return self.format_results_for_ui(results, search_time_ms, algorithm)
    
    def parse_keywords(self, keywords_str):
        if not keywords_str or not keywords_str.strip():
            return []
        
        # Parse comma-separated or space-separated keywords
        if ',' in keywords_str:
            keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        else:
            keywords = [kw.strip() for kw in keywords_str.split() if kw.strip()]
        
        print(f"Parsed keywords: {keywords}")
        return keywords
    
    def format_results_for_ui(self, search_results, search_time_ms, algorithm):
        ui_results = []
        
        for result in search_results:
            cv_id = result["cv_id"]
            cv_name = self.get_applicant_name_from_database(cv_id)
            
            matched_keywords_formatted = []
            for match_info in result["match_summary"]:
                keyword = match_info["keyword"]
                count = match_info["count"]
                matched_keywords_formatted.append(f"• {keyword} ({count})")
            
            ui_result = {
                "cv_id": cv_id,
                "name": cv_name,
                "total_matches": result["total_score"],
                "matched_keywords": matched_keywords_formatted,
                "match_details": result["matches"],
                "positions": result["keyword_positions"]
            }
            
            ui_results.append(ui_result)
        
        total_cvs = len(self.cv_database)
        cvs_with_matches = len([r for r in search_results if r["total_score"] > 0])
        
        formatted_response = {
            "results": ui_results,
            "summary": {
                "total_cvs_searched": total_cvs,
                "cvs_with_matches": cvs_with_matches,
                "search_time_ms": search_time_ms,
                "algorithm_used": algorithm,
                "keywords_searched": len(search_results[0]["matches"].keys()) if search_results else 0
            },
            "timing": {
                "search_time_ms": search_time_ms
            }
        }
        
        print(f"Search completed: {cvs_with_matches}/{total_cvs} CVs matched in {search_time_ms}ms using {algorithm}")
        return formatted_response
    
    def get_applicant_name_from_database(self, cv_id):
        try:
            detail_id = int(cv_id.split('_')[1])
            
            if detail_id in self.applicant_data_cache:
                return self.applicant_data_cache[detail_id]["name"]
            
            if self.cv_data_manager:
                applicant_data = self.cv_data_manager.get_applicant_data([detail_id])
                if detail_id in applicant_data:
                    return applicant_data[detail_id]["name"]
            
            return f"Applicant {detail_id}"
            
        except Exception as e:
            print(f"Error getting applicant name for {cv_id}: {e}")
            return cv_id.replace('_', ' ').title()
    
    def create_empty_result(self):
        total_cvs = len(self.cv_database) if self.cv_database else 0
        return {
            "results": [],
            "summary": {
                "total_cvs_searched": total_cvs,
                "cvs_with_matches": 0,
                "search_time_ms": 0,
                "algorithm_used": "KMP",
                "keywords_searched": 0
            },
            "timing": {
                "search_time_ms": 0
            }
        }
    
    def get_cv_content(self, cv_id):
        if cv_id in self.cv_database:
            return self.cv_database[cv_id]
        return "CV content not available"
    
    def get_applicant_summary_data(self, detail_id):
        try:
            if self.cv_data_manager:
                summary_data = self.cv_data_manager.get_applicant_summary_data(detail_id)
                    
                print(f"Retrieved summary data for detail_id {detail_id}: {summary_data['name']}")
                
                return summary_data
            else:
                return self.get_fallback_summary_data()
            
        except Exception as e:
            print(f"Error getting summary data for detail_id {detail_id}: {e}")
            return self.get_fallback_summary_data()
    
    def get_fallback_summary_data(self):
        return {
            "name": "Applicant",
            "birthdate": "N/A",
            "address": "N/A", 
            "phone": "N/A",
            "email": "N/A",
            "role": "N/A",
            "skills": ["None"],
            "job_history": [{
                "role": "Applicant Role",
                "year": "N/A",
                "company": "Applicant Company"
            }],
            "education": [{
                "degree": "Educational Background",
                "year": "N/A",
                "institution": "Applicant Institution"
            }]
        }
    
    def get_cv_file_path(self, cv_id):
        try:
            detail_id = int(cv_id.split('_')[1])
            if self.cv_data_manager:
                return self.cv_data_manager.get_cv_file_path(detail_id)
            return None
        except Exception as e:
            print(f"Error getting CV file path for {cv_id}: {e}")
            return None
    
    def refresh_database(self):
        print("Refreshing CV database...")
        if self.cv_data_manager:
            self.cv_data_manager.clear_cache()
            self._initialize_cv_database()
    
    def get_cv_summary_by_id(self, cv_id):
        try:
            detail_id = int(cv_id.split('_')[1]) if cv_id.startswith('cv_') else int(cv_id)
            return self.get_applicant_summary_data(detail_id)
        except Exception as e:
            print(f"Error getting CV summary for {cv_id}: {e}")
            return self.get_fallback_summary_data()
    
    def get_search_statistics(self):
        return {
            "total_cvs": len(self.cv_database),
            "cached_applicants": len(self.applicant_data_cache),
            "available_algorithms": {
                "KMP": search_cvs_with_kmp is not None,
                "Boyer-Moore": search_cvs_boyer_moore is not None,
                "Aho-Corasick": search_cvs_with_aho_corasick is not None,
                "Levenshtein": search_cvs_with_levenshtein is not None
            }
        }