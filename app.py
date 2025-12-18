# import streamlit as st
# import pandas as pd
# from scraper.freshersworld_scraper import scrape_freshersworld
# from scraper.internshala_scraper import scrape_internshala
# from utils.formatter import save_to_excel, save_to_json

# # ---------------------------------------------------
# st.set_page_config(page_title="Job Aggregation Tool", page_icon="💼", layout="wide")
# st.title("💼 Job Aggregation Tool")
# st.markdown("Search and aggregate jobs from **Freshersworld** and **Internshala** easily!")

# # ---------------- Dropdown Inputs -------------------
# col1, col2, col3 = st.columns(3)

# with col1:
#     designation = st.selectbox("🎯 Select Designation", [
#         "Python Developer", "Java Developer", "Data Analyst", "Data Scientist",
#         "Web Developer", "Frontend Developer", "Backend Developer",
#         "Full Stack Developer", "Machine Learning Engineer", "Software Engineer",
#         "Business Analyst", "UI/UX Designer", "Android Developer"
#     ])

# with col2:
#     city = st.selectbox("📍 Select City", [
#         "Bangalore", "Hyderabad", "Chennai", "Pune", "Mumbai",
#         "Delhi", "Ahmedabad", "Kolkata", "Noida", "Gurgaon", "Coimbatore", "Jaipur"
#     ])

# with col3:
#     experience = st.selectbox("🎓 Experience Level", [
#         "Fresher", "0–1 Years", "1–3 Years", "3–5 Years", "5–8 Years", "8+ Years"
#     ])

# # ----------------- Scrape Button --------------------
# if st.button("🚀 Search Jobs"):
#     st.info("⏳ Scraping job portals... please wait...")

#     # Dynamic source selection
#     if "fresher" in experience.lower() or "0" in experience:
#         st.write("🧑‍🎓 **Detected Fresher Level** → Scraping Internshala + Freshersworld")
#         fw_jobs = scrape_freshersworld(designation, city, experience)
#         intern_jobs = scrape_internshala(designation, city, experience)
#         all_jobs = fw_jobs + intern_jobs
#     else:
#         st.write("👨‍💼 **Experienced Level** → Scraping Freshersworld only")
#         all_jobs = scrape_freshersworld(designation, city, experience)

#     # ---------------- Display Results -----------------
#     if all_jobs:
#         df = pd.DataFrame(all_jobs)
#         st.success(f"✅ Found {len(df)} job listings")
#         st.dataframe(df[["Job Title", "Company Name", "Location", "Salary", "Job Portal"]])

#         # Save output
#         save_to_excel(all_jobs, "output/jobs.xlsx")
#         save_to_json(all_jobs, "output/jobs.json")

#         with open("output/jobs.xlsx", "rb") as f:
#             st.download_button(
#                 label="📥 Download Excel File",
#                 data=f,
#                 file_name="jobs.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )

#     else:
#         st.warning("❌ No jobs found. Try different filters.")



import streamlit as st
import pandas as pd
from scraper.freshersworld_scraper import scrape_freshersworld
from scraper.internshala_scraper import scrape_internshala
from utils.formatter import save_to_excel, save_to_json

# ---------------------------------------------------
st.set_page_config(page_title="Job Aggregation Tool", page_icon="💼", layout="wide")
st.title("💼 Job Aggregation Tool")
st.markdown("### 🔍 Find Jobs & Internships from **Freshersworld** and **Internshala**")

# ---------------- Dropdown Inputs -------------------
col1, col2, col3 = st.columns(3)

with col1:
    designation = st.selectbox("🎯 Select Designation", [
        "Python Developer", "Java Developer", "Data Analyst", "Data Scientist",
        "Web Developer", "Frontend Developer", "Backend Developer",
        "Full Stack Developer", "Machine Learning Engineer", "Software Engineer",
        "Business Analyst", "UI/UX Designer", "Android Developer", "DevOps Engineer",
        "Cloud Engineer", "Digital Marketing Executive", "Automation Tester"
    ])

with col2:
    city = st.selectbox("📍 Select City", [
        "Bangalore", "Hyderabad", "Chennai", "Pune", "Mumbai", "Delhi",
        "Ahmedabad", "Kolkata", "Noida", "Gurgaon", "Coimbatore", "Jaipur",
        "Indore", "Vadodara", "Nagpur", "Surat", "Chandigarh"
    ])

with col3:
    experience = st.selectbox("🎓 Experience Level", [
        "Fresher", "0–1 Years", "1–3 Years", "3–5 Years", "5–8 Years", "8+ Years"
    ])

