# 💼 Job Aggregation Tool
###### Developed By : Yash Goyani
A robust Python-based web scraping application designed to aggregate job and internship listings from multiple portals (Internshala and Freshersworld) based on user-defined criteria.

## 🚀 Overview
This tool allows users to search for jobs by Designation, City, and Experience Level. It dynamically scrapes data, cleans and normalizes the results, and provides a unified interface to view and download the data in JSON and Excel formats.

## 🌟 Features

### 🚀 Scraping & Core Logic
- **Dual Source:** Aggregates data from Internshala & Freshersworld.
- **Dynamic Queries:** Builds search URLs based on user inputs.
- **Resilient Headers:** Uses User-Agents to avoid detection.
- **Pagination:** Scans multiple result pages.

### 📊 Data Management
- **Normalization:** Standardizes Salary/Stipend fields across platforms.
- **Deduplication:** Removes duplicate entries automatically.
- **Structured Storage:** Saves data into `output/` folder instantly.

### 💻 User Experience
- **Web UI:** Interactive dashboard built with Streamlit.
- **CLI Mode:** Command-line support via `main.py`.
- **Downloadable Reports:** One-click Excel and JSON downloads.

# 🌐 Supported Job Portals
The application is currently integrated with the following portals:

- **Internshala:** https://www.internshala.com/
- **Freshersworld:** https://www.fresherworld.com/

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Web Scraping:** BeautifulSoup4 & Requests
- **Data Handling:** Pandas
- **Frontend UI:** Streamlit
- **Export Formats:** JSON, Excel (OpenPyXL)

## 📁 Project Structure
Plaintext
```bash 
job_scraper/
│
├── scraper/
│   ├── freshersworld_scraper.py  # Logic for Freshersworld.com
│   └── internshala_scraper.py    # Logic for Internshala.com
│
├── utils/
│   └── formatter.py             # Data conversion (JSON/Excel)
│
├── output/                      # Generated data files
│   ├── jobs.json
│   └── jobs.xlsx
│
├── app.py                       # Streamlit Web Interface
├── main.py                      # CLI Version
└── README.md                    # Documentation
```

## ⚙️ How to Run the Project
### 1. Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment.

### 2. Install Dependencies
Run the following command to install the required libraries:

Bash
```bash
pip install requests beautifulsoup4 pandas streamlit openpyxl
```
### 3. Running the Application
You can run the tool in two ways:

##### Option A: Web Interface (Recommended)
This provides a modern, interactive dashboard.
```bash
Bash
streamlit run app.py
```
##### Option B: Command Line Interface (CLI)
For a quick terminal-based search.

Bash
```bash
python main.py
```
## 🔍 Key Features
Smart Portal Selection: Automatically queries Internshala for "Fresher" roles while targeting Freshersworld for all experience levels.

Data Normalization: Merges salary and stipend fields into a single "Salary / Stipend" column for consistency.

Deduplication: Automatically removes duplicate listings based on Job Title and Company Name.

Dynamic UI: Built-in tabs to filter results by portal within the web app.

## ⚠️ Challenges Faced & Solutions
Anti-Scraping Measures: Portals often block script requests. Solution: Implemented realistic User-Agent headers and added time.sleep() delays to mimic human browsing.

- **Dynamic Selectors:** Job portals frequently change their HTML structure. Solution: Implemented "Fallback Selectors" in the scraping logic to try multiple class names and tags if the primary one fails.

- **Data Inconsistency:** Different sites use different labels for salary. Solution: Created a normalization utility in the Pandas pipeline to unify these fields before export.
- Multi-portal scraping.
- Deduplication of job results.
- Export functionality for data analysis.
- Fallback HTML selectors for high reliability.
