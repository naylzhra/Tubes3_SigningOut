# algorithm/boyer_moore.py
"""
Implementasi Algoritma Boyer-Moore untuk pencarian string yang efisien
"""

def build_last_occurrence(pattern: str) -> dict:
    """
    Build last occurrence table for Boyer-Moore algorithm
    
    Args:
        pattern (str): Pattern string
        
    Returns:
        dict: Dictionary mapping each character to its last occurrence index
    """
    return {char: idx for idx, char in enumerate(pattern)}

def boyer_moore_search(text: str, pattern: str) -> list:
    """
    Boyer-Moore string search algorithm implementation
    
    Args:
        text (str): Text to search in
        pattern (str): Pattern to search for
        
    Returns:
        list: List of starting indices where pattern is found
    """
    n, m = len(text), len(pattern)
    if m == 0 or n == 0 or m > n:
        return []

    last = build_last_occurrence(pattern)
    matches = []
    s = 0

    while s <= n - m:
        j = m - 1
        # Compare pattern from right to left
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            # Pattern found at position s
            matches.append(s)
            # Move to next possible position using last occurrence
            s += m - last.get(text[s + m], -1) if s + m < n else 1
        else:
            # Mismatch found, use bad character rule
            s += max(1, j - last.get(text[s + j], -1))
    
    return matches

def boyer_moore_search_keyword_list(text: str, keywords: list) -> dict:
    """
    Search for multiple keywords in text using Boyer-Moore algorithm
    
    Args:
        text (str): Text to search in
        keywords (list): List of keywords to search for
    
    Returns:
        dict: Dictionary with keyword as key and count as value
    """
    result = {}
    
    # Convert text to lowercase for case-insensitive search
    text_lower = text.lower()
    
    for keyword in keywords:
        if not keyword or not keyword.strip():
            continue
            
        keyword_lower = keyword.lower().strip()
        
        # Use Boyer-Moore algorithm to find all occurrences
        occurrences = boyer_moore_search(text_lower, keyword_lower)
        result[keyword] = len(occurrences)
        
        # Debug output
        print(f"Boyer-Moore - Keyword '{keyword}': {len(occurrences)} occurrences found")
        if occurrences:
            print(f"  Positions: {occurrences[:5]}{'...' if len(occurrences) > 5 else ''}")
    
    return result

def boyer_moore_with_cv_info(cv_database: dict, keywords: list) -> dict:
    """
    Enhanced Boyer-Moore implementation for multiple CV search
    
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
    keywords_lower = [kw.lower().strip() for kw in keywords if kw.strip()]

    for cv_id, cv_content in cv_database.items():
        cv_content_lower = cv_content.lower()
        cv_matches = {}
        cv_positions = {}
        total_score = 0

        for word in keywords_lower:
            if not word:
                continue

            # Find all occurrences using Boyer-Moore
            positions = boyer_moore_search(cv_content_lower, word)
            count = len(positions)

            # Store results with original keyword
            original_word = next((kw for kw in keywords if kw.lower().strip() == word), word)
            cv_matches[original_word] = count
            cv_positions[original_word] = positions
            total_score += count

        # Store CV results
        results["matches"][cv_id] = cv_matches
        results["cv_scores"][cv_id] = total_score
        results["keyword_positions"][cv_id] = cv_positions

        if total_score > 0:
            results["search_summary"]["cvs_with_matches"] += 1

    # Rank CVs by total score
    results["ranked_cvs"] = sorted(
        results["cv_scores"].items(), key=lambda x: x[1], reverse=True
    )

    return results

def search_cvs_boyer_moore(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    """
    Search CVs using Boyer-Moore algorithm and return detailed results for top N matches
    
    Args:
        cv_database (dict): Database CV {cv_id: content}
        keywords (list): Keywords to search
        top_n (int): Number of top results to return
    
    Returns:
        list: List of CV results with detailed match information
    """
    # Get search results
    search_results = boyer_moore_with_cv_info(cv_database, keywords)
    
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

# Data dummy (same as other algorithms for consistency)
DUMMY_CV_DATA = {
    "cv_1": """
    John Doe Software Engineer with 5 years of experience in python programming and web development. 
    Skilled in javascript, react, node.js, and database management using mysql and postgresql. 
    Experience working with python frameworks like django and flask. Proficient in git version control, 
    docker containerization, and aws cloud services. Strong background in algorithms and data structures. 
    Previously worked as a backend developer specializing in python and java programming languages. 
    Familiar with machine learning concepts and python libraries such as pandas, numpy, and scikit-learn. 
    Experience in agile development methodologies and team collaboration. Strong problem-solving skills 
    and ability to work in fast-paced environments. Bachelor's degree in Computer Science from MIT.
    """,
    
    "cv_2": """
    Sarah Johnson Frontend Developer with expertise in modern web technologies. Specialized in react 
    development, javascript programming, and responsive web design. Experience with html5, css3, and 
    modern css frameworks like bootstrap and tailwind. Proficient in state management using redux and 
    context api. Familiar with typescript for type-safe javascript development. Experience with build 
    tools like webpack, vite, and npm package management. Strong understanding of user interface design 
    principles and user experience optimization. Previously worked on react native mobile applications. 
    Bachelor's degree in Web Design and Development. Portfolio includes e-commerce sites and dashboard 
    applications built with react and javascript.
    """,
    
    "cv_3": """
    Michael Chen Data Scientist with strong background in machine learning and artificial intelligence. 
    Expert in python programming for data analysis using pandas, numpy, matplotlib, and seaborn. 
    Experience with machine learning frameworks including tensorflow, keras, pytorch, and scikit-learn. 
    Proficient in statistical analysis, data visualization, and predictive modeling. Strong background 
    in sql for database querying and data extraction. Experience with big data technologies like spark 
    and hadoop. Familiar with cloud platforms including aws and google cloud for ml model deployment. 
    PhD in Statistics from Stanford University. Previously worked on recommendation systems, natural 
    language processing, and computer vision projects using deep learning techniques.
    """,
    
    "cv_4": """
    Emily Rodriguez DevOps Engineer with expertise in cloud infrastructure and automation. Specialized 
    in aws cloud services including ec2, s3, lambda, and rds. Proficient in docker containerization 
    and kubernetes orchestration. Experience with infrastructure as code using terraform and cloudformation. 
    Strong background in ci/cd pipeline development using jenkins, gitlab ci, and github actions. 
    Familiar with monitoring tools like prometheus, grafana, and elk stack. Experience with linux 
    system administration and bash scripting. Previously worked with microservices architecture and 
    service mesh technologies. Bachelor's degree in Information Technology. Certified aws solutions 
    architect and certified kubernetes administrator.
    """,
    
    "cv_5": """
    David Wilson Full Stack Developer with comprehensive experience in both frontend and backend technologies. 
    Proficient in javascript, typescript, python, and java programming languages. Frontend expertise 
    includes react, vue.js, angular, and modern css frameworks. Backend experience with node.js, 
    express, django, and spring boot frameworks. Strong database skills including mysql, postgresql, 
    mongodb, and redis. Experience with rest api development and graphql. Familiar with testing 
    frameworks like jest, pytest, and selenium. Previously worked on e-commerce platforms, content 
    management systems, and real-time chat applications. Master's degree in Software Engineering. 
    Strong advocate for clean code practices and test-driven development methodologies.
    """,
    
    "cv_6": """
    Lisa Wang UI/UX Designer with passion for creating intuitive and beautiful user interfaces. 
    Expert in design tools including figma, adobe xd, sketch, and photoshop. Strong understanding 
    of user-centered design principles and usability testing methodologies. Experience with prototyping 
    and wireframing for web and mobile applications. Familiar with frontend technologies including 
    html, css, and basic javascript for design implementation. Previously worked on mobile app designs, 
    web application interfaces, and branding projects. Bachelor's degree in Graphic Design. Experience 
    with design systems, component libraries, and accessibility guidelines. Strong collaboration skills 
    working with development teams to implement pixel-perfect designs.
    """
}
