import matplotlib.pyplot as plt
plt.rcdefaults()
import copy
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import requests
import csv
import plotly
import operator
from fake_useragent import UserAgent
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='patryan117', api_key='4ShAMHvEZPvz1AdSEjGm')
import matplotlib.ticker as mtick
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import collections
import numpy as np
np.set_printoptions(threshold=np.inf)





def main():

    job_title = "registered nurse"
    job_title = format_job_title(job_title,True)  # Keep second quote layer for an exact string match, remove quotes to search for skills or industries
    matrix = scrape_salaries(str(job_title))
    df = pd.DataFrame(matrix)
    df.columns = ['State Abbreviation', 'State Name', "Job Count", 'Post per Salary Range', 'Posts per County', 'Posts per Company', 'Post per Experience Level', 'Posts per Jop Type', 'Mean Salary Per State'  ]
    df.to_csv("jobs_matrix.csv")
    FIPS_dict = get_FIPS_dict()
    populated_matrix = get_populated_FIPS_matrix(FIPS_dict,df,"blank_FIPS_matrix")
    make_county_cloropleth(populated_matrix, job_title)



def make_county_cloropleth(df_sample, job_title):


    colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
                  "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
                  "#08519c", "#0b4083", "#08306b"]

    endpts = list(np.linspace(1, 100, len(colorscale) - 1))
    fips = df_sample['FIPS'].tolist()
    values = df_sample['Job Post Count'].tolist()
    print(endpts)

    fig = ff.create_choropleth(
        fips=fips,
        values=values,
        binning_endpoints=endpts,
        colorscale=colorscale,
        show_state_data=True,
        show_hover=True,
        centroid_marker={'opacity': 0},
        asp=2.9, title= str(job_title) + " Job Posts per US County",    # put [1:-1] after job title to remove quotes in final post
        legend_title='No. of Posts'
    )

    py.plot(fig, filename='choropleth_full_usa')


def get_populated_FIPS_matrix(translation_dict, job_data_matrix, matrix_to_populate):

    matrix = pd.read_csv(str(matrix_to_populate)+'.csv')
    matrix_copy = copy.deepcopy(matrix)
    FIPS_dict = {}

    for x in range(50):
        print(x)
        state = str(job_data_matrix.iloc[x][0])
        print(state)
        town_list = list(job_data_matrix.iloc[x][4].keys())
        print(town_list)

        for y in range(len(town_list)):
            try:
                town = town_list[y]
                job_count = job_data_matrix.iloc[x][4][town]
                print(job_count)
                town_state = str(town + " " + state)
                print(town_state)
                FIPS = translation_dict[town_state]
                print(FIPS)

                if str(FIPS) not in FIPS_dict:
                    FIPS_dict[str(FIPS)] = 0

                if str(FIPS) in FIPS_dict:
                    FIPS_dict[str(FIPS)] = (str(int(FIPS_dict[str(FIPS)]) + int(job_count)))
                print('\n')

            except:
                print ("The location " + str(town_list[y]) + " cannot be found.")

    for x in range(3219):
        print(matrix_copy.iloc[x][4])
        if FIPS_dict.get(str(matrix_copy.iloc[x,4])) != None:
            print('the if statement worked')
            value = FIPS_dict[str(matrix_copy.loc[x,'FIPS'])]
            print(value)
            matrix_copy.loc[x, "Job Post Count"] = int(value)


    print(type(matrix_copy))
    print(FIPS_dict)
    matrix_copy.to_csv("loaded_matrix.csv")

    return(matrix_copy)



