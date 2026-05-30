"""
AI Resume Analyzer & Coaching System - Main Streamlit Application
"""
import streamlit as st
import json
from io import BytesIO
from database import db_manager
from resume_parser import resume_parser
from openai_integration import openai_integration
from config import SUPPORTED_FILE_TYPES

st.set_page_config(
    page_title="AI Resume Analyzer & Coaching System",
    page_icon="💼",
    layout="wide"
)

st.markdown('<style>.main-header{font-size:2.5rem;font-weight:700;color:#1f77b4;text-align:center;margin-bottom:2rem;}</style>', unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

with st.sidebar:
    st.title("🎯 Resume Coach AI")
    
    if st.session_state.logged_in:
        st.success(f"Logged in: {st.session_state.user_name}")
        menu = st.radio("Navigation", ["📊 Dashboard", "📄 Upload Resume", "🔍 Analyze Resume", "💬 Career Coaching", "📜 History"], label_visibility="collapsed")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()
    else:
        auth_mode = st.radio("Authentication", ["Login", "Sign Up"])
        if auth_mode == "Login":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                result = db_manager.authenticate_user(email, password)
                if result["success"]:
                    st.session_state.logged_in = True
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_name = result["name"]
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error(result["message"])
        else:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            if st.button("Sign Up"):
                if password != confirm_password:
                    st.error("Passwords don't match!")
                elif not name or not email or not password:
                    st.error("All fields are required!")
                else:
                    result = db_manager.create_user(name, email, password)
                    if result["success"]:
                        st.success("Account created! Please login.")
                    else:
                        st.error(result["message"])

if not st.session_state.logged_in:
    st.markdown('<p class="main-header">🚀 AI Resume Analyzer & Coaching System</p>', unsafe_allow_html=True)
    st.info("Please login or sign up to continue")
    st.stop()

# Dashboard
if menu == "📊 Dashboard":
    st.markdown('<p class="main-header">📊 Your Dashboard</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        resumes = db_manager.get_user_resumes(st.session_state.user_id)
        st.metric("Resumes Uploaded", len(resumes))
    with col2:
        analyses = db_manager.get_user_analyses(st.session_state.user_id)
        st.metric("Analyses Completed", len(analyses))
    with col3:
        sessions = db_manager.get_coaching_history(st.session_state.user_id)
        st.metric("Coaching Sessions", len(sessions))
    st.divider()
    st.subheader("📈 Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Upload New Resume", use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()
    with col2:
        if st.button("🔍 Analyze Resume", use_container_width=True):
            st.session_state.page = "analyze"
            st.rerun()
    with col3:
        if st.button("💬 Talk to Coach", use_container_width=True):
            st.session_state.page = "coaching"
            st.rerun()

# Upload Resume
elif menu == "📄 Upload Resume":
    st.markdown('<p class="main-header">📄 Upload Your Resume</p>', unsafe_allow_html=True)
    st.info(f"Supported formats: {', '.join(SUPPORTED_FILE_TYPES)}")
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"], help="Max file size: 10MB")
    if uploaded_file:
        file_type = "." + uploaded_file.name.split(".")[-1].lower()
        file_size = uploaded_file.size
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File Type:** {file_type}")
        st.write(f"**Size:** {file_size / 1024:.2f} KB")
        if st.button("💾 Upload to Database"):
            file_content = BytesIO(uploaded_file.read())
            result = db_manager.store_resume(user_id=st.session_state.user_id, filename=uploaded_file.name, file_content=file_content.getvalue(), file_type=file_type)
            if result["success"]:
                st.success(f"✅ Resume uploaded! ID: {result['resume_id']}")
                file_content.seek(0)
                parsed_data = resume_parser.parse_resume(file_content, file_type)
                db_manager.update_resume_data(resume_id=result["resume_id"], extracted_text=parsed_data['text'], skills=parsed_data['skills'], education=parsed_data['education'])
                st.info(f"📊 Extracted {len(parsed_data['skills'])} skills, {parsed_data['word_count']} words")
            else:
                st.error(f"❌ Upload failed: {result.get('message', 'Unknown error')}")

# Analyze Resume
elif menu == "🔍 Analyze Resume":
    st.markdown('<p class="main-header">🔍 AI Resume Analysis</p>', unsafe_allow_html=True)
    resumes = db_manager.get_user_resumes(st.session_state.user_id)
    if not resumes:
        st.warning("⚠️ No resumes found. Please upload a resume first.")
        st.stop()
    resume_options = {f"{r['filename']} ({r['uploaded_at'].strftime('%Y-%m-%d')} )": r['_id'] for r in resumes}
    selected_resume_name = st.selectbox("Select Resume to Analyze", list(resume_options.keys()))
    selected_resume_id = resume_options[selected_resume_name]
    if st.button("🚀 Analyze with AI"):
        with st.spinner("🤖 AI is analyzing your resume..."):
            resume_data = db_manager.get_resume(selected_resume_id)
            if resume_data:
                file_content = db_manager.fs.get(resume_data['file_id'])
                parsed_data = resume_parser.parse_resume(BytesIO(file_content.read()), resume_data['file_type'])
                analysis_result = openai_integration.analyze_resume_with_ai(resume_text=parsed_data['text'], skills=parsed_data['skills'], user_profile=None)
                if analysis_result["success"]:
                    analysis = analysis_result["analysis"]
                    st.session_state.current_analysis = analysis
                    db_manager.store_analysis(user_id=st.session_state.user_id, resume_id=selected_resume_id, analysis_data=analysis)
                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Overall Score", f"{analysis['overall_score']}/100")
                    with col2:
                        st.metric("ATS Compatibility", f"{analysis['ats_score']}/100")
                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("✅ Strengths")
                        for strength in analysis['strengths'][:5]:
                            st.success(strength)
                    with col2:
                        st.subheader("⚠️ Weaknesses")
                        for weakness in analysis['weaknesses'][:5]:
                            st.warning(weakness)
                    st.divider()
                    st.subheader("🎯 Recommended Career Paths")
                    for career in analysis['career_suggestions'][:3]:
                        with st.expander(f"{career['role']} ({career['match_percentage']}% match)"):
                            st.write(f"**Why suitable:** {career['why_suitable']}")
                            st.write(f"**Required skills:** {', '.join(career['required_skills'][:5])}")
                    st.subheader("📚 Skill Gaps to Fill")
                    for gap in analysis['skill_gaps'][:5]:
                        st.write(f"**{gap['missing_skill']}** ({gap['importance']}) - {gap['why_needed']}")
                    st.subheader("🎓 Learning Recommendations")
                    for rec in analysis['learning_recommendations'][:5]:
                        st.write(f"• {rec['skill']} - {rec['resource_type']} ({rec['estimated_time']}, {rec['difficulty']})")
                else:
                    st.error(f"❌ Analysis failed: {analysis_result['error']}")
            else:
                st.error("Resume not found")

# Career Coaching
elif menu == "💬 Career Coaching":
    st.markdown('<p class="main-header">💬 AI Career Coach</p>', unsafe_allow_html=True)
    st.info("Ask me anything about your career, resume, job search, or interview preparation!")
    question = st.text_area("Your question:", placeholder="Example: What careers should I consider with my skills in Python and web development?", height=100)
    if st.button("🤔 Get Coaching Advice"):
        if question:
            with st.spinner("🤖 Coach is thinking..."):
                resume_data_list = db_manager.get_user_resumes(st.session_state.user_id)
                resume_context = {}
                analysis_results = {}
                if resume_data_list:
                    latest_resume = db_manager.get_resume(resume_data_list[0]['_id'])
                    if latest_resume:
                        file_content = db_manager.fs.get(latest_resume['file_id'])
                        resume_context = resume_parser.parse_resume(BytesIO(file_content.read()), latest_resume['file_type'])
                if st.session_state.current_analysis:
                    analysis_results = st.session_state.current_analysis
                coaching_result = openai_integration.generate_career_coaching_response(user_question=question, resume_context=resume_context, analysis_results=analysis_results)
                if coaching_result["success"]:
                    st.success("✅ Coaching advice received!")
                    st.markdown(coaching_result["coaching_response"])
                    db_manager.store_coaching_session(user_id=st.session_state.user_id, session_data={"question": question, "response": coaching_result["coaching_response"]})
                else:
                    st.error(f"❌ Coaching failed: {coaching_result['error']}")
    st.divider()
    st.subheader("💡 Quick Questions")
    quick_questions = ["What careers match my current skills?", "How can I improve my resume for FAANG companies?", "What should I learn next to become a data scientist?", "How do I prepare for technical interviews?"]
    for q in quick_questions:
        if st.button(q):
            st.info(f"Question: {q}")
            st.rerun()

# History
elif menu == "📜 History":
    st.markdown('<p class="main-header">📜 Analysis & Coaching History</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔍 Analysis History", "💬 Coaching Sessions"])
    with tab1:
        analyses = db_manager.get_user_analyses(st.session_state.user_id)
        if analyses:
            for analysis in analyses:
                with st.expander(f"Analysis on {analysis['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                    data = analysis['analysis_data']
                    st.metric("Overall Score", f"{data.get('overall_score', 'N/A')}/100")
                    st.write(f"**Strengths:** {len(data.get('strengths', []))} identified")
                    st.write(f"**Skill Gaps:** {len(data.get('skill_gaps', []))} identified")
        else:
            st.info("No analysis history yet")
    with tab2:
        sessions = db_manager.get_coaching_history(st.session_state.user_id)
        if sessions:
            for session in sessions:
                with st.expander(f"Session on {session['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Question:** {session['session_data']['question']}")
                    st.write(f"**Answer:** {session['session_data']['response'][:200]}...")
        else:
            st.info("No coaching sessions yet")