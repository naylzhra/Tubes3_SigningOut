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

def extract_education(data : list) -> list :
    print("Extracting education")
    print(data)
    
    education = []
    
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
    
    for line in data:
        line_lower = line.lower()
        
        degree_found = None
        for pattern in degree_patterns:
            match = re.search(pattern, line_lower, re.IGNORECASE)
            if match:
                degree_found = match.group(0)
                break
        
        institution_found = None
        for pattern in institution_patterns:
            match = re.search(pattern, line_lower, re.IGNORECASE)
            if match:
                institution_found = line.strip()
                break
        
        field_found = None
        for pattern in field_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                field_found = match.group(1).strip() if len(match.groups()) > 0 else match.group(0)
                break
        
        date_found = None
        for pattern in date_patterns:
            match = re.search(pattern, line)
            if match:
                date_found = match.group(0)
                break
        
        if degree_found or institution_found or field_found:
            edu_entry = {
                "degree": degree_found or field_found or line.strip(),
                "period": date_found or "Study Period"
            }
            if institution_found:
                edu_entry["institution"] = institution_found
            education.append(edu_entry)
    
    return education[:2] if education else []

def extract_job_history(data : list) -> list :
    print("Extracting job")
    print(data)
    
    jobs = []
    
    job_title_patterns = [
        r'\b(manager|engineer|developer|analyst|coordinator|specialist|assistant|director|supervisor)\b',
        r'\b(senior|junior|lead|principal|staff)\s+\w+',
    ]
    
    company_patterns = [
        r'\b(company|corporation|corp|inc|ltd|llc|group|solutions|systems|technologies)\b',
        r'at\s+([^,\n]+)',
    ]
    
    date_patterns = [
        r'\b(20\d{2}|19\d{2})\s*[-–—]\s*(20\d{2}|19\d{2}|present|current)\b',
        r'\b(20\d{2}|19\d{2})\b',
    ]
    
    current_job = {}
    job_lines = []
    
    for line in data:
        line_stripped = line.strip()
        if not line_stripped:
            if job_lines:
                job_entry = process_job_lines(job_lines, job_title_patterns, company_patterns, date_patterns)
                if job_entry:
                    jobs.append(job_entry)
                job_lines = []
            continue
        
        job_lines.append(line_stripped)
    
    if job_lines:
        job_entry = process_job_lines(job_lines, job_title_patterns, company_patterns, date_patterns)
        if job_entry:
            jobs.append(job_entry)
    
    return jobs[:3] if jobs else []

def process_job_lines(lines: list, title_patterns: list, company_patterns: list, date_patterns: list) -> dict:
    try:
        title = lines[0] if lines else "Position"
        period = "Experience Period"
        company = ""
        description = ""
        
        all_text = " ".join(lines)
        
        for pattern in date_patterns:
            match = re.search(pattern, all_text, re.IGNORECASE)
            if match:
                period = match.group(0)
                break
        
        for pattern in company_patterns:
            match = re.search(pattern, all_text, re.IGNORECASE)
            if match:
                if len(match.groups()) > 0:
                    company = match.group(1).strip()
                break
        
        if len(lines) > 1:
            description = " ".join(lines[1:])[:150] + "..."
        else:
            description = "Professional experience in this role."
        
        return {
            "title": title,
            "period": period,
            "description": description
        }
        
    except Exception as e:
        print(f"Error processing job lines: {e}")
        return None

def extract_skill(data : list) -> list :
    print("Extracting skills")
    print(data)   
    
    skills = []
    
    skill_patterns = [
        r'\b(python|java|javascript|typescript|c\+\+|c#|php|ruby|go|rust)\b',
        r'\b(html|css|react|angular|vue|node\.?js|django|flask|spring)\b',
        r'\b(sql|mysql|postgresql|mongodb|redis|oracle|sqlite)\b',
        r'\b(aws|azure|gcp|docker|kubernetes|git|linux|windows)\b',
        r'\b(photoshop|illustrator|figma|sketch|autocad|solidworks)\b',
        r'\b(excel|powerpoint|word|outlook|salesforce|sap)\b',
        r'\b(project\s*management|team\s*leadership|communication|problem\s*solving)\b',
    ]
    
    for line in data:
        line_lower = line.lower()
        
        if ',' in line or '•' in line or '-' in line:
            parts = re.split(r'[,•\-\n]', line)
            for part in parts:
                skill = part.strip()
                if skill and len(skill) > 1:
                    skills.append(skill.title())
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, line_lower, re.IGNORECASE)
            for match in matches:
                skills.append(match.title())
        
        if len(line.strip().split()) <= 3 and len(line.strip()) > 2:
            skills.append(line.strip().title())
    
    unique_skills = list(dict.fromkeys(skills))
    return unique_skills[:10] if unique_skills else []
        
        
# driver
if __name__ == "__main__":
    extract_information_group('data/regex.txt')