def scrape_salaries(job_title):


    print("\nSearching for ", job_title, " jobs in all 50 US states...\n")
    state_abbreviations_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN",
                                "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
                                "NH", "NJ", "NM", "NY", "NC","ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
                                "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    state_full_names_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
                       "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
                       "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
                       "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                       "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                       "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    job_data_matrix = [[0 for x in range(9)] for y in range(50)]

    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    salary_list = []

    #  REPLACE CURLY BRACKETS BELOW  WITH "collections.OrderedDict()" TO MAKE ORDERED DICTS INSTEAD OF DICTS


    salary_dict = {}
    location_dict = {}
    company_dict = {}
    experience_level_dict = {}
    job_types_dict = {}

    for state in range(len(state_abbreviations_list)):

        global state_abbreviation
        state_abbreviation = state_abbreviations_list[state]
        state_name = state_full_names_list[state]





        url = str("https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(state_abbreviation) + "&qover=1")
        page = requests.get(url)
        print(url)
        salary = "N\A"
        soup = BeautifulSoup(page.text, "html.parser")



        # SCRAPE FOR AVAILABLE JOB POSTS (OF WHICH, INDEED WILL ONLY LET YOU SEE THE FIRST 100 PAGES FOR SOME REASON)

        for div in soup.find_all(name="div", attrs={"id":"searchCount"}):
            div = div.get_text()
            div = div.replace("\n","")
            div = div.replace(",","")
            div = div.replace("Page 1 of ","")
            div = div.replace(" jobs","")
            div = re.findall('\d+', div)
            div = int(div[0])
            job_count = div

        # SCRAPE FOR MEDIAN LISTED SALARY. IF HOURLY WAGE IS CITED, CONVERT TO ANNUALIZED SALARY (40 HRS/ WK, 50 WK'S PER YEAR)


        try:
            for div in soup.find_all(name="p", attrs={"id": "univsrch-salary-currentsalary"}):
                salary = div.get_text()
                if "hour" in salary:
                    salary = re.findall('\d+', salary)
                    salary = int(str(salary[0])+str(salary[1]))   # concatonates the two halves of the salary numbers
                    salary = int(salary)
                    salary = salary / 100 * 40 * 50
                    salary = round(salary, 0)
                    salary_list.append(salary)

                else:
                    salary = re.findall('\d+', salary)
                    salary = int(str(salary[0]) + str(salary[1]))  # concatonates the two halves of the salary numbers
                    salary_list.append(salary)
        except:
            salary = "N/A"
            salary_list.append(salary)
            print(salary)
        print("Location: ", state_abbreviation, "\t  Mean Salary: ", salary)
        mean_salary = salary


        for div in soup.find_all(name="div", attrs={"id":"SALARY_rbo"}):

            tier = div.get_text()
            tier = tier.replace("\n","")
            tier = tier.replace(",","")
            tier = tier.replace("$","")
            tier = tier.replace("$","")
            tier = tier.replace("(","")
            tier = tier.replace(")"," ")
            tier = tier.split(" ")
            tier = tier[:-1]
            for x in range(0,len(tier),2):
                price_range = tier[x]
                number = tier[x+1]
                salary_dict[price_range] = number

        for div in soup.find_all(name="div", attrs={"id":"LOCATION_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'loc', '1');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '2');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '3');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '4');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '5');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '6');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '7');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '8');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '9');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '10');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '11');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '12');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '13');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '14');"}):
                locations_to_ordered_dict(li,location_dict)

            for li in div.find_all(name='li', attrs={"onmousedown": "rbptk('rb', 'loc', '10');"}):
                locations_to_ordered_dict(li,location_dict)

        for div in soup.find_all(name="div", attrs={"id": "COMPANY_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '1');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '2');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '3');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '4');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '5');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '6');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '7');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '8');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '9');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '10');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '11');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '12');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '13');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '14');"}):
                companies_ordered_dict(li, company_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'cmp', '15');"}):
                companies_ordered_dict(li, company_dict)

        for div in soup.find_all(name="div", attrs={"id": "EXP_LVL_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '1');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '2');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '3');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '4');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '5');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'explvl', '6');"}):
                experience_level_to_ordered_dict(li, experience_level_dict)

        for div in soup.find_all(name="div", attrs={"id": "JOB_TYPE_rbo"}):
            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '1');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '2');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '3');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '4');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '5');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '6');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '7');"}):
                job_type_to_ordered_dict(li, job_types_dict)

            for li in div.find_all(name="li", attrs={"onmousedown": "rbptk('rb', 'jobtype', '8');"}):
                job_type_to_ordered_dict(li, job_types_dict)

        print("Job Count: ", job_count)
        print("Salary Ranges: ", salary_dict)
        print("Locations: ", location_dict)
        print("Company Names: ",company_dict)
        print("Experience Levels: ", experience_level_dict)
        print("Job Types: ", job_types_dict)
        print("\n")


        job_data_matrix[state][0] = state_abbreviation
        job_data_matrix[state][1] = state_name
        job_data_matrix[state][2] = job_count
        job_data_matrix[state][3] = salary_dict
        job_data_matrix[state][4] = location_dict
        job_data_matrix[state][5] = company_dict
        job_data_matrix[state][6] = experience_level_dict
        job_data_matrix[state][7] = job_types_dict
        job_data_matrix[state][8] = mean_salary

        job_count=0
        salary_dict = {}
        location_dict = {}
        company_dict = {}
        experience_level_dict = {}
        job_types_dict = {}


    return job_data_matrix

def format_job_title(job_title, exact_match=True):
    if exact_match:
        job_title = '"' + job_title + '"'
    return job_title


def locations_to_ordered_dict(li,dict):
    li = li.get_text()
    li = li.replace(")", "")
    li = li.replace(" (", "")
    li = li.replace("\n", "")
    li = li.replace(" " + state_abbreviation, "")
    li = li.replace(" ", "_")
    try:
        li = li.split(",")
        li[0] = li[0].replace("_"," ")
        dict[li[0]] = li[1]
    except:
        print("Someone entered the state as the county: ", li)

def companies_ordered_dict(li, dict):
    li = li.get_text()
    li = li.replace("\n", "")
    li = li.replace(")", "")
    li = li.replace(" (", ",")
    li = li.split(",")
    li[0] = li[0].replace("_"," ")
    dict[li[0]] = li[1]

def job_type_to_ordered_dict(li, dict):
    li =  li.get_text()
    li = li.replace("\n", "")
    li = li.replace(")", "")
    li = li.replace(" Level", "_Level")
    li = li.replace("(", "")
    li = li.split(" ")
    li[0] = li[0].replace("_"," ")
    dict[li[0]] = li[1]

def experience_level_to_ordered_dict(li, dict):
    li =  li.get_text()
    li = li.replace("\n", "")
    li = li.replace(" Level", "_Level")
    li = li.replace("(", "")
    li = li.replace(" )", "")
    li = li.replace(")", "")
    li = li.split(" ")
    dict[li[0]] = li[1]




def make_cloropleth(dataframe, job_title):

    df = dataframe

    for col in df.columns:
        df[col] = df[col].astype(str)

    scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'], \
           [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

    df['text'] = "Job Posts: " + df['State Name']

    data = [dict(
        type='choropleth',
        colorscale=scl,
        autocolorscale=False,
        locations=df['State Abbreviation'],
        z=df['Job Count'].astype(float),
        locationmode='USA-states',
        text=df['text'],
        marker=dict(
            line=dict(
                color='rgb(255,255,255)',
                width=2
            )),
        colorbar=dict(
            title="Total Posts")
    )]

    layout = dict(
        title = str(job_title) + ' Job Posts per State<br>(Hover for breakdown)',
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='d3-cloropleth-map')

def get_FIPS_dict():
    with open('us_cities.csv', mode='r') as infile:
        reader = csv.reader(infile)
        dict = {str(rows[0])+" "+str(rows[2]):rows[5] for rows in reader}
        return dict


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))



