
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import numpy as np
np.set_printoptions(threshold=np.inf)

class JobData():
    def __init__(self):
        self.company = ""
        self.jobTitle = ""
        self.salary = ""
        self.location = ""
        self.url = ""
        self.skills = []
        
    @classmethod
    def fromParameters(cls, company, jobTitle, salary, location, url):
        cls.company = company
        cls.jobTitle = jobTitle
        cls.salary = salary
        cls.location = location
        cls.url = url
        cls.skills = []
        return cls
    


def main():
    returned_job_matrix = scrape("data scientist", "Boston, MA")
    returned_job_matrix = np.array(returned_job_matrix)                             # convert job_matrix to a numpy array
    print("\n", col_dict_to_array(returned_job_matrix,5))                           # remove_rows for which there were scraping errors
    returned_job_matrix = remove_empty_rows(returned_job_matrix, 5)
    df = pd.DataFrame(returned_job_matrix)
    df.to_csv("jobs_matrix.csv")

####################################################################################################################################################3
#
#  TO DO:
#
######################################################################################################################################################


# TARGETED TEXT FROM POST SITE:
# if it goes to a page directly inside of indeed, we can search for the "job summary" <div> and use a try-except block to handle
# This'll cut down on scanning time, and should reduce the errors caused by HTML script still being left in

# INCREASE SCRAPED FIELDS FROM EACH PAGE:
# A couple more data points need to be scrape from each page (sponsored status, date, location)


#  FINAL PAGE DETECTION:
#  Need to have a logic test that can identify when the last page has been reached, so searching can stop.
#  Oddly the indeed site will kick back to either the second to last, or to the last page page for search calls exceeding the page limit.
#  Cannot simply compare the HTML of current page to previous pages to check if page has been revisited (since ads and sponsored content change every time)
#  I assume that this will have to be fixed by:
#           1) stopping when a post has already been found (will probably get duplicates on sponsored content)
#           2 ) identifying using the counter on the bottom of the page


#  CLEANSING FUNCTION:
#  Need to have a function that will
#       1) remove blank rows from job_data_matrix,
#       2) remove incomplete rows where the title, company was found, but the post URL was not able to be parsed
#       3) remove duplicate rows (i.e. identical posts)

####################################################################################################################################################


def col_dict_to_array(dict, colum_num=5):
    keys = list(dict[0][colum_num].keys())    # extract the keys
    cum_dict = list_to_dict(keys)             # cumulative dictionary
    for x in range(0,5000):
        if dict[x][colum_num] != 0:
            for y in keys:                          # if the job_title column is not empty
                if dict[x][colum_num][y] == 1:
                    cum_dict[y] += 1
        else:
            print(cum_dict)
            return(dict)


def remove_empty_rows(array, col = 5):
    count_rows = 0
    print("shape is:", str(array.shape[0]-1))
    for x in range ((array.shape[0])-1):
        count_rows += 1
        if array[x][0] != 0 and array[x][col] == 0:
            np.delete(array, col, 0)
    print(count_rows)
    return(array)




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


data_science_skills_list = ["Python", 'sql', "hadoop", " R ", "C#", " SAS ", "C++", "Java ",
                            "Matlab", "Hive", "Excel", "Perl", "Mapreduce", "noSQL",   #
                            "Spark", "Pig", "Ruby", "JavaScript", "HBase", "Mahout",   #
                            "Tableau", "Scala", "Cassandra", "machine learning", "PhD", "Master's" ]      #


global list_spot
global matrix_counter


def scrape(job_title="data analyst", job_location = "Boston, MA"):

    print("\nSearching for '" + job_title + "' jobs in the '" + job_location + "' area...\n")

    w, h =6, 6000;
    global job_data_matrix                                                   # Define a matrix of enough rows to hold all scraped job posts
    job_data_matrix = [[0 for x in range(w)] for y in range(h)]

    list_spot = 0
    matrix_counter = 0
    job_page_soup_list = []
    url_list = []


    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    job_location = job_location.replace(" ", "+")    # format the job location so that it can be inserted into the indeed url
    job_location = job_location.replace(",", "%2C")


