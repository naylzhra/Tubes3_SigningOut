# algorithm/levenshtein_distance.py
"""
Implementasi Algoritma Levenshtein Distance untuk pencarian fuzzy matching
"""

threshold = 0.5

def levenshtein_distance(data: list, keyword: list) -> dict:
    """
    Fuzzy matching using Levenshtein Distance
    
    Args:
        data (list): List of words from text
        keyword (list): List of keywords to search
    
    Returns:
        dict: Dictionary with keyword as key and count as value
    """
    res = {key: 0 for key in keyword}
    for word in data:
        for key in keyword:
            dist = levenshtein_calculation(word.lower(), key.lower())
            if is_pass(word.lower(), key.lower(), dist):
                res[key] += 1
    return res

def is_pass(string1: str, string2: str, dist: int) -> bool:
    """
    Check if similarity passes threshold
    
    Args:
        string1 (str): First string
        string2 (str): Second string
        dist (int): Levenshtein distance
    
    Returns:
        bool: True if similarity > threshold
    """
    m = max(len(string1), len(string2))
    if m == 0:
        return True  # Both strings are empty
    sim = 1 - (dist / m)
    return sim > threshold

def levenshtein_calculation(string1: str, string2: str) -> int:
    """
    Calculate Levenshtein distance between two strings
    
    Args:
        string1 (str): First string
        string2 (str): Second string
    
    Returns:
        int: Levenshtein distance
    """
    m = max(len(string1), len(string2))
    n = min(len(string1), len(string2))
    longer = string1
    shorter = string2
    if m != len(string1):
        longer = string2
        shorter = string1

    # If one string is empty, distance = length of non-empty string
    if m == 0:
        return n
    if n == 0:
        return m
    
    # Create prev and curr arrays for dynamic programming
    prev = [i for i in range(m + 1)]
    curr = [0 for i in range(m + 1)]
    
    # Iterate through each character in shorter string
    for j in range(1, n + 1):
        curr[0] = j
        # Iterate through each character in longer string
        for k in range(1, m + 1):
            if longer[k - 1] == shorter[j - 1]:
                curr[k] = prev[k - 1]  # No cost if characters match
            else:
                # Find minimum cost among insert, remove, replace
                curr[k] = 1 + min(
                    curr[k - 1],  # insert
                    prev[k],      # remove
                    prev[k - 1]   # replace
                )
        # Update prev with curr
        prev = curr.copy()
        
    # Last index of curr is the final Levenshtein distance
    return curr[m]

def levenshtein_search_cv(cv_content: str, keywords: list) -> dict:
    """
    Search CV content using Levenshtein distance
    
    Args:
        cv_content (str): CV content to search
        keywords (list): Keywords to search for
    
    Returns:
        dict: Dictionary with keyword matches and counts
    """
    # Split CV content into words
    words = cv_content.lower().replace('\n', ' ').split()
    
    # Clean words (remove punctuation)
    clean_words = []
    for word in words:
        clean_word = ''.join(char for char in word if char.isalnum())
        if clean_word:
            clean_words.append(clean_word)
    
    # Search using Levenshtein distance
    result = levenshtein_distance(clean_words, keywords)
    
    return result

def levenshtein_search_with_cv_info(cv_database: dict, keywords: list) -> dict:
    """
    Enhanced Levenshtein implementation for multiple CV search
    
    Args:
        cv_database (dict): Dictionary with key=cv_id, value=cv_content
        keywords (list): List of keywords to search for
    
    Returns:
        dict: Dictionary with comprehensive search information
    """
    results = {
        "matches": {},  # {cv_id: {keyword: count}}
        "cv_scores": {},  # {cv_id: total_score}
        "keyword_positions": {},  # {cv_id: {keyword: [positions]}}
        "ranked_cvs": [],  # List CV sorted by score
        "search_summary": {
            "total_cvs_searched": len(cv_database),
            "keywords_searched": keywords,
            "cvs_with_matches": 0
        }
    }
    
    # Clean keywords
    keywords_clean = [kw.strip().lower() for kw in keywords if kw.strip()]
    
    for cv_id, cv_content in cv_database.items():
        # Search using Levenshtein distance
        cv_matches = levenshtein_search_cv(cv_content, keywords_clean)
        
        # Calculate total score
        total_score = sum(cv_matches.values())
        
        # Store results
        results["matches"][cv_id] = cv_matches
        results["cv_scores"][cv_id] = total_score
        
        # Find approximate positions for matched keywords
        cv_positions = {}
        cv_content_lower = cv_content.lower()
        words = cv_content_lower.replace('\n', ' ').split()
        
        for keyword in keywords_clean:
            positions = []
            char_pos = 0
            
            for word_idx, word in enumerate(words):
                clean_word = ''.join(char for char in word if char.isalnum())
                if clean_word:
                    dist = levenshtein_calculation(clean_word, keyword)
                    if is_pass(clean_word, keyword, dist):
                        # Find character position in original text
                        word_start = cv_content_lower.find(word, char_pos)
                        if word_start != -1:
                            positions.append(word_start)
                        char_pos = word_start + len(word) if word_start != -1 else char_pos + len(word)
                    else:
                        char_pos += len(word) + 1  # +1 for space
            
            cv_positions[keyword] = positions
        
        results["keyword_positions"][cv_id] = cv_positions
        
        if total_score > 0:
            results["search_summary"]["cvs_with_matches"] += 1
    
    # Rank CVs by total score
    ranked_cvs = sorted(
        results["cv_scores"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    results["ranked_cvs"] = ranked_cvs
    
    return results

def search_cvs_with_levenshtein(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    """
    Search CVs using Levenshtein distance and return detailed results for top N matches
    
    Args:
        cv_database (dict): Database CV {cv_id: content}
        keywords (list): Keywords to search
        top_n (int): Number of top results to return
    
    Returns:
        list: List of CV results with detailed match information
    """
    # Get search results
    search_results = levenshtein_search_with_cv_info(cv_database, keywords)
    
    # Prepare detailed results
    detailed_results = []
    
    for cv_id, score in search_results["ranked_cvs"][:top_n]:
        if score == 0:  # Skip CVs with no matches
            continue
            
        cv_result = {
            "cv_id": cv_id,
            "total_score": score,
            "matches": search_results["matches"][cv_id],
            "keyword_positions": search_results["keyword_positions"][cv_id],
            "matched_keywords": [
                kw for kw, count in search_results["matches"][cv_id].items() 
                if count > 0
            ],
            "match_summary": []
        }
        
        # Create match summary
        for keyword, count in search_results["matches"][cv_id].items():
            if count > 0:
                positions = search_results["keyword_positions"][cv_id][keyword]
                cv_result["match_summary"].append({
                    "keyword": keyword,
                    "count": count,
                    "positions": positions[:3]  # Show first 3 positions
                })
        
        detailed_results.append(cv_result)
    
    return detailed_results