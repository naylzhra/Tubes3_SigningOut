def build_last_occurrence(pattern: str) -> dict:
    return {char: idx for idx, char in enumerate(pattern)}

def boyer_moore_search(text: str, pattern: str) -> list:
    n, m = len(text), len(pattern)
    if m == 0 or n == 0 or m > n:
        return []

    last = build_last_occurrence(pattern)
    matches = []
    s = 0

    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            matches.append(s)
            s += m - last.get(text[s + m], -1) if s + m < n else 1
        else:
            s += max(1, j - last.get(text[s + j], -1))
    return matches


def boyer_moore_with_cv_info(cv_database: dict, keyword: list) -> dict:
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

            positions = boyer_moore_search(cv_content_lower, word)
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

    results["ranked_cvs"] = sorted(
        results["cv_scores"].items(), key=lambda x: x[1], reverse=True
    )

    return results


def search_cvs_boyer_moore(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    search_results = boyer_moore_with_cv_info(cv_database, keywords)
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
