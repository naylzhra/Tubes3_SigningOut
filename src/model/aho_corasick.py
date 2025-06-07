# algorithm/aho_corasick.py
"""
Implementasi Algoritma Aho Corasick dengan integrasi untuk pencarian CV
"""

from collections import defaultdict, deque

class AhoCorasick:
    def __init__(self):
        self.trie = {}
        self.failure = {}
        self.output = defaultdict(list)
        self.keywords = []
    
    def add_keyword(self, keyword):
        # create trie (keyword tree)
        node = self.trie
        for char in keyword:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True  # end of word
        self.keywords.append(keyword)
    
    def build_failure_function(self):
        # the failure function for the automaton
        queue = deque()
        
        # initialize failure function for first level
        for char in self.trie:
            if char != '$':
                self.failure[id(self.trie[char])] = id(self.trie)
                queue.append((self.trie[char], char))
        
        # build failure function for remaining levels
        while queue:
            current_node, current_char = queue.popleft()
            current_id = id(current_node)
            
            for char in current_node:
                if char == '$':
                    continue
                    
                child_node = current_node[char]
                child_id = id(child_node)
                queue.append((child_node, char))
                
                # Find failure link
                failure_node_id = self.failure[current_id]
                failure_node = self._get_node_by_id(failure_node_id)
                
                while failure_node_id != id(self.trie) and char not in failure_node:
                    failure_node_id = self.failure[failure_node_id]
                    failure_node = self._get_node_by_id(failure_node_id)
                
                if char in failure_node and failure_node[char] is not child_node:
                    self.failure[child_id] = id(failure_node[char])
                else:
                    self.failure[child_id] = id(self.trie)
                
                # Build output function
                failure_target_id = self.failure[child_id]
                if failure_target_id in self.output:
                    self.output[child_id].extend(self.output[failure_target_id])
    
    def _get_node_by_id(self, node_id):   
        if node_id == id(self.trie):
            return self.trie
        
        def find_node(node, target_id):
            if id(node) == target_id:
                return node
            for key, child in node.items():
                if key != '$' and isinstance(child, dict):
                    result = find_node(child, target_id)
                    if result:
                        return result
            return None
        
        return find_node(self.trie, node_id)
    
    def _get_matches_at_node(self, node):
        matches = []
        node_id = id(node)
        
        if '$' in node:
            # Find the pattern that ends at this node
            pattern = self._reconstruct_pattern(node)
            if pattern:
                matches.append(pattern)
        
        if node_id in self.output:
            matches.extend(self.output[node_id])
        
        return matches
    
    def _reconstruct_pattern(self, target_node):
        # reconstruct pattern from root to target node
        def dfs(node, path, target_id):
            if id(node) == target_id:
                return path
            
            for char, child in node.items():
                if char != '$' and isinstance(child, dict):
                    result = dfs(child, path + char, target_id)
                    if result:
                        return result
            return None
        
        return dfs(self.trie, "", id(target_node))
    
    def search(self, text):
        if not self.keywords:
            return {}
        
        # build the automaton if not already built
        if not self.failure:
            self.build_failure_function()
        
        result_counts = {keyword: 0 for keyword in self.keywords}
        current_node = self.trie
        
        for i, char in enumerate(text):
            # follow failure links until we find a match or reach root
            while current_node is not self.trie and char not in current_node:
                current_node_id = id(current_node)
                if current_node_id in self.failure:
                    current_node = self._get_node_by_id(self.failure[current_node_id])
                else:
                    current_node = self.trie
            
            # move to next state if possible
            if char in current_node:
                current_node = current_node[char]
                
                # check for matches at current position
                matches = self._get_matches_at_node(current_node)
                for match in matches:
                    if match in result_counts:
                        result_counts[match] += 1
        
        return result_counts

def aho_corasick_search(text: str, keywords: list) -> dict:
    """
    Search for multiple keywords in text using Aho-Corasick algorithm
    
    Args:
        text (str): Text to search in
        keywords (list): List of keywords to search for
    
    Returns:
        dict: Dictionary with keyword as key and count as value
    """
    ac = AhoCorasick()
    
    # Convert to lowercase for case-insensitive search
    text_lower = text.lower()
    keywords_lower = [kw.lower().strip() for kw in keywords if kw.strip()]
    
    for keyword in keywords_lower:
        ac.add_keyword(keyword)
    
    result = ac.search(text_lower)
    
    # Map back to original keywords
    final_result = {}
    for i, original_keyword in enumerate(keywords):
        if i < len(keywords_lower):
            lower_keyword = keywords_lower[i]
            final_result[original_keyword] = result.get(lower_keyword, 0)
    
    return final_result

def aho_corasick_search_with_cv_info(cv_database: dict, keywords: list) -> dict:
    """
    Enhanced Aho-Corasick implementation for multiple CV search
    
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
    keywords_clean = [kw.strip() for kw in keywords if kw.strip()]
    
    for cv_id, cv_content in cv_database.items():
        # Search using Aho-Corasick
        cv_matches = aho_corasick_search(cv_content, keywords_clean)
        
        # Calculate total score
        total_score = sum(cv_matches.values())
        
        # Store results
        results["matches"][cv_id] = cv_matches
        results["cv_scores"][cv_id] = total_score
        
        # For Aho-Corasick, we'll find positions separately for each keyword
        cv_positions = {}
        cv_content_lower = cv_content.lower()
        
        for keyword in keywords_clean:
            keyword_lower = keyword.lower()
            positions = []
            start = 0
            while True:
                pos = cv_content_lower.find(keyword_lower, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
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

def search_cvs_with_aho_corasick(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    """
    Search CVs using Aho-Corasick and return detailed results for top N matches
    
    Args:
        cv_database (dict): Database CV {cv_id: content}
        keywords (list): Keywords to search
        top_n (int): Number of top results to return
    
    Returns:
        list: List of CV results with detailed match information
    """
    # Get search results
    search_results = aho_corasick_search_with_cv_info(cv_database, keywords)
    
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

# Data dummy (same as KMP for consistency)
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

# Driver code
if __name__ == "__main__":
    words = ["cook", "computer", "food", "culinary"]
    with open('data/dummy.txt', 'r') as file:
        text = file.readline().strip() 
        # print(text)

        result = aho_corasick_search(text, words)
        for key, count in result.items():
            print(f"'{key}': {count}")