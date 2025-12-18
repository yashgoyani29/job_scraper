import requests
from bs4 import BeautifulSoup
import time

def scrape_internshala(designation, city, experience):
    """
    Scrapes internship/job listings from Internshala
    """
    base_url = "https://internshala.com/internships/"
    # Clean and format the query
    designation_clean = designation.replace(' ', '-').lower()
    city_clean = city.replace(' ', '-').lower()
    query = f"{designation_clean}-internship-in-{city_clean}"
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    print(f"🔎 Scraping Internshala: {base_url}{query}")
    jobs = []

    # Try first page without pagination, then paginate if needed
    for page in range(1, 4):
        if page == 1:
            url = f"{base_url}{query}"
        else:
            url = f"{base_url}{query}/page-{page}/"
        
        print(f"➡️ Page {page}: {url}")
        time.sleep(1.5)  # Slight delay to avoid rate limiting

        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200:
                if page == 1:
                    print(f"⚠️ Page {page} returned status {r.status_code}")
                break
        except Exception as e:
            print(f"❌ Error fetching Internshala page {page}: {e}")
            if page == 1:
                return []
            break

        soup = BeautifulSoup(r.text, "html.parser")
        
        # Try multiple selectors for job cards
        job_cards = soup.find_all("div", class_="individual_internship")
        if not job_cards:
            # Try alternative selector
            job_cards = soup.find_all("div", {"class": "internship_meta"})
        
        if not job_cards:
            if page == 1:
                print("⚠️ No job cards found on Internshala — structure may have changed or no results.")
            break

        for j in job_cards:
            try:
                # Title - try multiple selectors
                title_tag = (j.find("h3", class_="job-internship-name") or 
                           j.find("h4", class_="job-internship-name") or
                           j.find("a", class_="view_detail_button"))
                if title_tag and title_tag.name == "a":
                    title = title_tag.get_text(strip=True)
                else:
                    title = title_tag.get_text(strip=True) if title_tag else "N/A"

                # Company name
                company_tag = (j.find("p", class_="company-name") or 
                             j.find("a", class_="link_display_like_text") or
                             j.find("div", class_="company-name"))
                company = company_tag.get_text(strip=True) if company_tag else "N/A"

                # Location - improved selectors
                location_tag = (j.find("a", class_="location_link") or 
                             j.find("span", class_="location") or
                             j.find("div", id="location_names"))
                if not location_tag:
                    # Try finding location in detail row
                    location_div = j.find("div", class_="internship_details")
                    if location_div:
                        location_tag = location_div.find("span", class_="location")
                location = location_tag.get_text(strip=True) if location_tag else city

                # Posted date
                posted_date = (j.select_one('div.color-labels span') or 
                             j.find("span", class_="posted-by-name") or
                             j.find("div", class_="posted_by_container"))
                posted = posted_date.get_text(strip=True) if posted_date else "Recently Posted"

                # Stipend/Salary
                stipend_tag = (j.find("span", class_="stipend") or 
                             j.find("span", id="stipend") or
                             j.find("div", class_="stipend"))
                salary = stipend_tag.get_text(strip=True) if stipend_tag else "N/A"

                # Only add if we have at least a title
                if title != "N/A":
                    jobs.append({
                        "Job Title": title,
                        "Company Name": company,
                        "Location": location,
                        "Experience Required": experience,
                        "Salary / Stipend": salary,
                        "Posted Date": posted,
                        "Job Portal": "Internshala"
                    })
            except Exception as e:
                print(f"⚠️ Error parsing Internshala job card: {e}")
                continue

    print(f"✅ Found {len(jobs)} jobs/internships from Internshala")
    return jobs


