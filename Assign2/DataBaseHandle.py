import sqlite3
from pandas import DataFrame

class StudentDb:
    '''
    Class provides interface with StudentDB.sqlite database
    '''
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def exists(self,sid):
        """
        checks to see if entry with a given student ID exists in database
        """
        val = (sid,)
        self.c.execute("SELECT * FROM Student WHERE StudentId = ? AND NOT isDeleted = 1",val)
        return not(self.c.fetchall() == [])

    def select_all(self):
        """
        :return: all entries in database as a Dataframe object
        """
        self.c.execute('SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor FROM Student WHERE NOT isDeleted = 1')
        df = DataFrame(self.c.fetchall(),columns = ['StudentId','Firstname','LastName', 'GPA', 'Major', 'FacultyAdvisor'])
        return df 

    def create_student(self, id, fname, lname, gpa, major, fa):
        """Method creates student with given id, first name, last name , gpa, major and faculty advisor"""
        if self.exists(id):
            print("Student with given ID already exists")
            return
        values = (id, fname,lname,gpa,major,fa,0)
        self.c.execute("INSERT INTO Student (StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, isDeleted) VALUES(?,?,?,?,?,?,?)",values)
        self.conn.commit()

    def update_student(self, sid, major = None, fa = None):
        """Updates student with given id (sid), using given major and faculty adivsor inputs"""
        if not self.exists(sid): return 0
        if major == None and fa == None: return 1
        sqlcmd = "UPDATE Student SET" 
        val = []
        if not major == None:
            sqlcmd+= " Major = ?,"
            val.append(major)
            if fa == None: 
                sqlcmd = sqlcmd[:-1]
        if not fa == None:
            sqlcmd+= " FacultyAdvisor = ?"
            val.append(fa)
        sqlcmd += " WHERE StudentID = ?"
        val.append(sid)
        values = tuple(val)
        self.c.execute(sqlcmd,values)
        self.conn.commit()
        return 1

    def delete(self, sid):
        """"deletes student from database if the student has given ID"""
        if not self.exists(sid):
            return 0
        val = (sid,)
        self.c.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", val)
        self.conn.commit()
        return 1

    def search(self, major = None, gpa = None, advisor = None):
        """Searches db for student with given major, gpa, or advisor"""
        if major == None and gpa == None and advisor == None: return None
        crit = []
        sqlcmd = "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor FROM Student WHERE "
        if not major == None:
            sqlcmd += " Major = ? AND"
            crit.append(major)
            if gpa == None and advisor == None:
                sqlcmd = sqlcmd[:-3]
        if not gpa == None:
            sqlcmd += " GPA = ? AND"
            crit.append(gpa)
            if advisor == None: 
                sqlcmd = sqlcmd[:-3]
        if not advisor == None:
            sqlcmd += " FacultyAdvisor = ?"
            crit.append(advisor)
        criteria = tuple(crit)
        self.c.execute(sqlcmd,criteria)
        results = self.c.fetchall()
        if results == []: return None
        df = DataFrame(results, columns = ['StudentId','Firstname','LastName', 'GPA', 'Major', 'FacultyAdvisor'])
        return df

    def __del__(self):
        self.conn.close()

