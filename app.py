import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD GEMINI API KEY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# ------------------------------------------------------------
# LOCAL DEVELOPMENT
# ------------------------------------------------------------

load_dotenv(dotenv_path=ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")


# ------------------------------------------------------------
# STREAMLIT CLOUD
# ------------------------------------------------------------

if not API_KEY:
    try:
        API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        API_KEY = None


# ------------------------------------------------------------
# CHECK API KEY
# ------------------------------------------------------------

if not API_KEY:
    st.error(
        "❌ Gemini API key not configured. "
        "Please add GEMINI_API_KEY to your Streamlit Secrets."
    )
    st.stop()


# ============================================================
# INITIALIZE GEMINI
# ============================================================

try:

    client = genai.Client(api_key=API_KEY)

except Exception as e:

    st.error("❌ Could not initialize Gemini.")
    st.code(str(e))
    st.stop()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .hero {
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            #111827,
            #1e293b
        );
        border: 1px solid #334155;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 18px;
        color: #cbd5e1;
    }

    .feature-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #334155;
        background: #111827;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">

        <h1>🧠 AI Career Copilot</h1>

        <p>
        Your GenAI-powered career assistant for resume optimization,
        job matching, skill-gap analysis, interview preparation
        and personalized career planning.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR — CANDIDATE PROFILE
# ============================================================

with st.sidebar:

    st.header("👤 Candidate Profile")

    st.caption(
        "Enter your information to generate a personalized "
        "career analysis."
    )

    name = st.text_input(
        "Full Name",
        placeholder="e.g. Soham Somavanshi"
    )

    education = st.text_area(
        "🎓 Education",
        placeholder=(
            "B.Tech in Computer Science\n"
            "University / College"
        )
    )

    skills = st.text_area(
        "💻 Skills",
        placeholder=(
            "Python, SQL, Excel, Power BI, AWS..."
        )
    )

    experience = st.text_area(
        "💼 Experience",
        placeholder=(
            "Internships, freelance work, "
            "part-time jobs, etc."
        )
    )

    projects = st.text_area(
        "🚀 Projects",
        placeholder=(
            "AI Supply Chain Platform\n"
            "Traffic Eye\n"
            "Portfolio Website"
        )
    )

    target_role = st.text_input(
        "🎯 Target Job Role",
        placeholder="e.g. Data Analyst"
    )


# ============================================================
# JOB DESCRIPTION
# ============================================================

st.header("🎯 Target Job")

