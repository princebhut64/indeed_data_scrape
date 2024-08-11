from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv,time
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#setting driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument('--disable-gpu')


class indeed_data:
    #creating driver
    def __init__(self):
        # Initialize any instance variables if needed
        pass

    def remove_extra_blank_lines(text):
        lines = text.splitlines()
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = '\n'.join(non_empty_lines)
        return cleaned_text

    def get_data():
        driver = webdriver.Chrome(options=options)
        csv_file_path = r'D:/python/F-Data/Scraping/indeed/jobs_data.csv'
        # Check if the CSV file already exists to determine if we need to write the header
        write_header = not os.path.exists(csv_file_path)
        city_list = []
        Possition_list = []
        result_counts = 100
        start_from = 10
        while start_from < result_counts:
            url = f"https://in.indeed.com/jobs?q=php+developer&l=Ahmedabad&start={start_from}&vjk=712706782a924cbf"
            start_from = start_from + 10
            driver.get(url)
            wait = WebDriverWait(driver, 5)
            #searching in a bar
            time.sleep(10)
            search_bar = driver.page_source
            soup1 = BeautifulSoup(search_bar, 'lxml')
            buttons = soup1.find_all('a', role='button')
            for data_url in buttons:
                driver.get(urljoin('https://in.indeed.com/',data_url.get('href')))
                post_page_data = BeautifulSoup(driver.page_source, 'lxml')
                if post_page_data:
                    # getting job post
                    try:
                        job_title_element = post_page_data.find('h1').find('span')
                        if job_title_element:
                            job_title = job_title_element.text.strip()

                        job_location_element = post_page_data.find('div', {'data-testid': 'inlineHeader-companyLocation'})
                        if job_location_element:
                            job_location = job_location_element.find('div').text.strip()

                        company_element = post_page_data.find('div', {'data-company-name': 'true'})
                        if company_element:
                            cpn_name = company_element.find('a').text.strip()
                            cpn_url = company_element.find('a').get('href')

                        job_type_element = post_page_data.find('li', {'data-testid': 'list-item'})
                        if job_type_element:
                            job_type = job_type_element.text.strip()

                        job_description_element = post_page_data.find('div', {'id': 'jobDescriptionText'})
                        if job_description_element:
                            job_description = indeed_data.remove_extra_blank_lines(job_description_element.get_text(separator='\n').strip())

                    except AttributeError as e:
                        print(f"Error processing element: {e}")
                        continue
                    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        # Write header row
                        if write_header:
                            writer.writerow(['Job Title', 'Job Location', 'Company Name', 'Company URL', 'Job Type', 'Job Description'])
                        # Write data row
                        writer.writerow([job_title, job_location, cpn_name, cpn_url, job_type, job_description])

indeed_data.get_data()