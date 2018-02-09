import sqlite3
from sqlite3 import Error
from DataAccess import internal


def add_job_and_skill(skill, job):
    conn = internal.get_db_base()
    skillId = internal.get_skill_id(skill, conn)
    jobId = internal.get_job_id(job, conn)
    print(jobId)
    print(skillId)
    
    internal.increment_job_and_skill(skillId, jobId, conn)
    conn.commit()
    conn.close()
    return None