# I think we can probably combine these two for loops into a single loop

    for page in range(10):  #
        counter = page * 10
        url = "https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(job_location) + "&start=" + str(counter)
        url_list.append(url)

    for x in range(10):           # number of pages to be scraped
        url = url_list[x]
        print("\nSearching URL: \n" + url + "\n")


        page = requests.get(url)                          #conducting a request of the stated URL above:
        soup = BeautifulSoup(page.text, "html.parser")    #specifying a desired format of using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
        job_page_soup_list.append(soup)
     #   print(soup.prettify())                            #printing soup in a more structured tree format that makes for easier reading



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


        locations = []
        spans = soup.find_all(name="span", attrs = {"class" : "location"})
        for span in spans:
            locations.append(span.text)




        salaries = []
        for div in soup.find_all(name="div", attrs={"class" : "row"}):
            try:
                salaries.append(div.find("nobr").text)
            except:
                try:
                    div_two = div.find(name="div", attrs={"class": "sjcl"})
                    div_three = div_two.find("div")
                    salaries.append(div_three.text.strip())
                except:
                    salaries.append("No Salary Provided")


        list_spot += matrix_counter
        matrix_counter = 0

        for x in range((len(jobs))):
            job_data_matrix[x + list_spot][0] = jobs[x]
            job_data_matrix[x + list_spot][1] = companies[x]
            job_data_matrix[x + list_spot][2] = salaries[x]
            job_data_matrix[x + list_spot][3] = locations[x]
      #      job_data_matrix[x][3] = dates              # NEEDS FIXING
            job_data_matrix[x+list_spot][4] = post_urls[x]

            try:
                post_page = requests.get(job_data_matrix[x+list_spot][4])
                print(post_page.text)
                job_soup = BeautifulSoup(post_page.text, "html.parser")    #Ideally we should seek to id the description class indeed <div>s to minimize scanning time
                job_soup = job_soup.get_text().lower()
            except:
                print("x:" + str(x) + "  list_spot:" + str(list_spot) + " matrix_counter: " + str(matrix_counter))
                print(" URL ERROR!!! \n")
        


            job_soup = job_soup.replace(",", " ")
            job_soup = job_soup.replace(".", " ")
            job_soup = job_soup.replace(";", " ")

            data_science_skills_dict = list_to_dict(data_science_skills_list)
            job_data_matrix[x+list_spot][5] = incr_dict(data_science_skills_dict, job_soup)

            #print()
            #print ( "Job Title: " + job_data_matrix[x + list_spot][0] + "\t" + "Company: " + job_data_matrix[x + list_spot][1] + "\t"+ "Location " + job_data_matrix[x + list_spot][3] )
            #print(str(job_data_matrix[x+ list_spot][5]))
            matrix_counter += 1




    print("\nJob search finished:")
    print("Jobs Found: " + str(list_spot + matrix_counter))
    return(job_data_matrix)





# print(np.matrix(returned_job_matrix))

# df = pd.DataFrame(returned_job_matrix)
# df.to_csv("jobs_matrix.csv")

def getJobSkills(pageText):   
    job_soup = BeautifulSoup(pageText, "html.parser")    #Ideally we should seek to id the description class indeed <div>s to minimize scanning time
    job_soup = job_soup.get_text().lower()
    
    job_soup = job_soup.replace(",", " ")
    job_soup = job_soup.replace(".", " ")
    job_soup = job_soup.replace(";", " ")

    data_science_skills_dict = list_to_dict(data_science_skills_list)
    return incr_dict(data_science_skills_dict, job_soup)

def getJobs(pageText):
    #w, h =6, 6000;
    #job_data_matrix = [[0 for x in range(w)] for y in range(h)]
    list_spot = 0
    matrix_counter = 0
    
    soup = BeautifulSoup(pageText, "html.parser")
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


    locations = []
    spans = soup.find_all(name="span", attrs = {"class" : "location"})
    for span in spans:
        locations.append(span.text.strip())




    salaries = []
    for div in soup.find_all(name="div", attrs={"class" : "row"}):
        try:
            salaries.append(div.find("nobr").text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class": "sjcl"})
                div_three = div_two.find("div")
                salaries.append(div_three.text.strip())
            except:
                salaries.append("No Salary Provided")


    list_spot += matrix_counter
    matrix_counter = 0

    job_data_list = []
    
    for x in range((len(jobs))):
        job_data_list.append(JobData.fromParameters(companies[x], 
                                                    jobs[x], 
                                                    salaries[x], 
                                                    locations[x], 
                                                    post_urls[x]))
       
        matrix_counter += 1
    print("\nJob search finished:")
    print("Jobs Found: " + str(list_spot + matrix_counter))

    return(job_data_list)
    
    
def getDataFromJobAndRegion(job_title="data analyst", job_location = "Boston, MA", page_count = 10):
    
    job_title = job_title.replace(" ", "+")
    job_location = job_location.replace(" ", "+")
    job_location = job_location.replace(",", "%2C")

    for page in range(page_count):
        counter = page * 10
        url = "https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(job_location) + "&start=" + str(counter)
        print("\nSearching URL: \n" + url + "\n")
        page = requests.get(url)       
        job_data_list = getJobs(page.text)
        for job_data in job_data_list:
            try:
                post_page = requests.get(job_data.post_url)
                job_data.skills = getJobSkills(post_page.text)
            except:
                print(" URL ERROR!!! \n")
                
                
    
if __name__ == '__main__':
    main()