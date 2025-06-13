'''
Implementasi Algoritma Aho Corasick
'''

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
    
    # helper function to get node by ID
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
    
    # get all pattern matches at a given node
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
    ac = AhoCorasick()
    
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
    
    keywords_clean = [kw.strip() for kw in keywords if kw.strip()]
    
    for cv_id, cv_content in cv_database.items():
        cv_matches = aho_corasick_search(cv_content, keywords_clean)
        
        total_score = sum(cv_matches.values())
        
        results["matches"][cv_id] = cv_matches
        results["cv_scores"][cv_id] = total_score
        
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
    
    ranked_cvs = sorted(
        results["cv_scores"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    results["ranked_cvs"] = ranked_cvs
    
    return results

def search_cvs_with_aho_corasick(cv_database: dict, keywords: list, top_n: int = 5) -> list:
    search_results = aho_corasick_search_with_cv_info(cv_database, keywords)
    
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
                    "positions": positions[:3]  # Show first 3 positions
                })
        
        detailed_results.append(cv_result)
    
    return detailed_results

# Driver code
if __name__ == "__main__":
    words = ["cook", "computer", "food", "culinary"]
    with open('data/dummy.txt', 'r') as file:
        text = file.readline().strip() 
        # print(text)

        result = aho_corasick_search(text, words)
        for key, count in result.items():
            print(f"'{key}': {count}")