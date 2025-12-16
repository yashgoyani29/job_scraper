import streamlit as st
import pandas as pd
from scraper.freshersworld_scraper import scrape_freshersworld
from scraper.internshala_scraper import scrape_internshala
from utils.formatter import save_to_excel

# =============================
# STREAMLIT APP CONFIGURATION
# =============================
st.set_page_config(page_title="Job Aggregation Tool", page_icon="💼", layout="centered")

st.title("💼 Job Aggregation Tool")
st.markdown("### 🔍 Search Jobs from Freshersworld & Indeed")

# =============================
# DROPDOWN INPUTS
# =============================
designation = st.selectbox(
    "Select Designation / Job Role",
    [
        "Python Developer",
        "Java Developer",
        "Data Analyst",
        "Web Developer",
        "Software Engineer",
        "Machine Learning Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Business Analyst",
        "UI/UX Designer",
        "Data Scientist",
    ],
    index=0
)

city = st.selectbox(
    "Select City / Location",
    [
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Mumbai",
        "Delhi",
        "Ahmedabad",
        "Kolkata",
        "Noida",
        "Gurgaon",
        "Coimbatore",
        "Jaipur",
    ],
    index=0
)

experience = st.selectbox(
    "Select Experience Level",
    [
        "Fresher",
        "0–1 Years",
        "1–3 Years",
        "3–5 Years",
        "5–8 Years",
        "8+ Years"
    ],
    index=0
)

# =============================
# SCRAPE BUTTON
# =============================
if st.button("Search Jobs 🔎"):
    st.info("⏳ Scraping job portals... Please wait...")

    fw_jobs = scrape_freshersworld(designation, city, experience)
    intern_jobs = scrape_internshala(designation, city, experience)

    all_jobs = fw_jobs + intern_jobs

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        df = df.dropna(subset=["Job Title", "Company Name", "Job URL"])

        st.success(f"✅ Found {len(df)} job listings.")
        st.markdown("### 📊 Job Results")

        # 🧠 Make Job URLs clickable
        df["Job URL"] = df["Job URL"].apply(lambda x: f"[View Job]({x})")

        # Display table with clickable links
        st.markdown(
            df.to_markdown(index=False),
            unsafe_allow_html=True
        )

        # Save to Excel
        save_to_excel(all_jobs, "output/jobs.xlsx")

        # Download button
        with open("output/jobs.xlsx", "rb") as file:
            st.download_button(
                label="📥 Download Excel File",
                data=file,
                file_name="jobs.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # st.markdown("### 🏢 Company Overview")
        # st.dataframe(df[["Company Name", "Job Title", "Salary", "Job Portal"]])
    else:
        st.warning("❌ No jobs found. Try changing your filters.")
