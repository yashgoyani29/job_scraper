import requests
from bs4 import BeautifulSoup

def scrape_freshersworld(designation, city, experience):
    """
    Scrapes job listings from Freshersworld (updated structure Dec 2025)
    """
    url = f"https://www.freshersworld.com/jobs/jobsearch/{designation.replace(' ', '-')}-jobs-in-{city.replace(' ', '-')}"
    print(f"🔎 Scraping: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching Freshersworld page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Try multiple selectors for job cards (Freshersworld may use different structures)
    job_cards = soup.find_all("div", class_="job-container")
    
    # Try alternative selectors
    if not job_cards:
        job_cards = soup.find_all("div", class_="job-item")
    if not job_cards:
        job_cards = soup.find_all("div", class_="job-card")
    if not job_cards:
        job_cards = soup.find_all("div", class_="job-listing")
    if not job_cards:
        # Try finding by data attributes or other patterns
        job_cards = soup.find_all("div", {"data-job-id": True})
    if not job_cards:
        # Try finding job links and their parent containers
        job_links = soup.find_all("a", href=lambda x: x and "/job/" in x)
        if job_links:
            job_cards = [link.find_parent("div") for link in job_links if link.find_parent("div")]
            job_cards = [card for card in job_cards if card is not None]

    if not job_cards:
        # Debug: print some info about what we found
        all_divs = soup.find_all("div", class_=True)
        if all_divs:
            unique_classes = set([div.get("class")[0] if div.get("class") else "" for div in all_divs[:20]])
            print(f"⚠️ No job cards found. Found div classes: {list(unique_classes)[:10]}")
        else:
            print("⚠️ No job cards found — structure may have changed or no jobs available.")
        return []

    jobs = []
    for job in job_cards:
        try:
            # Title - try multiple selectors
            title_tag = (job.find("h2") or 
                        job.find("h3", class_="job-title") or 
                        job.find("a", class_="job-title") or
                        job.find("a", href=lambda x: x and "/job/" in x))
            if not title_tag:
                title_tag = job.find("h3") or job.find("h4")
            if not title_tag:
                # Try finding any link with job in href
                title_tag = job.find("a", href=lambda x: x and "job" in x.lower())
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            
            # Skip if we don't have a valid title
            if title == "N/A" or not title:
                continue

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

            jobs.append({
                "Job Title": title,
                "Company Name": company,
                "Location": location,
                "Experience Required": exp,
                "Salary / Stipend": salary,
                "Posted Date": posted,
                "Job Portal": "Freshersworld"
            })
        except Exception as e:
            print("⚠️ Error parsing a job card:", e)
            continue

    print(f"✅ Found {len(jobs)} jobs from Freshersworld")
    return jobs
