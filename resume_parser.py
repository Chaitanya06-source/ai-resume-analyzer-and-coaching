"""
Resume Parser - Extracts text, skills, and information from PDF/DOCX resumes
"""
import PyPDF2
from docx import Document
import re
import nltk
from io import BytesIO

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ResumeParser:
    def __init__(self):
        self.skill_keywords = {
            'programming': ['python', 'java', 'c', 'c++', 'javascript', 'typescript', 'sql', 'html', 'css', 'php', 'ruby', 'go', 'rust'],
            'web_development': ['react', 'angular', 'vue', 'django', 'flask', 'node.js', 'express', 'nestjs'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'machine learning', 'deep learning', 'ai'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'git', 'ci/cd'],
            'database': ['mysql', 'mongodb', 'postgresql', 'redis', 'cassandra', 'firebase', 'nosql'],
            'testing': ['pytest', 'selenium', 'jest', 'cypress', 'qa', 'quality assurance'],
            'mobile': ['flutter', 'react native', 'android', 'ios', 'swift', 'kotlin']
        }
    
    def extract_text_from_pdf(self, file_content):
        """Extract text from PDF file"""
        text = ""
        try:
            if isinstance(file_content, bytes):
                file_content = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(file_content)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
        return text
    
    def extract_text_from_docx(self, file_content):
        """Extract text from DOCX file"""
        text = ""
        try:
            if isinstance(file_content, bytes):
                file_content = BytesIO(file_content)
            doc = Document(file_content)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
        return text
    
    def extract_text_from_txt(self, file_content):
        """Extract text from TXT file"""
        try:
            if isinstance(file_content, bytes):
                text = file_content.decode('utf-8', errors='ignore')
            else:
                text = file_content.read().decode('utf-8', errors='ignore')
        except:
            text = ""
        return text
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        detected_skills = []
        
        for category, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    skill_entry = {
                        'skill': keyword.title(),
                        'category': category,
                        'confidence': 'high'
                    }
                    if skill_entry not in detected_skills:
                        detected_skills.append(skill_entry)
        
        return detected_skills
    
    def extract_education(self, text):
        """Extract education information"""
        education = []
        
        patterns = [
            r'(b\.?tech?|b\.?sc?|b\.?com|b\.?pharm|m\.?tech?|m\.?sc?|m\.?com|m\.?pharm|phd)\s+in\s+([a-zA-Z0-9\s]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'degree': match[0] if isinstance(match, tuple) else match,
                    'institution': match[1] if isinstance(match, tuple) else '',
                    'year': self.extract_year(text)
                })
        
        return education
    
    def extract_year(self, text):
        """Extract year from text"""
        years = re.findall(r'\b(20\d{2}|19\d{2})\b', text)
        return years[-1] if years else ""
    
    def extract_experience_years(self, text):
        """Extract years of experience"""
        patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*\+\s*years',
            r'(\d+)\s*years?\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0
    
    def extract_contact_info(self, text):
        """Extract contact information"""
        contact = {'email': '', 'phone': '', 'linkedin': '', 'github': ''}
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group()
        
        phone_pattern = r'\+?\d[\d\s-]{7,}\d'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact['phone'] = phone_match.group()
        
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        github_match = re.search(r'github\.com/[\w-]+', text)
        if github_match:
            contact['github'] = github_match.group()
        
        return contact
    
    def parse_resume(self, file_content, file_type):
        """Main function to parse resume"""
        if file_type == '.pdf':
            text = self.extract_text_from_pdf(file_content)
        elif file_type == '.docx':
            text = self.extract_text_from_docx(file_content)
        elif file_type == '.txt':
            text = self.extract_text_from_txt(file_content)
        else:
            text = ""
        
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        experience_years = self.extract_experience_years(text)
        contact_info = self.extract_contact_info(text)
        
        return {
            'text': text,
            'skills': skills,
            'education': education,
            'experience_years': experience_years,
            'contact_info': contact_info,
            'word_count': len(text.split()),
            'character_count': len(text)
        }

# Initialize parser
resume_parser = ResumeParser()