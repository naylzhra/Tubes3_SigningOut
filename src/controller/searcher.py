# controller/searcher.py
"""
Controller untuk menghubungkan KMP algorithm dengan UI
"""

from model.knuth_morris_pratt import (
    knuth_morris_pratt_with_cv_info, 
    search_cvs_with_details,
    DUMMY_CV_DATA
)
import time

class SearchController:
    def __init__(self):
        # Use dummy data from KMP module
        self.cv_database = DUMMY_CV_DATA
        print(f"SearchController initialized with {len(self.cv_database)} CVs")
    
    def search_cvs(self, keywords_str, algorithm="KMP", top_n=5):
        """
        Main search method yang dipanggil dari UI
        
        Args:
            keywords_str (str): String keywords yang dipisah koma atau spasi
            algorithm (str): Algorithm type (KMP, BM, Fuzzy)
            top_n (int): Number of top results to return
            
        Returns:
            dict: Formatted results untuk UI
        """
        start_time = time.time()
        
        # Parse keywords dari string input
        keywords = self.parse_keywords(keywords_str)
        
        if not keywords:
            return self.create_empty_result()
        
        # Untuk sekarang hanya implement KMP
        if algorithm == "KMP":
            results = self.search_with_kmp(keywords, top_n)
        else:
            # TODO: Implement BM and Fuzzy matching
            results = self.search_with_kmp(keywords, top_n)  # Fallback to KMP
        
        end_time = time.time()
        search_time_ms = round((end_time - start_time) * 1000, 2)
        
        # Format results untuk UI
        formatted_results = self.format_results_for_ui(results, search_time_ms, algorithm)
        
        return formatted_results
    
    def parse_keywords(self, keywords_str):
        """Parse keywords dari input string"""
        if not keywords_str or not keywords_str.strip():
            return []
        
        # Split by comma or space, clean whitespace
        keywords = []
        
        # Try comma first
        if ',' in keywords_str:
            keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        else:
            # Split by space
            keywords = [kw.strip() for kw in keywords_str.split() if kw.strip()]
        
        print(f"Parsed keywords: {keywords}")
        return keywords
    
    def search_with_kmp(self, keywords, top_n):
        """Search using KMP algorithm"""
        print(f"Searching with KMP for keywords: {keywords}")
        
        # Use the detailed search function from KMP module
        detailed_results = search_cvs_with_details(self.cv_database, keywords, top_n)
        
        return detailed_results
    
    def format_results_for_ui(self, search_results, search_time_ms, algorithm):
        """Format search results untuk ditampilkan di UI"""
        
        # Convert detailed results ke format yang dibutuhkan UI
        ui_results = []
        
        for result in search_results:
            cv_id = result["cv_id"]
            
            # Get CV name from the CV content (extract first line or use ID)
            cv_name = self.extract_name_from_cv(cv_id)
            
            # Format matched keywords dengan count
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
        
        # Create summary
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
        
        print(f"Search completed: {cvs_with_matches}/{total_cvs} CVs matched in {search_time_ms}ms")
        
        return formatted_response
    
    def extract_name_from_cv(self, cv_id):
        """Extract name from CV content"""
        cv_content = self.cv_database.get(cv_id, "")
        
        # Try to extract name from CV content
        lines = cv_content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('   ') and len(line.split()) <= 3:
                # Likely a name (first non-indented short line)
                words = line.split()
                if len(words) >= 2:
                    return f"{words[0]} {words[1]}"
        
        # Fallback: use CV ID
        return cv_id.replace('_', ' ').title()
    
    def create_empty_result(self):
        """Create empty result when no keywords provided"""
        return {
            "results": [],
            "summary": {
                "total_cvs_searched": len(self.cv_database),
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
        """Get full CV content by ID"""
        return self.cv_database.get(cv_id, "")
    
    def get_available_cvs(self):
        """Get list of available CV IDs"""
        return list(self.cv_database.keys())


# Untuk testing
if __name__ == "__main__":
    # Test the search controller
    controller = SearchController()
    
    # Test search
    test_keywords = "python, javascript, react"
    results = controller.search_cvs(test_keywords, "KMP", 3)
    
    print("\n=== SEARCH RESULTS ===")
    print(f"Summary: {results['summary']}")
    
    print("\nResults:")
    for i, result in enumerate(results['results'], 1):
        print(f"{i}. {result['name']} - {result['total_matches']} matches")
        for keyword in result['matched_keywords']:
            print(f"   {keyword}")