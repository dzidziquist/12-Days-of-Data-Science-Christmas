#import libraries 

import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from random import randint
from requests import get
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from time import time




class get_jobs:
    def __init__(self, no_of_jobs, url, chromedriver_path):

        self.no_of_jobs = no_of_jobs
        self.url = url 
        self.chromedriver_path = chromedriver_path

    def get_job_data(self, no_of_jobs,url, chromedriver_path):

        #Opening browser 
        driver = webdriver.Chrome(executable_path= chromedriver_path)
        driver.get(url)
        sleep(3)

        #action to automate mouse movement
        action = ActionChains(driver)
        
        

        i = 2
        while i <= (no_of_jobs/25): 
            driver.find_element_by_xpath('/html/body/main/div/section/button').click()
            i = i + 1
            sleep(5)


        # parsing the visible webpage using beautifulsoup
        pageSource = driver.page_source
        lxml_soup = BeautifulSoup(pageSource, 'lxml')

        # searching for all job containers
        job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')

        print('You are scraping information about {} jobs.'.format(len(job_container)))


        self.job_data = pd.DataFrame(pd.DataFrame(columns = ['Job ID','Date', 'Company Name', 'Post', 'Location','Description','Level', 'Type', 'Function',
                                                    'Industry']))


        # for loop for job title, company, id, location and date posted
        for job in job_container:
            
            # job title
            self.job_data['Post'] = job.find("span", class_="screen-reader-text").text

            job_id = []
            # linkedin job id
            job_ids = job.find('a', href=True)['href']
            job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)',job_ids)[0]
            job_id.append(job_ids)
            
            self.job_data['Job ID']= job_id
            
            # company name
            self.job_data['Company Name'] = job.select_one('img')['alt']
            

            
            # job location
            self.job_data['Location'] = job.find("span", class_="job-result-card__location").text

            
            # posting date
            self.job_data['Date'] = job.select_one('time')['datetime']


        # for loop for job description and criterias
        for x in range(1,len(job_id)+1):
            
            # clicking on different job containers to view information about the job
            job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(x)
            driver.find_element_by_xpath(job_xpath).click()
            sleep(3)
            
            # job description
            jobdesc_xpath = '/html/body/main/section/div[2]/section[2]/div'
            self.job_data['Description'] = driver.find_element_by_xpath(jobdesc_xpath).text

            # cleaning description column
            self.job_data['Description'] = self.job_data['Description'].str.replace('\n',' ')


            
            # job criteria container below the description
            job_criteria_container = lxml_soup.find('ul', class_ = 'job-criteria__list')
            all_job_criterias = job_criteria_container.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
            
            # Seniority level

            seniority_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[1]'
            self.job_data['Level'] = driver.find_element_by_xpath(seniority_xpath).text[16:]
         
            
            # Employment type
            type_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[2]'
            self.job_data['Type'] = driver.find_element_by_xpath(type_xpath).text[16:]
            
            
            # Job function
            function_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[3]'
            self.job_data['Function'] = driver.find_element_by_xpath(function_xpath).text[13:]
            
            
            # Industries
            industry_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[4]'
            self.job_data['Industry'] = driver.find_element_by_xpath(industry_xpath).text[11:]

            return self.job_data


