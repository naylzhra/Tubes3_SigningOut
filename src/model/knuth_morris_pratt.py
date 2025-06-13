def knuth_morris_pratt(data: str, keyword: list) -> dict:
    result = {}
    data_lower = data.lower()
    
    for word in keyword:
        if not word:  
            continue
            
        word_lower = word.lower().strip()
        if not word_lower:
            continue
            
        occurrences = kmp_search(data_lower, word_lower)
        result[word] = len(occurrences)
        
    return result

def knuth_morris_pratt_with_cv_info(cv_database: dict, keyword: list) -> dict:
    results = {
        "matches": {},  
        "cv_scores": {},  
        "keyword_positions": {},  
        "ranked_cvs": [],  
        "search_summary": {
            "total_cvs_searched": len(cv_database),
            "keywords_searched": keyword,
            "cvs_with_matches": 0
        }
    }
    
    keywords_lower = [kw.lower().strip() for kw in keyword if kw.strip()]
    
    for cv_id, cv_content in cv_database.items():
        cv_content_lower = cv_content.lower()
        cv_matches = {}
        cv_positions = {}
        total_score = 0
        
        for word in keywords_lower:
            if not word:
                continue
            
            positions = kmp_search(cv_content_lower, word)
            count = len(positions)
            
            original_word = next((kw for kw in keyword if kw.lower().strip() == word), word)
            cv_matches[original_word] = count
            cv_positions[original_word] = positions
            total_score += count
        
        results["matches"][cv_id] = cv_matches
        results["cv_scores"][cv_id] = total_score
        results["keyword_positions"][cv_id] = cv_positions
        
        if total_score > 0:
            results["search_summary"]["cvs_with_matches"] += 1
    
    ranked_cvs = sorted(
        results["cv_scores"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    results["ranked_cvs"] = ranked_cvs
    
    return results

def search_cvs_with_details(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    search_results = knuth_morris_pratt_with_cv_info(cv_database, keywords)
    detailed_results = []
    
    for cv_id, score in search_results["ranked_cvs"][:top_n]:
        if score == 0:
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
        
        for keyword, count in search_results["matches"][cv_id].items():
            if count > 0:
                positions = search_results["keyword_positions"][cv_id][keyword]
                cv_result["match_summary"].append({
                    "keyword": keyword,
                    "count": count,
                    "positions": positions[:3]  # Tunjukkan 3 yang sama
                })
        
        detailed_results.append(cv_result)

    return detailed_results

def build_bf_array(pattern: str) -> list:
    length = 0  
    bf = [0] * len(pattern)  
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            bf[i] = length
            i += 1
        else:
            if length != 0:
                length = bf[length - 1]
            else:
                bf[i] = 0
                i += 1
    
    return bf

def kmp_search(text: str, pattern: str) -> list:
    if not pattern or not text:
        return []
    
    matches = []
    n = len(text)
    m = len(pattern)
    
    # Border Function (bp)
    bf = build_bf_array(pattern)
    
    i = 0  # index untuk text
    j = 0  # index untuk pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            matches.append(i - j)  
            j = bf[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = bf[j - 1]
            else:
                i += 1
    
    return matches
