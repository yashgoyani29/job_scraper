from scraper.freshersworld_scraper import scrape_freshersworld
from scraper.internshala_scraper import scrape_internshala
from utils.formatter import save_to_json, save_to_excel

def main():
    print("===== JOB AGGREGATION TOOL =====")
    designation = input("Enter Job Title (e.g., Python Developer): ")
    city = input("Enter City / Location (e.g., Bangalore): ")
    experience = input("Enter Experience Level (e.g., Fresher, 1–3 Years): ")

    print("\n🔍 Collecting job data... Please wait.\n")

    fw_jobs = scrape_freshersworld(designation, city, experience)
    intern_jobs = scrape_internshala(designation, city, experience)

    all_jobs = fw_jobs + intern_jobs

    print(f"\n✅ Total Jobs Collected: {len(all_jobs)}")

    save_to_json(all_jobs)
    save_to_excel(all_jobs)

    print("\n🎯 All done! Results saved in the /output folder.")
    print("📘 Files: output/jobs.json & output/jobs.xlsx")

if __name__ == "__main__":
    main()
