import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def scrape_internshala(designation, city, experience):
    """
    Scrapes job and internship listings from Internshala.
    Automatically goes through multiple pages.
    Extracts Job Title, Company Name, Location, Stipend/Salary, and Job URL.
    """

    base_url = "https://internshala.com/internships/"
    query = f"{designation.replace(' ', '-')}-internship-in-{city.replace(' ', '-')}"
    print(f"🔎 Scraping: {base_url}{query}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    jobs = []

    # Pagination: scrape up to 3 pages
    for page in range(1, 4):
        url = f"{base_url}{query}/page-{page}/"
        print(f"➡️ Scraping page {page}: {url}")
        time.sleep(1)

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"⚠️ Skipping page {page}, status {response.status_code}")
                continue
        except Exception as e:
            print(f"❌ Error fetching page {page}:", e)
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="individual_internship")

        if not job_cards:
            print(f"⚠️ No job cards found on page {page}")
            break

        for job in job_cards:
            try:
                title_tag = job.find("h3", class_="job-internship-name")
                title = title_tag.get_text(strip=True) if title_tag else None

                company_tag = job.find("p", class_="company-name")
                company = company_tag.get_text(strip=True) if company_tag else None

                location_tag = job.find("a", class_="location_link")
                location = location_tag.get_text(strip=True) if location_tag else city

                stipend_tag = job.find("span", class_="stipend")
                salary = stipend_tag.get_text(strip=True) if stipend_tag else "Not Mentioned"

                link_tag = job.find("a", href=True)
                link = f"https://internshala.com{link_tag['href']}" if link_tag else None

                if not (title and company and link):
                    continue

                jobs.append({
                    "Job Title": title,
                    "Company Name": company,
                    "Location": location,
                    "Experience": experience,
                    "Salary": salary,
                    "Job Portal": "Internshala",
                    "Job URL": link
                })
            except Exception as e:
                print("⚠️ Error parsing job card:", e)
                continue

    print(f"✅ Found {len(jobs)} jobs from Internshala")
    return jobs
