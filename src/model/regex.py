'''
Hal-hal yang perlu di-ekstrak:
    1. job history
    2. skills
    3. education
'''
import re

info_key_regex = [["skill"], ["summary"], ["highlight"], ["accomplishment"],
                  ["experience", "work"], ["education"]]

def count_words(s: str) -> int:
    return len(s.strip().split())

# return dict dg key = info group, val = konten
def extract_information_group(filename : str) -> dict :
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]
        lines = list(filter(lambda line: line != "", lines))
        # print(lines)
        
        # extract info per info_key_regex
        info_groups = {}
        current_key = None
        current_content = []
        
        job_title = None
        start_idx = 0
        
        # get job title (first line)
        if lines and not any((re.search(pattern, lines[0], re.IGNORECASE) for pattern in patterns) for patterns in info_key_regex):
            job_title = lines[0].strip()
            start_idx = 1
        
        for i in range(start_idx, len(lines)):
            line = lines[i]
            matched_key = None
            for patterns in info_key_regex:
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns) and patterns[0] not in info_groups and count_words(line) <= 3:
                    matched_key = patterns[0].replace('[','').replace(']','').lower()
                    # print("found matched: " + matched_key)
                    break
            if matched_key:
                # save prev section
                if current_key and current_content:
                    info_groups[current_key] = current_content.copy()
                    # print("save: " + current_key)
                    
                # start new section
                current_key = matched_key
                current_content = []
            else:
                # add content to current section
                if current_key:
                    # print("added line: " + line)
                    current_content.append(line)
        
        # save the last section
        if current_content and current_key:
            info_groups[current_key] = current_content
        
        # add job title
        if job_title:
            info_groups['job_title'] = [job_title]
        
        # print(info_groups)
        
        # generate summary per info\
        summary = generate_summary(info_groups)    
        return summary    

# generate summary for education, job history, and skill
def generate_summary(data : dict) -> dict :
    summaries = {}
    for key, content in data.items():
        if key == 'education':
            summaries[key] = extract_education(content)
        elif key == 'skill':
            summaries[key] = extract_skill(content)
        elif key == 'experience':
            summaries[key] = extract_job_history(content)
            
    return summaries

# extracting education
def extract_education(data : list) -> list :
    print("Extracting education")
    print(data)
    processed_data = data.copy()
    educatinon = []
    current_edu = {}
    
    degree_patterns = [
        r'\b(bachelor|master|phd|doctorate|diploma|certificate)\b',
        r'\b(b\.?s\.?|m\.?s\.?|m\.?a\.?|ph\.?d\.?|b\.?a\.?)\b',
        r'\b(undergraduate|graduate|postgraduate)\b',
        r'\b(associate|degree|certification)\b',
        r'\b(high\s*school)\b',
    ]
    
    institution_patterns = [
        r'\b(university|college|institute|school|academy)\b',
        r'\bof\s+[\w\s]+\b',  # "University of Something"
    ]
    
    field_patterns = [
        r':\s*([^,]+)',  # "Diploma : Culinary/Auto Body"
        r'\bin\s+([^,]+)\b',  # "Bachelor in Computer Science"
        r'\bof\s+([^,]+)\b',  # "Master of Business"
        r'\b(computer\s*science|engineering|business|management|arts|science|culinary|hospitality)\b',
    ]
    
    date_patterns = [
        r'\b(20\d{2}|19\d{2})\b',
        r'\b(graduated|class\s*of)\s*\d{4}\b',
    ]
    
    # year-only pattern for standalone years
    year_only_pattern = r'^\s*(20\d{2}|19\d{2})\s*'
    

# extracting job history
def extract_job_history(data : list) -> list :
    print("Extracting job")
    print(data)
    
# extracting skills
def extract_skill(data : list) -> list :
    print("Extracting skills")
    print(data)   
        
        
# driver
if __name__ == "__main__":
    extract_information_group('data/regex.txt')