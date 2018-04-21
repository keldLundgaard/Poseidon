import requests
import bs4
from bs4 import BeautifulSoup
import csv

#This is the list that will hold the dictionary for each job
listOfDict = []

#URL to scrape data from
URL = "https://www.indeed.com/jobs?q=fintech&&start=%d"
# page = requests.get(URL)
# soup = BeautifulSoup(page.text, "html.parser")
#To print the soup in a more structured format
#print(soup.prettify())


def extract_jobs_from_page(soup):
    divs = soup.find_all(name="div", attrs={"class":"row"})

    job_obj_list = []

    for i, div in enumerate(divs):
        job_obj = {}
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            job_obj['title'] = a["title"]    
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
            break
        for span in div.find_all("span", {"class": "location"}):
            job_obj['location'] = span.next_element
        
        job_obj_list.append(job_obj)
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
        c = div.find_all("span", attrs={"class": "location"})
        for span in c:
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
    return listOfDict

if __name__ == '__main__':

    # X is our counter
    # newURL is each new URL to scrape
    x = 0
    newURL = ''
    while x < 991:
        newURL = URL % (x)
        print(newURL)
        #Fetch the page from the internet
        page = requests.get(newURL)

        #Parse the HTML
        soup = BeautifulSoup(page.text, "html.parser")

        #Extract all the relevant job details
        extract_job_title_from_result(soup)

        #Increment X to move to next page
        x += 10

    #Extract headers to put in as column names in our excel
    keys = listOfDict[0].keys()

    #Write each job entry to the excel file
    with open('jobCount.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(listOfDict)