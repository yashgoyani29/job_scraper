# import requests
# from bs4 import BeautifulSoup

# def scrape_freshersworld(designation, city, experience):
#     url = f"https://www.freshersworld.com/jobs/jobsearch/{designation.replace(' ', '-')}-jobs-in-{city.replace(' ', '-')}"
#     print(f"🔎 Scraping: {url}")

#     try:
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         response.raise_for_status()
#     except Exception as e:
#         print("❌ Error fetching Freshersworld page:", e)
#         return []

#     soup = BeautifulSoup(response.text, "html.parser")
#     job_cards = soup.find_all("div", class_="job-container")
#     jobs = []

#     if not job_cards:
#         print("⚠️ No job cards found — structure may have changed.")
#         return jobs

#     for job in job_cards:
#         try:
#             title_tag = job.find("h2")
#             company_tag = job.find("h3", class_="latest-jobs-title font-16 margin-none inline-block company-name")
#             salary_tag = job.find("span", class_="qualifications display-block modal-open pull-left job-details-span")
#             location_tag = job.find("a", class_="bold_font")
#             exp_tag = job.find("span", class_="experience job-details-span")
#             date_tag = job.find("span", class_="ago-text")
#             link_tag = job.find("a", class_="job-title", href=True)

#             title = title_tag.get_text(strip=True) if title_tag else "N/A"
#             company = company_tag.get_text(strip=True) if company_tag else "N/A"
#             salary = salary_tag.get_text(strip=True) if salary_tag else "Not Mentioned"
#             location = location_tag.get_text(strip=True) if location_tag else city
#             exp_required = exp_tag.get_text(strip=True) if exp_tag else experience
#             posted = date_tag.get_text(strip=True) if date_tag else "Recently Posted"
#             link = f"https://www.freshersworld.com{link_tag['href']}" if link_tag else "N/A"

#             jobs.append({
#                 "Job Title": title,
#                 "Company Name": company,
#                 "Location": location,
#                 "Experience Required": exp_required,
#                 "Salary": salary,
#                 "Posted Date": posted,
#                 "Job Portal": "Freshersworld",
#                 "Job URL": link,
#             })
#         except Exception as e:
#             print("⚠️ Error reading a job card:", e)
#             continue

#     print(f"✅ Found {len(jobs)} jobs from Freshersworld")
#     return jobs


import requests
from bs4 import BeautifulSoup

def scrape_freshersworld(designation, city, experience):
    """
    Scrapes job listings from Freshersworld (updated structure Dec 2025)
    """
    url = f"https://www.freshersworld.com/jobs/jobsearch/{designation.replace(' ', '-')}-jobs-in-{city.replace(' ', '-')}"
    print(f"🔎 Scraping: {url}")

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        print("❌ Error fetching Freshersworld page:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="job-container")

    if not job_cards:
        print("⚠️ No job cards found — structure may have changed.")
        return []

    jobs = []
    for job in job_cards:
        try:
            # Title - try multiple selectors
            title_tag = job.find("h2") or job.find("h3", class_="job-title") or job.find("a", class_="job-title")
            if not title_tag:
                title_tag = job.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            # Company
            company_tag = job.find("h3", class_="latest-jobs-title font-16 margin-none inline-block company-name")
            if not company_tag:
                company_tag = job.find("h3", class_="company-name") or job.find("span", class_="company-name")
            company = company_tag.get_text(strip=True) if company_tag else "N/A"

            # Location
            location_tag = job.find("a", class_="bold_font")
            location = location_tag.get_text(strip=True) if location_tag else city

            # Experience
            exp_tag = job.find("span", class_="experience job-details-span")
            exp = exp_tag.get_text(strip=True) if exp_tag else experience

            # Posted Date
            date_tag = job.find("span", class_="ago-text")
            posted = date_tag.get_text(strip=True) if date_tag else "Recently Posted"
            
            # Salary
            salary_tag = job.find("span", class_="qualifications display-block modal-open pull-left job-details-span")
            salary = salary_tag.get_text(strip=True) if salary_tag else "Not Mentioned"

            # Job Link - try multiple selectors
            link_tag = job.find("a", class_="apply-button") or job.find("a", class_="job-title", href=True)
            if link_tag and link_tag.has_attr("href"):
                href = link_tag["href"]
                link = href if href.startswith("http") else f"https://www.freshersworld.com{href}"
            else:
                link = "N/A"

            jobs.append({
                "Job Title": title,
                "Company Name": company,
                "Location": location,
                "Experience Required": exp,
                "Salary / Stipend": salary,
                "Skills / Role": "N/A",  # Freshersworld doesn't typically show skills in listing
                "Duration": "N/A",  # Not applicable for jobs
                "Posted Date": posted,
                "Job Portal": "Freshersworld",
                "Job URL": link
            })
        except Exception as e:
            print("⚠️ Error parsing a job card:", e)
            continue

    print(f"✅ Found {len(jobs)} jobs from Freshersworld")
    return jobs
