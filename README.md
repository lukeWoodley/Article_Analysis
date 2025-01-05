

# Article Analysis Automation Project

## Overview

This Python project automates the process of analyzing articles using OpenAI's ChatGPT API, Selenium, and OpenPyxl. It retrieves articles based on a search query, processes them to extract insights, and saves the results in an Excel file for further analysis.

## Features

- **Automated Web Scraping**: Utilizes Selenium to search for articles and scrape their content.
- **Content Analysis**: Analyzes articles using the OpenAI GPT-4 model to classify content, summarize it, and extract relevant metadata.
- **Excel Reporting**: Generates a comprehensive Excel report with the processed data, including customizable column headers and automatic formatting.
- **Dynamic Querying**: Supports dynamic query modifications to target specific topics and date ranges.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lukeWoodley/Article_Analysis
   cd https://github.com/lukeWoodley/Article_Analysis
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the ChromeDriver compatible with your Chrome version and place it in your system's PATH or specify its location in the code.

4. Set up your OpenAI API key:
   Replace the placeholder `""` in the script with your actual OpenAI API key.

## Usage

1. **Configure the Search Query**:  
   Modify the `search_query` variable in the script to tailor the articles you want to analyze.

2. **Run the Script**:  
   Execute the script:
   ```bash
   python article_analysis.py
   ```

3. **Output**:  
   The processed results will be saved in an Excel file named in the format `article_analysis_YYYYMMDD_HHMMSS.xlsx`.

## File Structure

- **Main Script**:  
  Contains the core logic for article scraping, analysis, and data storage.
  
- **Excel Output**:  
  Generated Excel files containing the analyzed data.

## Customization

- **Headers**:  
  Modify the `checkbox_headers` and `primary_description_map` dictionaries to adjust the classifications and criteria used for article analysis.

- **Search Engine**:  
  Adjust the Selenium configuration to work with different search engines or additional filtering.

## Dependencies

- `selenium`  
- `openai`  
- `openpyxl`  
- `re`  
- `datetime`  

Install these using the `requirements.txt` file.

## Important Notes

- **API Usage**: Ensure your OpenAI API key has sufficient credits and permissions to handle the volume of articles.
- **Timeouts and Errors**: The script is configured to handle timeouts and unexpected errors during scraping and processing. Adjust timeouts as necessary for your environment.

## Potential Improvements

- Add support for parallel article processing to increase efficiency.
- Extend to other article sources or databases for broader analysis.
- Incorporate NLP techniques for more advanced insights.

## License

This project is open-source and available under the MIT License.








---

For any issues or questions, feel free to open an issue in the repository.