job_description = st.text_area(
    "Paste the Job Description",
    height=200,
    placeholder=(
        "Paste the job description here.\n\n"
        "For example:\n"
        "We are looking for a Data Analyst who can work "
        "with Python, SQL, Excel and Power BI..."
    )
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

generate = st.button(
    "🚀 Analyze My Career",
    type="primary",
    use_container_width=True
)


# ============================================================
# AI ANALYSIS
# ============================================================

if generate:

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if not name:

        st.warning(
            "⚠️ Please enter your name."
        )

        st.stop()

    if not target_role:

        st.warning(
            "⚠️ Please enter your target job role."
        )

        st.stop()


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an expert career coach, technical recruiter,
resume consultant and interview specialist.

Analyze the candidate below for their target job role.

============================================================
CANDIDATE PROFILE
============================================================

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

Target Job Role:
{target_role}

============================================================
JOB DESCRIPTION
============================================================

{job_description}

============================================================
IMPORTANT RULE
============================================================

Do NOT invent information.

Do NOT invent:

- Experience
- Certifications
- Achievements
- Technologies
- Companies
- Job positions
- Metrics
- Projects
- Awards

Only use information provided by the candidate.

If information is missing, clearly say that it was
not provided.

============================================================
1. CAREER OBJECTIVE
============================================================

Write a strong 2-3 sentence career objective
specifically targeted toward the target job role.

============================================================
2. PROFESSIONAL SUMMARY
============================================================

Write a professional resume summary.

Keep it concise, realistic and suitable for a resume.

============================================================
3. RESUME READINESS SCORE
============================================================

Give a score from 0-100.

Explain:

- What is already strong
- What is missing
- What needs improvement

============================================================
4. SKILL ANALYSIS
============================================================

Create the following sections:

### Strong Skills

Skills the candidate already demonstrates.

### Missing Skills

Important skills required for the target role
that the candidate does not currently mention.

### Skills to Prioritize

Top 5 skills the candidate should learn next.

============================================================
5. JOB MATCH SCORE
============================================================

Give a Job Match Score from 0-100%.

Explain:

- Matching skills
- Missing skills
- Relevant experience
- Relevant projects
- Overall suitability

============================================================
6. PROJECT OPTIMIZATION
============================================================

Rewrite each candidate project into strong,
professional resume bullet points.

Use action-oriented language.

Do NOT invent metrics or achievements.

============================================================
7. RESUME IMPROVEMENTS
============================================================

Give 5 specific recommendations that would make
the candidate's resume stronger.

============================================================
8. INTERVIEW QUESTIONS
============================================================

Generate 10 interview questions.

### Technical Questions

5 technical questions related to the target job.

### HR Questions

3 HR questions.

### Project Questions

2 questions specifically related to the
candidate's projects.

============================================================
9. 30-DAY LEARNING ROADMAP
============================================================

Create a practical 30-day roadmap.

### Week 1 — Foundation

Topics and activities.

### Week 2 — Skill Development

Topics and activities.

### Week 3 — Projects and Practice

Topics and activities.

### Week 4 — Interview and Job Preparation

Topics and activities.

Make the roadmap realistic for a student.

============================================================
10. FINAL CAREER RECOMMENDATION
============================================================

Provide:

### Biggest Strength

### Biggest Weakness

### Most Important Skill to Learn

### Recommended Next Step

### Overall Recommendation

============================================================

Use clean Markdown formatting.

Make the answer detailed enough to be useful but
avoid unnecessary repetition.
"""


    # --------------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------------

    with st.spinner(
        "🤖 Gemini is analyzing your career profile..."
    ):

        try:

            interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt
            )

            result = interaction.output_text


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            st.success(
                "✅ Career analysis completed successfully!"
            )

            st.divider()

            st.header(
                "📊 Your AI Career Analysis"
            )

            st.markdown(result)


            # ------------------------------------------------
            # DOWNLOAD REPORT
            # ------------------------------------------------

            st.download_button(
                label="📥 Download Career Analysis",
                data=result,
                file_name="AI_Career_Analysis.txt",
                mime="text/plain",
                use_container_width=True
            )


        except Exception as e:

            st.error(
                "❌ Gemini API request failed."
            )

            st.code(str(e))


# ============================================================
# LANDING PAGE
# ============================================================

else:

    st.markdown(
        """
        ## 👋 Welcome to AI Career Copilot

        AI Career Copilot uses **Generative AI** to analyze
        your career profile and provide personalized
        career guidance.

        ### 🔄 How It Works

        **1. 👤 Enter Your Profile**

        Add your education, skills, experience and projects.

        **2. 🎯 Choose Your Target Role**

        Examples:

        - Data Analyst
        - Software Developer
        - AI Engineer
        - Cloud Engineer
        - Product Manager
        - Business Analyst

        **3. 📄 Add a Job Description**

        Paste the job description you're targeting.

        **4. 🤖 Let Gemini Analyze Your Profile**

        The AI compares your profile against the
        requirements of the target role.

        **5. 📊 Get Your Career Report**

        You receive:

        - 🎯 Career Objective
        - 📝 Professional Summary
        - 📊 Resume Readiness Score
        - 🔍 Skill Gap Analysis
        - 💼 Job Match Score
        - 🚀 Project Improvements
        - 🎤 Interview Questions
        - 📚 30-Day Learning Roadmap
        - 💡 Personalized Career Recommendations

        ---

        ### 🧠 What Makes This a GenAI Project?

        Instead of using fixed rules or predefined responses,
        the application uses a Large Language Model to
        understand the candidate's profile and generate
        personalized recommendations dynamically.

        ---

        ### 🛠️ Technology

        **Python • Streamlit • Google Gemini • Generative AI**
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧠 AI Career Copilot • "
    "Built with Python, Streamlit & Google Gemini"
)
