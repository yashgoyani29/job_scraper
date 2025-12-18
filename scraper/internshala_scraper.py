import requests
from bs4 import BeautifulSoup
import time

def scrape_internshala(designation, city, experience):
    base_url = "https://internshala.com/internships/"
    query = f"{designation.replace(' ', '-')}-internship-in-{city.replace(' ', '-')}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        )
    }

    print(f"🔎 Scraping: {base_url}{query}")
    jobs = []

    # Pagination (1–3)
    for page in range(1, 4):
        url = f"{base_url}{query}/page-{page}/"
        print(f"➡️ Page {page}: {url}")
        time.sleep(1)

        try:
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                continue
        except Exception as e:
            print("❌ Error fetching Internshala:", e)
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        job_cards = soup.find_all("div", class_="individual_internship")
        if not job_cards:
            break

        for j in job_cards:
            try:
                title_tag = j.find("h3", class_="job-internship-name")
                company_tag = j.find("p", class_="company-name")
                location_tag = j.find("a", class_="location_link") or j.find("span", class_="location")
                if not location_tag:
                    location_tag = j.find("span")
                posted_date = j.select_one('div.color-labels span') or j.find("span", class_="posted-by-name")
                stipend_tag = j.find("span", class_="stipend")
                duration_tag = j.find("div", class_="other_detail_item_row") or j.find("span", class_="duration")
                skills_tag = j.find("div", class_="round_tabs_container")
                # Find the main job link (usually in the title area)
                link_tag = j.find("a", class_="view_detail_button") or j.find("a", href=True)

                title = title_tag.get_text(strip=True) if title_tag else "N/A"
                company = company_tag.get_text(strip=True) if company_tag else "N/A"
                location = location_tag.get_text(strip=True) if location_tag else city
                posted = posted_date.get_text(strip=True) if posted_date else "Recently Posted"
                salary = stipend_tag.get_text(strip=True) if stipend_tag else "N/A"
                duration = duration_tag.get_text(strip=True) if duration_tag else "N/A"
                skills = ", ".join([s.get_text(strip=True) for s in skills_tag.find_all("span")]) if skills_tag else "N/A"
                
                if link_tag and link_tag.has_attr("href"):
                    href = link_tag["href"]
                    link = href if href.startswith("http") else f"https://internshala.com{href}"
                else:
                    link = "N/A"

                jobs.append({
                    "Job Title": title,
                    "Company Name": company,
                    "Location": location,
                    "Experience Required": experience,
                    "Salary / Stipend": salary,
                    "Skills / Role": skills,
                    "Duration": duration,
                    "Posted Date": posted,
                    "Job Portal": "Internshala",
                    "Job URL": link,
                })
            except Exception as e:
                print("⚠️ Error parsing job card:", e)
                continue

    print(f"✅ Found {len(jobs)} jobs from Internshala")
    return jobs


