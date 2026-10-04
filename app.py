import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load environment variables
# -----------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------

st.title("🧠 AI Career Copilot")

st.write(
    "Generate personalized career guidance, resume content, "
    "skill-gap analysis and interview preparation using Gemini."
)

st.divider()

# -----------------------------
# Check API key
# -----------------------------

if not API_KEY:

    st.error(
        "❌ Gemini API key not found. "
        "Please create a .env file containing GEMINI_API_KEY."
    )

    st.stop()

# -----------------------------
# Connect to Gemini
# -----------------------------

try:

    client = genai.Client(api_key=API_KEY)

except Exception as e:

    st.error(f"❌ Could not initialize Gemini: {e}")

    st.stop()


# -----------------------------
# Candidate Information
# -----------------------------

st.header("👤 Candidate Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Full Name",
        placeholder="e.g. Soham Somavanshi"
    )

    education = st.text_area(
        "Education",
        placeholder="B.Tech in Computer Science..."
    )

    skills = st.text_area(
        "Skills",
        placeholder="Python, SQL, Excel, Power BI..."
    )

with col2:

    experience = st.text_area(
        "Experience",
        placeholder="Internships, freelance work, etc."
    )

    projects = st.text_area(
        "Projects",
        placeholder="AI Supply Chain Platform..."
    )

    target_role = st.text_input(
        "Target Job Role",
        placeholder="e.g. Data Analyst"
    )


# -----------------------------
# Job Description
# -----------------------------

st.header("🎯 Target Job")

job_description = st.text_area(
    "Paste the Job Description",
    height=180,
    placeholder="Paste the job description here..."
)


# -----------------------------
# Generate Button
# -----------------------------

generate = st.button(
    "🚀 Analyze My Career",
    type="primary",
    use_container_width=True
)


# -----------------------------
# Generate AI Response
# -----------------------------

if generate:

    if not name or not target_role:

        st.warning(
            "Please enter your name and target job role."
        )

    else:

        prompt = f"""
You are an expert career coach and technical recruiter.

Analyze this candidate for the target job.

CANDIDATE:

Name:
{name}

Education:
{education}

Skills:
{skills}

Experience:
{experience}

Projects:
{projects}

Target Role:
{target_role}

JOB DESCRIPTION:
{job_description}

Provide the following:

1. Career Objective
Write a strong 2-3 sentence career objective.

2. Professional Summary
Write a professional resume summary.

3. Resume Readiness Score
Give a score from 0-100 and explain the score.

4. Skill Analysis
Identify:
- Strong skills
- Missing skills
- Skills to prioritize

5. Job Match Score
Give a percentage from 0-100 and explain why.

6. Project Improvements
Rewrite each project into strong resume bullet points.

7. Resume Improvements
Give 5 specific recommendations.

8. Interview Questions
Generate:
- 5 technical questions
- 3 HR questions
- 2 project-specific questions

9. 30-Day Learning Roadmap
Create a four-week learning plan.

10. Final Recommendation
Give the candidate's biggest strength,
biggest weakness and most important next step.

IMPORTANT:
Do not invent experience, achievements,
certifications or skills that the candidate
did not provide.

Use clear Markdown headings.
"""

        with st.spinner("🤖 Gemini is analyzing your profile..."):

            try:

                interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt
          )

                result = interaction.output_text

                st.success("✅ Analysis completed!")

                st.divider()

                st.header("📊 AI Career Analysis")

                st.markdown(result)

            except Exception as e:

                st.error("❌ Gemini API request failed.")

                st.code(str(e))


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "AI Career Copilot • Python • Streamlit • Google Gemini"
)