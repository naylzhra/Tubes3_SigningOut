# algorithm/kmp.py
"""
Implementasi Algoritma Knuth Morris Pratt
"""

def knuth_morris_pratt(data: str, keyword: list) -> dict:
    """
    Implementasi menerima data (long string) dan keyword (kata yang ingin dicari)
    Mengembalikan map dengan key = keyword yang ditemukan dan value = banyaknya occurence
    
    Args:
        data (str): String panjang tempat pencarian
        keyword (list): List kata kunci yang ingin dicari
    
    Returns:
        dict: Dictionary dengan key=keyword, value=jumlah kemunculan
    """
    result = {}
    
    # Convert data to lowercase for case-insensitive search
    data_lower = data.lower()
    
    for word in keyword:
        if not word:  # Skip empty keywords
            continue
            
        word_lower = word.lower().strip()
        if not word_lower:
            continue
            
        # Use KMP algorithm to find all occurrences
        occurrences = kmp_search(data_lower, word_lower)
        result[word] = len(occurrences)
        
        # Debug output
        print(f"Keyword '{word}': {len(occurrences)} occurrences found")
        if occurrences:
            print(f"  Positions: {occurrences[:5]}{'...' if len(occurrences) > 5 else ''}")
    
    return result

def knuth_morris_pratt_with_cv_info(cv_database: dict, keyword: list) -> dict:
    """
    Enhanced KMP implementation yang mencari di multiple CV dan mengembalikan info CV
    
    Args:
        cv_database (dict): Dictionary dengan key=cv_id, value=cv_content
        keyword (list): List kata kunci yang ingin dicari
    
    Returns:
        dict: Dictionary dengan informasi lengkap hasil pencarian
    """
    results = {
        "matches": {},  # {cv_id: {keyword: count}}
        "cv_scores": {},  # {cv_id: total_score}
        "keyword_positions": {},  # {cv_id: {keyword: [positions]}}
        "ranked_cvs": [],  # List CV diurutkan berdasarkan score
        "search_summary": {
            "total_cvs_searched": len(cv_database),
            "keywords_searched": keyword,
            "cvs_with_matches": 0
        }
    }
    
    # Convert keywords to lowercase
    keywords_lower = [kw.lower().strip() for kw in keyword if kw.strip()]
    
    for cv_id, cv_content in cv_database.items():
        cv_content_lower = cv_content.lower()
        cv_matches = {}
        cv_positions = {}
        total_score = 0
        
        for word in keywords_lower:
            if not word:
                continue
            
            # Find all occurrences using KMP
            positions = kmp_search(cv_content_lower, word)
            count = len(positions)
            
            # Store results
            original_word = next((kw for kw in keyword if kw.lower().strip() == word), word)
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
    ranked_cvs = sorted(
        results["cv_scores"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    results["ranked_cvs"] = ranked_cvs
    
    return results

def search_cvs_with_details(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    """
    Search CVs and return detailed results for top N matches
    
    Args:
        cv_database (dict): Database CV {cv_id: content}
        keywords (list): Keywords to search
        top_n (int): Number of top results to return
    
    Returns:
        list: List of CV results with detailed match information
    """
    # Get search results
    search_results = knuth_morris_pratt_with_cv_info(cv_database, keywords)
    
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

def build_lps_array(pattern: str) -> list:
    """
    Build Longest Proper Prefix which is also Suffix array for KMP algorithm
    
    Args:
        pattern (str): Pattern string
        
    Returns:
        list: LPS array
    """
    length = 0  # Length of the previous longest prefix suffix
    lps = [0] * len(pattern)  # LPS array
    i = 1
    
    # The loop calculates lps[i] for i = 1 to len(pattern)-1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text: str, pattern: str) -> list:
    """
    KMP Algorithm implementation untuk mencari semua kemunculan pattern dalam text
    
    Args:
        text (str): Text tempat pencarian
        pattern (str): Pattern yang dicari
        
    Returns:
        list: List of starting indices where pattern is found
    """
    if not pattern or not text:
        return []
    
    matches = []
    n = len(text)
    m = len(pattern)
    
    # Build LPS array
    lps = build_lps_array(pattern)
    
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            matches.append(i - j)  # Found a match
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return matches

# ========================= DATA DUMMY =========================

# Data dummy berupa string panjang yang menyimulasikan konten CV
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


# def interactive_cv_search():
#     try:
#         print("Available CVs:")
#         for cv_id in DUMMY_CV_DATA.keys():
#             # Extract name from CV content
#             content = DUMMY_CV_DATA[cv_id].strip()
#             name = ' '.join(content.split()[:2])
#             print(f"  • {cv_id}: {name}")
        
#         print("\nEnter keywords separated by commas:")
#         user_input = input("Keywords: ").strip()
        
#         if not user_input:
#             keywords = ["python", "javascript", "react"]  # Default
#             print(f"Using default keywords: {keywords}")
#         else:
#             keywords = [kw.strip() for kw in user_input.split(',') if kw.strip()]
        
#         print(f"\nSearching for: {keywords}")
        
#         # Get top N
#         try:
#             top_n_input = input("How many top results? (default 3): ").strip()
#             top_n = int(top_n_input) if top_n_input else 3
#         except ValueError:
#             top_n = 3
        
#         # Perform search
#         results = search_cvs_with_details(DUMMY_CV_DATA, keywords, top_n)
        
#         print(f"\nTop {len(results)} Results:")
        
#         for i, result in enumerate(results, 1):
#             print(f"\n{i}. CV: {result['cv_id']}")
#             print(f"   Score: {result['total_score']}")
#             print(f"   Matches: {dict(result['matches'])}")
            
#             # Show snippet with context
#             cv_content = DUMMY_CV_DATA[result['cv_id']]
#             snippet = cv_content[:150] + "..." if len(cv_content) > 150 else cv_content
#             print(f"   Preview: {snippet}")
        
#         if not results:
#             print(" No matching CVs found for these keywords.")
    
#     except KeyboardInterrupt:
#         print("\n Search interrupted by user.")
#     except Exception as e:
#         print(f"Error: {e}")

# # Test
# if __name__ == "__main__":
#     # Interactive search
#     interactive_cv_search()
