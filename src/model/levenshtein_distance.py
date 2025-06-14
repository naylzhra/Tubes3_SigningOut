'''
Implementasi Allgoritma Levenshtein Distance
'''

threshold = 0.8

def levenshtein_distance(data: list, keyword: list) -> dict:
    res = {key: 0 for key in keyword}
    for word in data:
        for key in keyword:
            dist = levenshtein_calculation(word.lower(), key.lower())
            if is_pass(word.lower(), key.lower(), dist):
                res[key] += 1
    return res

def is_pass(string1: str, string2: str, dist: int) -> bool:
    m = max(len(string1), len(string2))
    if m == 0:
        return True 
    sim = 1 - (dist / m)
    # panjang keyword kecil
    if len(string2) <= 4:
        return sim >= 0.75
    return sim > threshold

def levenshtein_calculation(string1: str, string2: str) -> int:
    m = max(len(string1), len(string2))
    n = min(len(string1), len(string2))
    longer = string1
    shorter = string2
    if m != len(string1):
        longer = string2
        shorter = string1

    # jika string1 or string2 is empty, maka ld = panjang string tidak kosong
    if m == 0:
        return n
    if n == 0:
        return m
    
    # membuat prev dan curr untuk mengecek perbedaan kedua string    
    prev = [i for i in range(m + 1)]
    curr = [0 for i in range(m + 1)]
    
    # iterate untuk setiap character di shorter string
    for j in range(1, n + 1):
        curr[0] = j
        # iterate untuk setiap character di longer string
        for k in range(1, m + 1):
            if longer[k - 1] == shorter[j - 1]:
                curr[k] = prev[k - 1]  # jika karakter sama, tidak ada biaya tambahan dari perhitungan sblmnya
            else:
                # cek minimum cost antara insert, remove, replace
                curr[k] = 1 + min(
                    curr[k - 1],  # insert, cek dari biaya sejauh ini (pake curr)
                    prev[k],      # remove, cek biaya dari prev untuk dpt cost sampai curr char (jika di-remove)
                    prev[k - 1]   # replace, cek dari biaya prev (pengecekan terakhir sblm curr char di-replace)
                )
        # Update prev dengan curr
        prev = curr.copy()
        
    # last index dari curr adalah nilai akhir levensh dist
    return curr[m]

def levenshtein_search_cv(cv_content: str, keywords: list) -> dict:
    words = cv_content.lower().replace('\n', ' ').split()
    
    clean_words = []
    for word in words:
        clean_word = ''.join(char for char in word if char.isalnum())
        if clean_word:
            clean_words.append(clean_word)
    
    result = levenshtein_distance(clean_words, keywords)
    
    return result

def levenshtein_search_with_cv_info(cv_database: dict, keywords: list) -> dict:
    results = {
        "matches": {},  
        "cv_scores": {},  
        "keyword_positions": {}, 
        "ranked_cvs": [],  
        "search_summary": {
            "total_cvs_searched": len(cv_database),
            "keywords_searched": keywords,
            "cvs_with_matches": 0
        }
    }
    
    keywords_clean = [kw.strip().lower() for kw in keywords if kw.strip()]
    
    for cv_id, cv_content in cv_database.items():
        cv_matches = levenshtein_search_cv(cv_content, keywords_clean)
        
        total_score = sum(cv_matches.values())
        
        results["matches"][cv_id] = cv_matches
        results["cv_scores"][cv_id] = total_score
        
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
    
    ranked_cvs = sorted(
        results["cv_scores"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    results["ranked_cvs"] = ranked_cvs
    
    return results

def search_cvs_with_levenshtein(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    search_results = levenshtein_search_with_cv_info(cv_database, keywords)
    
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
                    "positions": positions[:3]  
                })
        
        detailed_results.append(cv_result)
    
    return detailed_results

# driver
if __name__ == "__main__":
    with open('../../data/dummy.txt', 'r') as file:
        line = file.readline().strip()
        words = line.split(' ')
    
        keywords = ['kook', 'coos', 'computer']

        # Function call to calculate Levenshtein distance
        result = levenshtein_distance(words, keywords)
        print(result)