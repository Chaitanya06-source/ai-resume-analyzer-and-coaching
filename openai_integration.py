"""
OpenAI API Integration for Personalized Career Suggestions & Coaching
"""
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

class OpenAIIntegration:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
    
    def analyze_resume_with_ai(self, resume_text, skills, user_profile=None):
        """Get comprehensive AI-powered resume analysis"""
        
        user_context = ""
        if user_profile:
            user_context = f"""
User's Career Goals: {user_profile.get('career_goals', 'Not specified')}
Target Role: {user_profile.get('target_role', 'Not specified')}
Experience Level: {user_profile.get('experience_level', 'Entry')}
"""
        
        prompt = f"""You are an expert career coach and resume analyst. Analyze this resume and provide detailed feedback in VALID JSON format only.

RESUME TEXT:
{resume_text[:8000]}

EXTRACTED SKILLS:
{json.dumps(skills, indent=2)}

{user_context}

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:

{{
  "overall_score": 0-100,
  "ats_score": 0-100,
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "skill_gaps": [{{"missing_skill": "skill name", "importance": "high/medium/low", "why_needed": "reason"}}],
  "improvement_suggestions": [{{"category": "skills/formatting/content", "suggestion": "specific suggestion", "priority": "high/medium/low"}}],
  "career_suggestions": [{{"role": "job title", "match_percentage": 0-100, "why_suitable": "reason", "required_skills": ["skill1", "skill2"]}}],
  "learning_recommendations": [{{"skill": "skill to learn", "resource_type": "course/certification/project", "estimated_time": "hours/weeks", "difficulty": "beginner/intermediate/advanced"}}]
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert career coach. Always return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return {"success": True, "analysis": analysis}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_career_coaching_response(self, user_question, resume_context, analysis_results):
        """Get personalized career coaching response"""
        
        skills_list = ', '.join([s['skill'] for s in resume_context.get('skills', [])][:10])
        
        context = f"""
User's Resume Summary:
- Skills: {skills_list}
- Experience: {resume_context.get('experience_years', 0)} years

Recent Analysis Results:
- Overall Score: {analysis_results.get('overall_score', 'N/A')}/100
- Top Strengths: {analysis_results.get('strengths', [])[:3]}

User's Question: {user_question}
"""
        
        prompt = f"""You are a supportive career coach. Help the user with their career question.

{context}

Provide a helpful, encouraging, and actionable response. Keep it concise (under 300 words) and practical."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a supportive career coach. Be encouraging and practical."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {"success": True, "coaching_response": response.choices[0].message.content}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_cover_letter(self, resume_text, job_description):
        """Generate a cover letter based on resume and job description"""
        
        prompt = f"""Create a professional cover letter.

RESUME:
{resume_text[:6000]}

JOB DESCRIPTION:
{job_description[:4000]}

Format: Professional business letter, 3-4 paragraphs
Tone: Confident but humble
Include: Introduction, relevant experience, why you're a good fit, call to action

Return ONLY the cover letter text, no markdown."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional career writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return {"success": True, "cover_letter": response.choices[0].message.content}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def interview_prep_questions(self, target_role, skills):
        """Generate interview preparation questions"""
        
        skills_list = ', '.join([s['skill'] for s in skills][:8])
        
        prompt = f"""Generate 10 interview questions for a {target_role} position.

Relevant Skills: {skills_list}

For each question provide: question, what_interviewer_wants_to_know, sample_answer

Return as JSON array:
[{{"question": "...", "what_interviewer_wants_to_know": "...", "sample_answer": "..."}}]

Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interview coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            questions = json.loads(response.choices[0].message.content)
            return {"success": True, "questions": questions}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

# Initialize OpenAI integration
openai_integration = OpenAIIntegration()