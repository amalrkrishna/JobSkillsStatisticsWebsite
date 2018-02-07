
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np

# if it goes to a page directly inside of indeed, we can search for the "job summary" <div> and use a try-except block to handle
# This'll cut down on scanning time, and should reduce the errors caused by HTML script still being left in

# A couple more data points need to be scrape from each page (sponsored status, date, location)


#  Need to have a logic test that can identify when the last page has been reached, so searching can stop.
#  Oddly the indeed site will kick back to either the second to last, or to the last page page for search calls exceeding the page limit.
#  Cannot simply compare the HTML of current page to previous pages to check if page has been revisited (since ads and sponsored content change every time)
#  I assume that this will have to be fixed by:
#           1) stopping when a post has already been found (will probably get duplicates on soponsored content)
#           2 ) identifying using the counter on the botton of the page


def list_to_dict(target_list):    # Creates an dictionary for counting, with each pair as key:0
    target_list = list({ str(target_list[x].lower())for x in range(len(target_list))})
    return {target_list[x] : 0 for x in range(len(target_list))}


def incr_dict(dict, target_text):
    for x in dict.keys():
        if x in target_text:
            dict[x] += 1
    return(dict)


def column(matrix, i):
    return [row[i] for row in matrix]


data_science_skills_list = ["Python", 'sql', "hadoop", " R ", "C#", "SAS", "C++", "Java ",
                            "Matlab", "Hive", "Excel", "Perl", "Mapreduce", "noSQL",   #
                            "Spark", "Pig", "Ruby", "JavaScript", "HBase", "Mahout",   #
                            "Tableau", "Scala", "Cassandra", "machine learning" ]      #

global list_spot
global matrix_counter

def scrape(job_title="data analyst", job_location = "Boston, MA"):

    print("\nSearching for '" + job_title + "' jobs in the '" + job_location + "' area...\n")

    matrix_counter = 0
    job_page_soup_list = []


    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    job_location = job_location.replace(" ", "+")    # format the job location so that it can be inserted into the indeed url
    job_location = job_location.replace(",", "%2C")

    url_list = []
    page_counter = 0

    for page in range(50):  # needs to be changed to a while loop later on (while page != notfound)
        counter = page * 10
        url = "https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(job_location) + "&start=" + str(counter)
        url_list.append(url)

    for x in range(30):
        url = url_list[x]
        print("\nSearching URL: \n" + url + "\n")


        page = requests.get(url)                          #conducting a request of the stated URL above:
        soup = BeautifulSoup(page.text, "html.parser")    #specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
        job_page_soup_list.append(soup)
     #   print(soup.prettify())                            #printing soup in a more structured tree format that makes for easier reading


        # Create a global 2d array to hold all job data.  (might want to eventually upgrade to a data frame)

        w, h = 10, 5000;
        global job_data_matrix
        job_data_matrix = [[0 for x in range(w)] for y in range(h)]


        jobs = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
          for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])


        companies = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            company = div.find_all(name="span", attrs = {"class":"company"})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs = {"class":"result - link - source"})
                for span in sec_try:
                    companies.append(span.text.strip())


        post_urls=[]
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                base_url = (a["href"])
                post_urls.append(" http://indeed.com"+str(base_url))



    ########################################################################################################################

        # Time since job posting was posted to indeed                     # Needs be added  (lots of nesting required)
                                                                            # Note some of the sponsored contents do not have data, or its in a different spot
        dates = []
        for a in div.find_all(name="span", attrs={"class":"date"}):
            print(a["date"])

    ########################################################################################################################

        salaries = []
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            try:
                salaries.append(div.find("nobr").text)
            except:
                try:
                    div_two = div.find(name="div", attrs={"class": "sjcl"})
                    div_three = div_two.find("div")
                    salaries.append(div_three.text.strip())
                except:
                    salaries.append("No Salary Provided")


        list_spot = 0

        for x in range((len(jobs))):
            job_data_matrix[x + list_spot][0] = jobs[x]
            job_data_matrix[x + list_spot][1] = companies[x]
            job_data_matrix[x + list_spot][2] = salaries[x]
            # job_data_matrix[x][3] = location          # Needs to be added
     #       job_data_matrix[x][3] = dates              # NEEDS FIXING
            job_data_matrix[x+list_spot][4] = post_urls[x]

            try:
                post_page = requests.get(job_data_matrix[x][4])
                job_soup = BeautifulSoup(post_page.text, "html.parser")    #Ideally we should seek to id the description class indeed <div>s to minimize scanning time
                job_soup = job_soup.get_text().lower()
            except:
                continue


            job_soup = job_soup.replace(",", " ")
            job_soup = job_soup.replace(".", " ")
            job_soup = job_soup.replace(";", " ")

            data_science_skills_dict = list_to_dict(data_science_skills_list)
            job_data_matrix[x+list_spot][5] = incr_dict(data_science_skills_dict, job_soup)


            #print ( "Job Title: " + job_data_matrix[x + list_spot][0] + "\t" + "Company: " + job_data_matrix[x + list_spot][1])
            #print(str(job_data_matrix[x][5]))
            matrix_counter += 1


    print("\nJob search finished:")
    return(job_data_matrix)

jobMatrix = scrape("data scientist", "Boston, MA")
print(jobMatrix)