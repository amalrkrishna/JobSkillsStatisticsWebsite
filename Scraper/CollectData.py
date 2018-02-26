
import django
from plotly.api.v2.grids import row
django.setup()
import csv
from django.utils import timezone

from Scraper import preprocessing
from Scraper import scraper
from Scraper import DisplayData
from django.db.models import F
from Site.models import *

def printShapeFile():
    import shapefile
    shape = shapefile.Reader("C:\\Users\Matt\\Downloads\\tl_2017_us_county\\tl_2017_us_county.shp")
    num_records = shape.numRecords
    
    for i in range(0, num_records):
        feat = shape.shapeRecord(i)
        print(feat.record[4] + "(" + feat.record[1] + "," + feat.record[0] + ")")
        
    print(shape.shapeRecords()[0])
    
def populateMany():
    job_titles = ["data scientist",
                  "software engineer",
                  "computer scientist",
                  "software developer",
                  "information technology",
                  "network architect",
                  "database administrator",
                  "web developer"]
    
    #regions = Geography.objects.all()
    regions = Geography.objects.filter(AreaCode = 25).all()
    
    now = datetime.datetime.now()
    
    for region in regions:
        for job in job_titles:
            runPopulateJobSkillRegionData(
                job,
                region.SubArea + " County, " + region.Area, 
                region.id, 
                now)

def runPopulateJobSkillRegionData(job_title, job_location, geography_id, now):
    unscrubbed_data = scraper.scrape(job_title, job_location)
    
    end_date = datetime.datetime(now.year, now.month, 1)
    if (now.month == 12):
        end_date = datetime.datetime(now.year + 1, 1, 1)
    else:
        end_date = datetime.datetime(now.year, now.month + 1, 1)
        
    counts = {("", "") : 0}
    
    for jobSkills in unscrubbed_data:
        job = jobSkills[0]
        if (job != 0):
            for thisSkill in jobSkills[5]:
                #TODO Add logic for date posted filtering
                if (jobSkills[5][thisSkill] > 0):
                    if ((job_title, thisSkill) in counts):   
                        currentCount = counts[(job_title, thisSkill)]
                        counts[(job_title, thisSkill)] = currentCount + 1
                    else: 
                        counts[(job_title, thisSkill)] = 1
                
    
    del counts[("","")]
    for jobSkill in counts:
        p, created = JobSkill.objects.get_or_create(category = job_title, skill = jobSkill[1])
        
        row, count = JobSkillRegionDateCount.objects.get_or_create(
            job_skill_id = p.id,
            geography_id = geography_id,
            start_date = timezone.make_aware(datetime.datetime(now.year, now.month, 1), timezone.get_current_timezone()),
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone()))
        
        JobSkillRegionDateCount.objects.filter(id = row.id).update(posted_count = F('posted_count')+ counts[jobSkill])
    
    
def runPopulate(job_title, job_location):
    unscrubbed_data = scraper.scrape(job_title, job_location)
    
    counts = {("", "") : 0}
    
    for jobSkills in unscrubbed_data:
        job = jobSkills[0]
        if (job != 0):
            for thisSkill in jobSkills[5]:
                #TODO Add logic for date posted filtering
                if (jobSkills[5][thisSkill] > 0):
                    if ((job_title, thisSkill) in counts):   
                        currentCount = counts[(job_title, thisSkill)]
                        counts[(job_title, thisSkill)] = currentCount + 1
                    else: 
                        counts[(job_title, thisSkill)] = 1
                
    
    del counts[("","")]
    for jobSkill in counts:
        p, created = JobSkill.objects.get_or_create(category = job_title, skill = jobSkill[1])
        count, createdCount = JobSkillCount.objects.get_or_create(job_skill_id = p.id)
        JobSkillCount.objects.filter(id = count.id).update(posted_count = F('posted_count')+ counts[jobSkill])

def populateGeography():
    country = "US"
    country_code = 1
    csv_file = open("C:\\Users\\Matt\\Desktop\\CS673\\Geography.csv", "rt", encoding="ansi")
    reader = csv.reader(csv_file)
    states = {0 : ""}
    first = True
    
    for row in reader:
        if(first):
            first = False
        else:
            if(row[0] == "40"):
                states[row[1]] = row[6]
            if(row[0] == "50"):
                state = states[row[1]]
                state_code = row[1]
                county_code = row[2]
                county = row[6][:row[6].rfind(' ')]

                Geography.objects.get_or_create(Country = country, 
                                         CountryCode = country_code,
                                         Area = state,
                                         AreaCode = state_code,
                                         SubArea = county,
                                         SubAreaCode = county_code)
     
if __name__ == "__main__":    
    populateMany()
    #populateGeography()
    #printShapeFile()
    #runPopulate("data analyst", "Suffolk County, MA")
    '''DisplayData.GetSkillsFromJobRegion("data analyst", "Boston, MA")'''
   
    
    
    