import sqlite3
from sqlite3 import Error
from EmploymentSkillsStatisticsProject.settings import BASE_DIR
from multiprocessing.process import _process_counter

DB_NAME = "db.sqlite3"

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def get_db_base():
    return create_connection(BASE_DIR + "\\" + DB_NAME)

def increment_job_and_skill(skill, job, conn):
    print(skill)
    print(job)
    cur = conn.cursor()
    
    sqlSelect = '''SELECT COUNT(*)
                FROM JobSkillCounts
                WHERE JobTitleID = ? 
                AND SkillID = ?'''
    
    currentCount = cur.execute(sqlSelect, (job,skill)).fetchall()[0][0]
    if (currentCount == 0):
        sqlInsert = '''INSERT INTO JobSkillCounts
            VALUES(?,?,?)'''
        cur.execute(sqlInsert, (job,skill,1))
        print("inserting jobSkillCount")
    else:
        sqlUpdate = '''UPDATE JobSkillCounts
            SET Count = Count + 1
            WHERE JobTitleID = ?
            AND SkillID = ?'''
        cur.execute(sqlUpdate, (job, skill))
    
    cur.close()
    return None

def get_skill_id(skill, conn):
    cur = conn.cursor()
    sqlCount = '''SELECT COUNT(*)
    FROM Skills
    WHERE Skill = ? '''
    counter = cur.execute(sqlCount, (skill,)).fetchall()[0][0]
    
    sqlSelect = '''SELECT SkillID
            FROM Skills
            WHERE Skill = ? '''
    
    print("SkillCount")
    print(counter)      
    if (counter == 0):
        sqlInsert = '''INSERT INTO Skills(Skill)
                VALUES(?)'''
        cur.execute(sqlInsert, (skill,))
        
    print("Getting SkillID")
    cur.execute(sqlSelect, (skill,))
    
    skillId = cur.fetchall()
    cur.close()
    return skillId[0][0]
    
def get_job_id(job, conn):
    cur = conn.cursor()
    sqlCount = '''SELECT COUNT(*)
    FROM JobTitles
    WHERE JobTitle = ? '''
    countTest = cur.execute(sqlCount, (job,)).fetchall()
    counter = countTest[0][0]
    print(counter)
    sqlSelect = '''SELECT JobTitleID
            FROM JobTitles
            WHERE JobTitle = ? ''' 
    
    if (counter == 0):
        sqlInsert = '''INSERT INTO JobTitles(JobTitle)
                VALUES(?)'''
        cur.execute(sqlInsert, (job,))
        print("inserting")
    
    print("Getting")
    cur.execute(sqlSelect, (job,))
    jobId = cur.fetchall()
    print(jobId[0][0])
    cur.close()
    return jobId[0][0]