# ----------------- Scrape Button --------------------
if st.button("🚀 Search Jobs"):
    st.info("⏳ Scraping job portals... Please wait...")

    # 🧠 Smart Experience Detection
    try:
        if "fresher" in experience.lower() or "0" in experience:
            st.write("🧑‍🎓 **Detected Fresher Level** → Scraping from Freshersworld + Internshala")
            fw_jobs = scrape_freshersworld(designation, city, experience) or []
            intern_jobs = scrape_internshala(designation, city, experience) or []
            all_jobs = fw_jobs + intern_jobs
        else:
            st.write("👨‍💼 **Experienced Level** → Scraping from Freshersworld only")
            all_jobs = scrape_freshersworld(designation, city, experience) or []
    except Exception as e:
        st.error(f"❌ Error during scraping: {str(e)}")
        all_jobs = []

    # ---------------- Combine & Display Results -----------------
    if all_jobs:
        # ✅ Display search criteria prominently
        st.markdown("---")
        st.markdown("### 📋 Your Search Criteria")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**🎯 Job Title:** {designation}")
        with col2:
            st.markdown(f"**📍 Location:** {city}")
        with col3:
            st.markdown(f"**🎓 Experience:** {experience}")
        st.markdown("---")
        
        df = pd.DataFrame(all_jobs)

        # ✅ Add the searched job title column
        df["Searched Job Title"] = designation

        # ✅ Ensure all columns exist (prevents KeyErrors)
        expected_columns = [
            "Searched Job Title", "Job Title", "Company Name", "Location", "Experience Required",
            "Salary", "Salary / Stipend", "Skills / Role", "Duration",
            "Posted Date", "Job Portal", "Job URL"
        ]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = "N/A"

        # ✅ Merge Salary/Stipend into one unified column
        if "Salary" in df.columns and "Salary / Stipend" in df.columns:
            df["Salary / Stipend"] = df["Salary / Stipend"].where(
                (df["Salary / Stipend"] != "N/A") & (df["Salary / Stipend"] != ""),
                df["Salary"]
            )
            df.drop(columns=["Salary"], inplace=True, errors="ignore")
        elif "Salary" in df.columns:
            df["Salary / Stipend"] = df["Salary"]
            df.drop(columns=["Salary"], inplace=True, errors="ignore")

        # ✅ Remove duplicates (Job Title + Company)
        raw_count = len(df)
        df.drop_duplicates(subset=["Job Title", "Company Name"], inplace=True)
        unique_count = len(df)

        # ✅ Make Job URLs clickable (only for display, keep original for saving)
        df_display = df.copy()
        df_display["Job URL"] = df_display["Job URL"].apply(
            lambda x: f"[🔗 View Job]({x})" if isinstance(x, str) and x != "N/A" else "N/A"
        )

        st.info(f"🧾 Merged {raw_count} listings → after removing duplicates: **{unique_count} unique jobs saved.**")
        print(f"🧾 Merged {raw_count} listings → after removing duplicates: {unique_count} unique jobs saved.")

        # ✅ Column order for display (include searched job title first)
        display_cols = [
            "Searched Job Title", "Job Title", "Company Name", "Location", "Experience Required",
            "Salary / Stipend", "Posted Date",
            "Job Portal"
        ]
        # Ensure display columns exist
        available_display_cols = [col for col in display_cols if col in df_display.columns]

        # ✅ Display results with searched job title
        st.success(f"✅ Found {len(df)} unique job listings for **{designation}** (merged from Freshersworld + Internshala)")
        st.dataframe(df_display[available_display_cols], width='stretch')

        # ✅ Save outputs (save full dataframe with ALL columns - no filtering)
        # Get all columns from dataframe (not just display columns)
        all_columns = list(df.columns)
        all_jobs_data = df[all_columns].to_dict(orient="records")
        
        # Save complete job data with all fields
        save_to_excel(all_jobs_data, "output/jobs.xlsx")
        save_to_json(all_jobs_data, "output/jobs.json")
        st.info(f"💾 Saved {len(all_jobs_data)} complete job records (all fields included) to JSON and Excel files")

        # ✅ Download Buttons
        colA, colB = st.columns(2)
        with colA:
            with open("output/jobs.xlsx", "rb") as f:
                st.download_button(
                    label="📥 Download Excel File",
                    data=f,
                    file_name="jobs.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        with colB:
            with open("output/jobs.json", "rb") as f:
                st.download_button(
                    label="📄 Download JSON File",
                    data=f,
                    file_name="jobs.json",
                    mime="application/json"
                )

    else:
        st.warning("❌ No jobs found. Try changing your filters.")
