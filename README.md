# 🚀 AI Resume Analyzer & Coaching System

A full-stack AI-powered resume analysis and career coaching application with MongoDB database integration.

## ✨ Features

- **Resume Upload & Storage**: Upload PDF/DOCX/TXT resumes to MongoDB
- **AI-Powered Analysis**: Get detailed resume scoring and feedback using OpenAI
- **Career Suggestions**: Personalized career path recommendations
- **Skill Gap Analysis**: Identify missing skills and learning recommendations
- **Career Coaching**: Interactive AI career coach for Q&A
- **User Authentication**: Secure login/signup with password hashing
- **Analysis History**: Track all your resume analyses over time

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **AI/ML**: OpenAI GPT-4o-mini, NLTK, spaCy
- **Database**: MongoDB (with GridFS for file storage)
- **Document Parsing**: PyPDF2, python-docx

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure Environment Variables

Edit `.env` file and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=resume_coaching_db
JWT_SECRET=your_random_secret_key
```

### 3. Get OpenAI API Key

- Sign up at [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key and paste it in `.env`

### 4. Setup MongoDB (Free)

**Option A: MongoDB Atlas (Cloud - Recommended)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create free account
3. Create cluster (free tier)
4. Get connection string and paste in `.env`

**Option B: Local MongoDB**
```bash
# Install MongoDB locally
# Then use: MONGODB_URI=mongodb://localhost:27017
```

## 🚀 Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure
