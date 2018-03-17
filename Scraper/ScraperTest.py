import unittest
import Scraper

class TestScrape(unittest.TestCase):
    
    TEST_COMPANY_NAME = "MAGIC COMPANY"
    TEST_JOB_NAME = "MAGIC JOB"
    TEST_JOB_LOCATION = "MAGIC LOCATION"
    
    TEST_JOB_URL = "/MAGICURL"
    TEST_JOB_SALARY = "10000"
    
            
    def buildValidIndeedCompany(self, numCompanies, hasSalary):
        fullText = ""
        salaryText = ""
        if hasSalary:
            salaryText = "<nobr>" + self.TEST_JOB_SALARY + "</nobr>"
        for x in range(numCompanies):
            fullText += """
            <div class="row">
            """ + salaryText + """
            <a 
                data-tn-element="jobTitle"
                title=""" + "\"" + self.TEST_JOB_NAME + "\""  + """
                
                href=""" + "\"" + self.TEST_JOB_URL + "\"" + """
            >  
            </a>
            <span class="company">
                <a data-tn-element="companyName">
                    """ + self.TEST_COMPANY_NAME + """
                </a>
            </span>
            <span class=location>
                """ + self.TEST_JOB_LOCATION + """
            </span>
            </div>
            """
        return fullText
        
    def test_RealExampleSkills(self):
        testText = """
            <b>Other information:
            <br>
            </b>Experience: Minimum 5 years experience in clinical nursing or allied health discipline
            <br>
            <br>
            <b>Competencies and skills:
            <br>
            </b>BLS, Excel
            <b><br>
            </b><br>
            <b>Summary:
            <br>
            </b>Serves as educator, consultant, researcher, instructional and evaluation designer, clinical practice expert, and interprofessional collaborator supporting the clinical development needs of staff throughout the PHS enterprise
            <b><br>
            <br>
            </b>Supports the educational components of the organizations clinical initiatives and practices
            <br>
            <br>
            Program Development, Promotion and Oversight Functions: Develops program in area of clinical expertise including training and development of specialty teams or specialty knowledge in all staff. Develops program elements such as clinical guidelines and disease state management protocols and clinical outcome studies; Promotes quality of care and development of standards of care through such activities as concurrent and retrospective chart review, conducting process and outcome evaluation and data analysis.
            """
        returnedSkills = Scraper.scraper.getJobSkills(testText)
        assert(returnedSkills["excel"] == 1)

    def test_noRSkill_Rword(self):
        testText = """
            word
            """
        returnedSkills = Scraper.scraper.getJobSkills(testText)
        assert(returnedSkills[" r "] == 0)

    def test_noSASSkill_SASWord(self):
        testText = """
            sassy
            """
        returnedSkills = Scraper.scraper.getJobSkills(testText)
        assert(returnedSkills[" sas "] == 0)
        
    def test_allSkills(self):
        
        testText = ""
        for skill in Scraper.scraper.data_science_skills_list:
            testText += skill + " "
            
        returnedSkills = Scraper.scraper.getJobSkills(testText)
        for skill in Scraper.scraper.data_science_skills_list:
            skill = skill.lower()
            if returnedSkills[skill] == 0:
                print(skill)
            assert(returnedSkills[skill] == 1)
            
    def DISABLED_test_JobOnlyText(self):
        testText = """
        <div class="row">
            <a 
                data-tn-element="jobTitle"
                title=""" + "\"" + self.TEST_JOB_NAME + "\""  + """
            </a>
        </div>
        """
        returnedJobData = Scraper.scraper.getJobs(testText)
        for jobData in returnedJobData:
            assert(jobData.job == self.TEST_JOB_NAME)
        
    def test_getJobNoSalaryCompanyClass(self):
        testText = """
        <div class="row">
            <a 
                data-tn-element="jobTitle"
                title=""" + "\"" + self.TEST_JOB_NAME + "\""  + """
                
                href=""" + "\"" + self.TEST_JOB_URL + "\"" + """
            >  
            </a>
            <span class="company">
                <a data-tn-element="companyName">
                    """ + self.TEST_COMPANY_NAME + """
                </a>
            </span>
            <span class=location>
                """ + self.TEST_JOB_LOCATION + """
            </span>
        </div>
        """
        returnedJobData = Scraper.scraper.getJobs(testText)
        for jobData in returnedJobData:
            assert(jobData.jobTitle == self.TEST_JOB_NAME)
            assert(jobData.company == self.TEST_COMPANY_NAME)
            assert(jobData.location == self.TEST_JOB_LOCATION)
            assert(jobData.url == " http://indeed.com" + self.TEST_JOB_URL)
            assert(jobData.skills == [])
            assert(jobData.salary == "No Salary Provided")
            
    def test_getJobNoSalaryResultLinkSourceCompanyClass(self):
        testText = """
        <div class="row">
            <a 
                data-tn-element="jobTitle"
                title=""" + "\"" + self.TEST_JOB_NAME + "\""  + """
                
                href=""" + "\"" + self.TEST_JOB_URL + "\"" + """
            >  
            </a>
            <span class="result - link - source">
                <a data-tn-element="companyName">
                    """ + self.TEST_COMPANY_NAME + """
                </a>
            </span>
            <span class=location>
                """ + self.TEST_JOB_LOCATION + """
            </span>
        </div>
        """
        returnedJobData = Scraper.scraper.getJobs(testText)
        for jobData in returnedJobData:
            assert(jobData.jobTitle == self.TEST_JOB_NAME)
            assert(jobData.company == self.TEST_COMPANY_NAME)
            assert(jobData.location == self.TEST_JOB_LOCATION)
            assert(jobData.url == " http://indeed.com" + self.TEST_JOB_URL)
            assert(jobData.skills == [])
            assert(jobData.salary == "No Salary Provided")
        
    def test_getJobSalaryNobr(self):
        testText = """
        <div class="row">
            <nobr>""" + self.TEST_JOB_SALARY + """</nobr>
            <a 
                data-tn-element="jobTitle"
                title=""" + "\"" + self.TEST_JOB_NAME + "\""  + """
                
                href=""" + "\"" + self.TEST_JOB_URL + "\"" + """
            >  
            </a>
            <span class="company">
                <a data-tn-element="companyName">
                    """ + self.TEST_COMPANY_NAME + """
                </a>
            </span>
            <span class=location>
                """ + self.TEST_JOB_LOCATION + """
            </span>
        </div>
        """
        returnedJobData = Scraper.scraper.getJobs(testText)
        for jobData in returnedJobData:
            assert(jobData.jobTitle == self.TEST_JOB_NAME)
            assert(jobData.company == self.TEST_COMPANY_NAME)
            assert(jobData.location == self.TEST_JOB_LOCATION)
            assert(jobData.url == " http://indeed.com" + self.TEST_JOB_URL)
            assert(jobData.skills == [])
            assert(jobData.salary == self.TEST_JOB_SALARY)
        
    def test_getJobSalarySjcl(self):
        testText = """
        <div class="row">
            <div class="sjcl">
                <div>
                    """ + self.TEST_JOB_SALARY + """
                </div>
            </div>
            <a 
                data-tn-element="jobTitle"
                title=""" + "\"" + self.TEST_JOB_NAME + "\""  + """
                
                href=""" + "\"" + self.TEST_JOB_URL + "\"" + """
            >  
            </a>
            <span class="company">
                <a data-tn-element="companyName">
                    """ + self.TEST_COMPANY_NAME + """
                </a>
            </span>
            <span class=location>
                """ + self.TEST_JOB_LOCATION + """
            </span>
        </div>
        """
        returnedJobData = Scraper.scraper.getJobs(testText)
        for jobData in returnedJobData:
            assert(jobData.jobTitle == self.TEST_JOB_NAME)
            assert(jobData.company == self.TEST_COMPANY_NAME)
            assert(jobData.location == self.TEST_JOB_LOCATION)
            assert(jobData.url == " http://indeed.com" + self.TEST_JOB_URL)
            assert(jobData.skills == [])
            assert(jobData.salary == self.TEST_JOB_SALARY)
            
            
    def test_threeJobsNoSalary(self):
        testText = self.buildValidIndeedCompany(3, False)
        returnedJobData = Scraper.scraper.getJobs(testText)
        assert(returnedJobData.__len__() == 3)
        for jobData in returnedJobData:
            assert(jobData.jobTitle == self.TEST_JOB_NAME)
            assert(jobData.company == self.TEST_COMPANY_NAME)
            assert(jobData.location == self.TEST_JOB_LOCATION)
            assert(jobData.url == " http://indeed.com" + self.TEST_JOB_URL)
            assert(jobData.skills == [])
            assert(jobData.salary == "No Salary Provided")
            
    def test_threeJobsWithSalary(self):
        testText = self.buildValidIndeedCompany(3, True)
        returnedJobData = Scraper.scraper.getJobs(testText)
        assert(returnedJobData.__len__() == 3)
        for jobData in returnedJobData:
            assert(jobData.jobTitle == self.TEST_JOB_NAME)
            assert(jobData.company == self.TEST_COMPANY_NAME)
            assert(jobData.location == self.TEST_JOB_LOCATION)
            assert(jobData.url == " http://indeed.com" + self.TEST_JOB_URL)
            assert(jobData.skills == [])
            assert(jobData.salary == self.TEST_JOB_SALARY)
        
if __name__ == '__main__':
    unittest.main()