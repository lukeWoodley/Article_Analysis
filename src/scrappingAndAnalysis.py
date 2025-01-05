import time
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
from openpyxl.styles import Alignment
from datetime import datetime
import re

# Add here your own chatgpt api key (If you don't have one create it at https://platform.openai.com/api-keys)
openai.api_key = ""

# Base name for the Excel file
excel_file_base = "article_analysis"

# Mapping of primary description numbers to text
primary_description_map = {
    0: "The article is primarily about the state of Israel, and the lives of Israelis.",
    1: "The article is primarily about Jews in Canada, or Jewish institutions in Canada.",
    2: "The article is primarily about Palestinians, or other Arabs, and the lives of Palestinians and other Arabs in the Middle East.",
    3: "The article is primarily about Palestinians or Arabs in Canada, or Palestinian institutions or Arab institutions in Canada.",
    4: "The article is primarily about the war between Israel and Hamas, Israel and Gaza, Israel and the Palestinians, or Israel and the Arabs.",
    5: "The article is about something else."
}

# Column headers for checkbox results
checkbox_headers = [
    "The article provides input or quotes from Israeli government sources, or an Israeli official.",
    "The article provides input or quotes from Jewish Canadians, or someone from a Jewish organization in Canada.",
    "The article provides input or quotes from someone from the Centre for Israel and Jewish Affairs (CIJA), B'nai Brith Canada, the Friends of Simon Wiesenthal Centre.",
    "The article provides input or quotes from someone from Independent Jewish Voices, or Independent Jewish Voices Canada.",
    "The article provides input or quotes from a Palestinian official, whether from Hamas, from the Palestinian Authority, or from another international Palestinian organization.",
    "The article provides input or quotes from a Palestinian in Canada, or someone from a Palestinian or Arab organization in Canada.",
    "The article provides input or quotes from someone from Canadians for Justice and Peace in the Middle East (CJPME), the National Council for Canadian Muslims (NCCM), the Palestinian Youth Movement (PYM).",
    "The article provides input or quotes from someone who is not clearly Israeli, Palestinian, or Arab, but who supports Israel's overall interests and objective.",
    "The article provides input or quotes from someone who is not clearly Israeli, Palestinian, or Arab, but who supports the Palestinians' overall interests and objectives."
]


# Function to process a single article with ChatGPT
def analyze_article(article_text):
    prompt = f"""
First, read the article below and determine which of the following statements is most true about the article.
Ignore any text that seems irrelevant, such as unrelated advertisements, links, or notices, and focus only on the main body of the article.
Choose the one item which best describes the article:
0. The article is primarily about the state of Israel, and the lives of Israelis.
1. The article is primarily about Jews in Canada, or Jewish institutions in Canada.
2. The article is primarily about Palestinians, or other Arabs, and the lives of Palestinians and other Arabs in the Middle East.
3. The article is primarily about Palestinians or Arabs in Canada, or Palestinian institutions or Arab institutions in Canada.
4. The article is primarily about the war between Israel and Hamas, Israel and Gaza, Israel and the Palestinians, or Israel and the Arabs.
5. The article is about something else.

Next, please indicate which of the following are true about the article. You may indicate all the items that apply:
{', '.join(f'{i}. {text}' for i, text in enumerate(checkbox_headers))}

Additionally, provide the following:
1. A 1-2 sentence summary of the article.
2. A phrase that summarizes the article.
3. Your level of certainty (1-100) about the correctness of the first question's answer.
4. The date of the article, if available.
5. The author of the article, if listed.

Article:
{article_text}

Please return your answer in this format:
[Primary description number]
[Numbers for all applicable items]
Summary: [1-2 sentence summary]
Phrase: [Phrase summarizing the article]
Certainty: [Certainty level, 1-100]
Date: [Date of the article]
Author: [Author of the article]
"""

    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system",
                   "content": "You are a helpful assistant that analyzes articles based on specific criteria."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']


# Function to save data to an Excel file
def save_to_excel(base_filename, headers, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.xlsx"

    # Create a new workbook
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Article Analysis"

    # Write headers
    sheet.append(headers)

    # Write data rows
    for row in data:
        sheet.append(row)

    # Set wrap text and center-align all cells
    alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in sheet.iter_rows():
        for cell in row:
            cell.alignment = alignment

    # Auto-adjust column widths
    for col in sheet.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        col_letter = col[0].column_letter
        sheet.column_dimensions[col_letter].width = max_length + 2  # Add padding

    # Save the workbook
    wb.save(filename)
    print(f"File saved as: {filename}")


# Set up Chrome options
options = Options()
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(15)

try:
    search_query = "israel OR palestine OR jewish OR palestinian after:2024-10-01 -video -audio -shorts -youtube site:cbc.ca"
    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.submit()
    time.sleep(3)

    articles = []
    data_rows = []

    for page in range(0, 3):  # Loop through the first 5 pages
        time.sleep(3)
        page_url = f"https://www.google.com/search?q={search_query}&start={page * 10}"
        driver.get(page_url)
        time.sleep(3)

        articles = driver.find_elements(By.CSS_SELECTOR, 'div.g')

        for article in articles:
            try:
                link_element = article.find_element(By.TAG_NAME, 'a')
                if link_element:
                    link = link_element.get_attribute('href')
                    print(f"Visiting: {link}")
                    driver.get(link)
                    time.sleep(3)

                    try:
                        title = driver.title
                        article_body = driver.find_element(By.TAG_NAME, 'body').text
                        analysis_result = analyze_article(article_body)
                        lines = analysis_result.strip().splitlines()

                        primary_description = int(re.search(r'\d+', lines[0]).group())
                        checkboxes = set(map(int, re.findall(r'\d+', lines[1])))

                        summary = re.search(r"Summary: (.+)", analysis_result).group(1).strip()
                        phrase = re.search(r"Phrase: (.+)", analysis_result).group(1).strip()
                        certainty = re.search(r"Certainty: (\d+)", analysis_result).group(1).strip()
                        date = re.search(r"Date: (.+)", analysis_result).group(
                            1).strip() if "Date:" in analysis_result else "N/A"
                        author = re.search(r"Author: (.+)", analysis_result).group(
                            1).strip() if "Author:" in analysis_result else "N/A"

                        row = [
                                  title,
                                  primary_description_map[primary_description],
                                  certainty,
                                  link,
                                  summary,
                                  phrase,
                                  date,
                                  author
                              ] + ["✔" if i in checkboxes else "" for i in range(len(checkbox_headers))]
                        data_rows.append(row)
                    except Exception as e:
                        print(f"Could not retrieve or process article from {link}: {e}")
                    driver.back()
                    time.sleep(3)
            except Exception as e:
                print(f"Error processing article: {e}")
finally:
    save_to_excel(
        excel_file_base,
        [
            "Title",
            "Article Description",
            "Certainty",
            "Link",
            "Summary",
            "Phrase",
            "Date",
            "Author"
        ] + checkbox_headers,
        data_rows
    )
    driver.quit()
