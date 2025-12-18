from scraper.freshersworld_scraper import scrape_freshersworld
from scraper.internshala_scraper import scrape_internshala
from utils.formatter import save_to_json, save_to_excel
import pandas as pd

def main():
    print("===== JOB AGGREGATION TOOL =====")
    designation = input("Enter Job Title: ")
    city = input("Enter City / Location: ")
    experience = input("Enter Experience (Fresher / Years): ")

    print("\n🔍 Collecting job data... please wait...\n")

    try:
        if "fresher" in experience.lower() or "0" in experience:
            fw_jobs = scrape_freshersworld(designation, city, experience) or []
            intern_jobs = scrape_internshala(designation, city, experience) or []
            all_jobs = fw_jobs + intern_jobs
        else:
            all_jobs = scrape_freshersworld(designation, city, experience) or []
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        all_jobs = []

    print(f"\n✅ Total Jobs Collected: {len(all_jobs)}")

    if all_jobs:
        # Add searched job title to each job entry
        for job in all_jobs:
            job["Searched Job Title"] = designation
        
        # Display summary
        df = pd.DataFrame(all_jobs)
        print(f"\n📊 Search Results for: {designation}")
        print(f"📍 Location: {city}")
        print(f"🎓 Experience: {experience}")
        print(f"\n📋 Job Listings Preview:")
        print(df[["Searched Job Title", "Job Title", "Company Name", "Location", "Job Portal"]].to_string(index=False))
        
        save_to_json(all_jobs)
        save_to_excel(all_jobs)
        print("\n🎯 Results saved in /output as jobs.json and jobs.xlsx")
    else:
        print("\n⚠️ No jobs found. Please try different search criteria.")

if __name__ == "__main__":
    main()
