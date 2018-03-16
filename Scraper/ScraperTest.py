import unittest
import Scraper

class TestScrape(unittest.TestCase):
    
    def test_RealExample(self):
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
        
if __name__ == '__main__':
    unittest.main()