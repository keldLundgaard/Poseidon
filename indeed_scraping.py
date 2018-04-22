"""Indeed scraping of demand and supply side jobs."""
import csv
import time
import os

import requests
import bs4
from bs4 import BeautifulSoup
import numpy as np
from tqdm import tqdm
import pandas as pd


DATA_DIR = os.path.join(os.getcwd(), 'data')
try:
    os.makedirs(DATA_DIR)
except FileExistsError:
    pass

def extract_people_info(divs):
    results = []

    for div in divs:
        info = {}
        for exp_div in div.find_all("div", attrs={"class": "experience"}):
            info["experience"] = exp_div.contents[0]
        for span in div.find_all("span", attrs={"class": "location"}):
              info["location"] = span.text[3:]
        for span in div.find_all("span", attrs={"class": "company"}):
              info["company"] = span.text[3:]
        for span in div.find_all("span", attrs={"class": "degree"}):
              info["degree"] = span.text[2:]
        results.append(info)    
    
        time.sleep(0.01 * np.random.random()) # Time in seconds.
    return results


def get_supply_side(query):
    experience_dict = {
        'exp_1_11': '1-11', 
        'exp_12_24': '12-24', 
        'exp_25_60': '25-60', 
        'exp_61_120': '61-120', 
        'exp_121+': '121'
    }

    degree_dict = {
        'diploma': 'di', 
        'associate': 'as', 
        'bachelor': 'ba', 
        'master': 'ms', 
        'doctor': 'doc'
    }

    done_partitions = [
        fn.split('.tsv')[0] 
        for fn in os.listdir(DATA_DIR) 
        if (
            'tsv' in fn and 
            '_all_partitions' not in fn and 
            'resumes' in fn)]

    for experience_key, experience in experience_dict.items():
        for degree_key, degree in degree_dict.items():
            partition = '-'.join(['resumes', query, experience_key, degree_key])
            print(partition, flush=True)
            if partition in done_partitions:
                continue

            resumes_all_list = []
            for x in tqdm(range(0, 991, 10)):
                query_url = (
                    'https://www.indeed.com/resumes'
                    '?q={:}&co=US&rb=dt%3A{:}%2Cjtyp%3Aft%2Cyoe%3A{:}&start={:}').format(
                        query, degree, experience, x)

                page = requests.get(query_url)

                soup = BeautifulSoup(page.text, "html.parser")

                divs = soup.find_all(name="div", attrs={"class":"sre-content"})

                if not len(divs):
                    break
                resumes_all_list.append(extract_people_info(divs))

            if len(resumes_all_list):
                df_partition = pd.concat([pd.DataFrame(plist) for plist in resumes_all_list])
                df_partition.to_csv(os.path.join(DATA_DIR, partition + '.tsv'), sep='\t')
                print('Resumes {:,d}'.format(len(df_partition)), flush=True)
            else:
                print('No resumes')
                print(query_url)

    dfs = []
    for partition in done_partitions:
        df = pd.read_csv(os.path.join(DATA_DIR, partition + '.tsv'), sep='\t')
        df = df[['experience', 'location', 'company', 'degree']]
        df['partition'] = partition
        dfs.append(df.reset_index(drop=True))

    df_all_partitions = pd.concat(dfs)
    df_all_partitions.reset_index(drop=True)
    df_all_partitions.to_csv(os.path.join(
        DATA_DIR, 'resumes_' + query + '_all_partitions.tsv'), sep='\t')

    return df_all_partitions


def extract_jobs_from_page(soup):
    divs = soup.find_all(name="div", attrs={"class":"row"})
    
    job_obj_list = []
    for i, div in enumerate(divs):
        job_obj = {}
        # title
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            job_obj['title'] = a["title"]    

        # location
        for span in div.find_all("span", {"class": "location"}):
            job_obj['location'] = span.next_element

        # company name
        for a in div.find_all(name="a", attrs={"data-tn-element": "companyName"}):
            job_obj['company_name'] = a['href'].split('/')[-1]

        if not job_obj.get('company_name'):
            for span in div.find_all("span", {"class": "company"}):
                job_obj['company_name'] = span.next_element
                if job_obj['company_name'] == '\n':
                    if span.contents[1].attrs.get('href'):
                        job_obj['company_name'] = (
                            span.contents[1].attrs['href'].split('/')[-1])
                    
        if len(job_obj.get('company_name', '')) == 0:
            continue
        
        job_obj_list.append(job_obj)
        time.sleep(0.01 * np.random.random()) # Time in seconds.
    return job_obj_list



#This function extracts Job data from a webpage
def extract_job_title_from_result(soup):
    listOfDict = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        # Initiate empty object to hold data for a job
        jobDict = {}

        # Fetch Job Title
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobDict["jobTitle"] = a["title"]

        # Fetch Job Location
        for span in div.find_all("span", attrs={"class": "location"}):
          jobDict["location"] = span.text

        # Fetch Company name
        comps = div.findAll("span", attrs={"class": "company"})
        for a in comps:
            compStr = ''
            compStr = a.text.replace(" ", "")
            compStr = compStr.replace("\n", "")
            jobDict["company"] = compStr

        #Append this job to our list of jobs
        listOfDict.append(jobDict)
        time.sleep(0.01 * np.random.random()) # Time in seconds.
    return listOfDict


def get_demand_side_jobs(query):
    done_partitions = [
        fn.split('.tsv')[0] 
        for fn in os.listdir(DATA_DIR) 
        if (
            'tsv' in fn and 
            '_all_partitions' not in fn and 
            'resumes' not in fn)]

    levels = ['entry_level', 'mid_level', 'senior_level']
    salaries = ['$70,000', '$90,000', '$100,000', '$110,000', '$120,000']

    for level in levels:
        for salary in salaries:
            partition = '-'.join([query, level, salary])
            print(partition, flush=True)
            if partition in done_partitions:
                continue

            jobs_all_list = []
            for x in tqdm(range(0, 991, 10)):
                #     query_url = "https://www.indeed.com/jobs?q={:}&&start={:}".format(query, x)
                query_url = "https://www.indeed.com/jobs?q={:}+{:}&jt={:}&explvl={:}&&start={:}".format(
                    query, salary, job_type, level, x)

                page = requests.get(query_url)

                soup = BeautifulSoup(page.text, "html.parser")

                jobs_all_list.append(indeed_scraping.extract_jobs_from_page(soup))

            df_partition = pd.concat([pd.DataFrame(plist) for plist in jobs_all_list])
            df_partition.to_csv(os.path.join(DATA_DIR, partition + '.tsv'), sep='\t')
    dfs = []
    for partition in done_partitions:
        df = pd.read_csv(os.path.join(DATA_DIR, partition + '.tsv'), sep='\t')
        df = df[['company_name', 'location', 'title']]
        df['partition'] = partition
        dfs.append(df.reset_index(drop=True))

    df_all_partitions = pd.concat(dfs)
    df_all_partitions.to_csv(os.path.join(DATA_DIR, query + '_all_partitions.tsv'), sep='\t')         
    return df_all_partitions

if __name__ == '__main__':
    pass