from Scraper import preprocessing
from Scraper import scraper


import django
django.setup()
from django.db.models import F
from Site.models import *

if __name__ == "__main__":
    print('start')
    job_title="data analyst"
    job_location = "Boston, MA"
    unscrubbed_data = scraper.scrape(job_title, job_location)
    
    counts = {("", "") : 0}
    
    for jobSkills in unscrubbed_data:
        job = jobSkills[0]
        if (job != 0):
            print(job)
            for thisSkill in jobSkills[5]:
                
                print(thisSkill)
                if (jobSkills[5][thisSkill] > 0):
                    if ((job_title, thisSkill) in counts):   
                        currentCount = counts[(job_title, thisSkill)]
                        counts[(job_title, thisSkill)] = currentCount + 1
                    else: 
                        counts[(job_title, thisSkill)] = 1
                #p, created = JobSkill.objects.get_or_create(category = job_title, skill = thisSkill)
                
                #count, createdCount = JobSkillCount.objects.get_or_create(job_skill_id = p.id)
            
    #scrubbed_data = preprocessing.scrubScrapedData(unscrubbed_data)
    #test = ""
    
    del counts[("","")]
    for jobSkill in counts:
        p, created = JobSkill.objects.get_or_create(category = job_title, skill = jobSkill[1])
        count, createdCount = JobSkillCount.objects.get_or_create(job_skill_id = p.id)
        print(count)
        JobSkillCount.objects.filter(id = count.id).update(posted_count = F('posted_count')+ counts[jobSkill])
        print(counts[jobSkill])
        
    
    
    