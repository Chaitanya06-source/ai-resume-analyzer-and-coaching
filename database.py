"""
In-Memory Database (No MongoDB Required)
"""
from datetime import datetime
import bcrypt

class InMemoryDatabase:
    def __init__(self):
        self.users = {}
        self.resumes = {}
        self.analyses = {}
        self.coaching_sessions = {}
        self.user_counter = 1
        self.resume_counter = 1
        self.analysis_counter = 1
        self.session_counter = 1
        print("✅ In-memory database initialized!")
    
    def create_user(self, name, email, password):
        if email in self.users:
            return {"success": False, "message": "Email already registered"}
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_id = str(self.user_counter)
        self.user_counter += 1
        self.users[email] = {
            "user_id": user_id, "name": name, "email": email,
            "password": hashed_password, "created_at": datetime.now(),
            "profile": {"career_goals": "", "target_role": "", "experience_level": "entry"}
        }
        return {"success": True, "user_id": user_id}
    
    def authenticate_user(self, email, password):
        if email not in self.users:
            return {"success": False, "message": "Invalid email or password"}
        user = self.users[email]
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return {"success": True, "user_id": user["user_id"], "name": user["name"]}
        return {"success": False, "message": "Invalid email or password"}
    
    def store_resume(self, user_id, filename, file_content, file_type):
        resume_id = str(self.resume_counter)
        self.resume_counter += 1
        self.resumes[resume_id] = {
            "resume_id": resume_id, "user_id": user_id, "filename": filename,
            "file_type": file_type, "file_content": file_content,
            "uploaded_at": datetime.now(), "extracted_text": "", "skills": [], "education": []
        }
        return {"success": True, "resume_id": resume_id, "file_id": resume_id}
    
    def get_user_resumes(self, user_id):
        return [r for r in self.resumes.values() if r["user_id"] == user_id]
    
    def get_resume(self, resume_id):
        return self.resumes.get(resume_id)
    
    def update_resume_data(self, resume_id, extracted_text, skills, education):
        if resume_id in self.resumes:
            self.resumes[resume_id]["extracted_text"] = extracted_text
            self.resumes[resume_id]["skills"] = skills
            self.resumes[resume_id]["education"] = education
            return {"success": True}
        return {"success": False}
    
    def store_analysis(self, user_id, resume_id, analysis_data):
        analysis_id = str(self.analysis_counter)
        self.analysis_counter += 1
        self.analyses[analysis_id] = {
            "analysis_id": analysis_id, "user_id": user_id,
            "resume_id": resume_id, "analysis_data": analysis_data, "created_at": datetime.now()
        }
        return {"success": True, "analysis_id": analysis_id}
    
    def get_user_analyses(self, user_id):
        return [a for a in self.analyses.values() if a["user_id"] == user_id][-10:]
    
    def store_coaching_session(self, user_id, session_data):
        session_id = str(self.session_counter)
        self.session_counter += 1
        self.coaching_sessions[session_id] = {
            "session_id": session_id, "user_id": user_id,
            "session_data": session_data, "created_at": datetime.now()
        }
        return {"success": True, "session_id": session_id}
    
    def get_coaching_history(self, user_id):
        return [s for s in self.coaching_sessions.values() if s["user_id"] == user_id]

db_manager = InMemoryDatabase()