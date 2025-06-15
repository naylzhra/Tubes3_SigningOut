'''
Hal-hal yang perlu di-ekstrak:
    1. job history
    2. skills
    3. education
'''
import re

info_key_regex = [["skill", "summary", "highlight"], ["accomplishment"],
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
    # print(data)
    
    degree_patterns = [
        r'\b(bachelor(?:\s+of\s+\w+)?|b\.?s\.?|b\.?a\.?)\b',                         
        r'\b(master(?:\s+of\s+\w+)?|m\.?s\.?|m\.?a\.?)\b',                      
        r'\b(ph\.?d\.?|doctorate|doctoral)\b',                                       
        r'\b(associate(?:\s+degree)?|undergraduate|graduate|postgraduate)\b',      
        r'\b(diploma|certificate|certification)\b',                               
        r'\b(high\s*school|secondary\s*school)\b'                             
    ]

    
    institution_patterns = [
        r'\b(?:university|college|school|academy|institute|school)\s+of\s+[\w\s&\-]+',    
        r'\b[\w\s&\-]+(?:university|college|school|academy|institute)\b'        
    ]

    
    date_patterns = [
        r'\b(19\d{2}\s*(?: -|to)\s*20\d{2})',
        r'\b(20\d{2}\s*(?: -|to)\s*20\d{2})',
        r'\b(20\d{2}|19\d{2})\b',
        r'\b(graduated|class\s*of)\s*\d{4}\b',
    ]
    
    education = []
    info_education = ['year', 'institution', 'degree']
    current_edu = dict.fromkeys(info_education)
    
    for line in data:        
        raw_line = line.strip().lower()
        
        sub_lines = raw_line.split(',')
        
        for sentence in sub_lines:
            # search degree
            for pattern in degree_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match and current_edu['degree'] is None:
                    print("deg: " + match.group(0))
                    current_edu['degree'] = match.group(0)
                    break
            
            # search institution
            for pattern in institution_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match and current_edu['institution'] is None:
                    print("inst: " + match.group(0))
                    current_edu['institution'] = match.group(0)
                    break
        
            # search tahun
            for pattern in date_patterns:
                match = re.search(pattern, sentence)
                if match and current_edu['year'] is None:
                    print("year: " + match.group(0))
                    current_edu['year'] = match.group(0)
                    break
                
            # jika seluruh field telah terisi, tambahkan ke education dan buat current edu baru
            if all(current_edu.values()):
                education.append(current_edu)
                current_edu = dict.fromkeys(info_education)
    return education[:2] if education else []

def extract_job_history(data : list) -> list :
    print("Extracting job...")
    # print(data)
    
    role_core = r'(assistant|senior|junior|staff|lead|principal|manager|engineer|developer|analyst|specialist|director|supervisor|consultant|architect|officer|chef|cook)'
    modifiers = r'(?:r&d|kitchen|hospitality|research|product|software|data|qa|project|business|marketing|sales|cloud|network|hr|finance|development|design|testing|support|systems|operations|manager)'

    job_title_patterns = [
        rf'\b(?:{modifiers}\s+)?(?:{modifiers}\s+)?{role_core}\b', # before core
        rf'\b{role_core}(?:\s+{modifiers})?(?:\s+{modifiers})?\b', # after core
        rf'\b(?:{modifiers}\s+)?{role_core}(?:\s+{modifiers})?\b', # mixed
    ]


    
    company_keywords = (
        r'Company|Co\.?|Corporation|Corp\.?|Inc\.?|Ltd\.?|' 
        r'Pvt Ltd|Group|Enterprises?|Solutions?|Technologies?|Industries|'
        r'International|Partners|Systems|Consulting|Networks'
    )

    company_patterns = [
        fr'\b(?:{company_keywords})\s+[A-Z][\w&,.()-]*\b|'
        fr'\b[A-Z][\w&,.()-]*(?:\s+[A-Z][\w&,.()-]*)*\s+(?:{company_keywords})\b'
    ]


    date_patterns = [
        r'\b(19\d{2}\s*(?: -|to)\s*20\d{2})',
        r'\b(20\d{2}\s*(?: -|to)\s*20\d{2})',
        r'\b(20\d{2}|19\d{2})\s*(?: -|to)\s*(20\d{2}|19\d{2}|present|current)\b',
        r'\b(20\d{2}|19\d{2})\b',
    ]
    
    info_job = ['year', 'company', 'role']
    jobs = []
    current_job = dict.fromkeys(info_job)
    
    for line in data:
        raw_line = line.strip().lower()
        
        sub_lines = raw_line.split(',')
        
        for sentence in sub_lines:

            if count_words(sentence) > 15 : continue
            
            # search year/period
            for pattern in date_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match and current_job['year'] is None:
                    # print("year: " + match.group(0))
                    current_job['year'] = match.group(0)
                    break
                
            # search company
            for pattern in company_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match and current_job['company'] is None:
                    # print("company: " + match.group(0))
                    current_job['company'] = match.group(0)
                    break
                
            # search role
            for pattern in job_title_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match and current_job['role'] is None:
                    print(sentence)
                    print("role: " + match.group(0))
                    current_job['role'] = match.group(0)
                    break
                
        # jika seluruh field telah terisi, tambahkan ke education dan buat current edu baru
            if all(current_job.values()):
                jobs.append(current_job)
                current_job = dict.fromkeys(info_job)
        
    # print(jobs)
    return jobs[:3] if jobs else []

def extract_skill(data : list) -> list :
    print("Extracting skills...")
    # print(data)   
    
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
    summary = extract_information_group('../../data/regex.txt')
    print(summary)