import requests
from bs4 import BeautifulSoup

def scrape_freshersworld(designation, city, experience):
    url = f"https://www.freshersworld.com/jobs/jobsearch/{designation.replace(' ', '-')}-jobs-in-{city.replace(' ', '-')}"
    print(f"🔎 Scraping: {url}")

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    except Exception as e:
        print("❌ Error fetching Freshersworld page:", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    job_cards = soup.find_all('div', class_='job-container')

    if not job_cards:
        print("⚠️ No job cards found — structure may have changed.")
        return jobs

    for job in job_cards:
        try:
            title_tag = job.find('h3', class_='latest-job-title')
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            company_tag = job.find('span', class_='job-company-name')
            company = company_tag.get_text(strip=True) if company_tag else "N/A"

            location_tag = job.find('span', class_='job-location')
            location = location_tag.get_text(strip=True) if location_tag else city

            link_tag = job.find('a', class_='job-title')
            link = "https://www.freshersworld.com" + link_tag['href'] if link_tag and link_tag.has_attr('href') else "N/A"

            salary_tag = job.find('span', class_='package')
            salary = salary_tag.get_text(strip=True) if salary_tag else "Not Mentioned"

            jobs.append({
                "Job Title": title,
                "Company Name": company,
                "Location": location,
                "Experience": experience,
                "Salary": salary,
                "Job Portal": "Freshersworld",
                "Job URL": link
            })
        except Exception as e:
            print("⚠️ Error reading a job card:", e)
            continue

    print(f"✅ Found {len(jobs)} jobs from Freshersworld")
    return jobs
