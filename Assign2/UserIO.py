#Daniel Briseno
#SID 2282050
#File defines user interface with StudentDB object, which interacts with the actual
#   mysql database


from DataBaseHandle import StudentDb
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class IO:
    def __init__(self):
        #Create database interface object
        db_path = os.path.join(BASE_DIR,'StudentDB.sqlite')
        self.db = StudentDb(db_path)
        self.user_exit = False #if user_exit == True, application will close
    
    def menu(self):
        """ This function displays a menu for the user to select the database action
        they wish to take"""
        #Database menu options
        menu = {'1':self.select_all,'2':self.add_student,'3':self.update_student,'4':self.delete_student,'5':self.search,'0':self.close_app}
        while not self.user_exit:  #while the user has not closed the application
            print("\n\n")
            #print menu
            selection = input("Please select one of the following:\n\tDisplay all students: 1\n\tAdd a student to the database: 2\n\tUpdate an existing student's information: 3\n\tDelete a student: 4\n\tSearch for students with a given Major, GPA, or Faculty Advisor: 5\n\tExit the application: 0\n").strip()
            if not selection in menu:# if invalid input given
                print("Invalid input given, please try again")
                continue
            #launch selected menu item
            menu[selection]()
    
    def select_all(self):
        """Function prints all entries in database"""
        print("\n\n")
        print(self.db.select_all())

    def add_student(self):
        """Method takes user input and adds student outlined by user to database"""
        print("You have chosen to add a student")
        #Collect input
        sid = input("Please input the student's ID\n").strip()
        fname = input("Please input the student's first name\n").strip()
        lname = input("Please input student's last name\n").strip()
        gpa_str = input("Please input student's GPA\n").strip()
        major = input("Please input student's Major\n").strip()
        fa = input("Please input student's Faculty Advisor\n").strip()
        #Check for invalid input
        tocheck = [fname, lname, major, fa]
        gpa = self.to_gpa(gpa_str)
        sid = self.to_id(sid)
        if self.are_all_names(tocheck) and not (gpa == None or sid == None):
            #send query to database interface object
            self.db.create_student(sid, fname,lname,gpa,major,fa)

    def update_student(self):
        """Method  takes in user input and updates the selected student entry with user defined values"""

        sid = self.to_id(input("You have chosen to update a student's database entry.\nPlease enter the student's Student Id\n").strip())
        #take in input
        major = input("Please enter the student's new major. If you do not wish to update this student's major, enter \"?\"\n").strip()
        fa = input("Please enter the student's new Faculty Advisor. If you do not wish to update this studetn's faculty advisor, enter \"?\"\n").strip()
        #check for invalid input
        if not self.are_all_names([major,fa],['?']) or sid == None : return
        #send in query corresponding to user selection
        if major == '?':
            if fa == '?': return
            if self.db.update_student(sid,fa = fa):
                print("Student's faculty advisor changed to ", fa)
            else:
                print("No student found with given Student Id")
        elif fa == '?':
            if self.db.update_student(sid,major=major):
                print("Student's Major changed to ",major)
            else:
                print("No student found with given Student Id")
        else:
            if self.db.update_student(sid,major = major, fa = fa):
                print("Student's major changed to ", major)
                print("Student's Faculty Advisor changed to", fa)
            else:
               print("No student found with given Student Id")

    def delete_student(self):
        """Method asks user for a student ID, and performs a soft delete of the student entry in the database 
        corresponding to that ID"""
        print("You have chosen to delete a student from the database")
        #take in input and check that it is a valid ID
        sid = self.to_id(input("Please enter the student's SID\n").strip())
        if sid == None: return
        #delete entry if it exists, else return an error message
        if self.db.delete(sid):
            print("Student with ID",sid,"has been deleted")
        else:
            print("No student with ID", sid,"found in the database")
    
    def search(self):
        """
        Method displays students matching input provided by user. User can search by GPA, Major, or advisor
        """
        #Take in input
        gpa = input("Please input GPA. If you do not wish to search by GPA enter \"?\"\n").strip()
        major = input("Please input student's Major. If you do not wish to search by Major enter \"?\"\n").strip()
        fa = input("Please input student's Faculty Advisor. If you do not wish to search by Advisor enter \"?\"\n").strip()
        if gpa == "?": 
            gpa = None
        else: 
            gpa = self.to_gpa(gpa)
            if gpa == None: 
                gpa = -1
        #check for invalid input
        if (gpa == -1 or not self.are_all_names([major,fa],['?'])):
            return
        if major == "?": 
            major = None
        if fa == "?": fa = None
        results = self.db.search(major = major, gpa = gpa, advisor = fa)
        #check if search critera matched any db entries
        if type(results) == type(None):
            print("No entries in database match search criteria")
        else:
            print("\n\n")
            print(results)

    def close_app(self):
        print("Goodbye")
        self.user_exit = True

    def are_all_names(self,lst:list, allow = []):
        """Method checks if all elements of input list are composed of alphabetic characters or whitespace
         param:
            lst: list to check
            allow: list of non alphabetic characters to allow as a 'word'"""
        return all([self.is_name(name,allow) for name in lst])
    

    def is_name(self, name:str, allow = []):
        """Method checks if given word is made of only alphabetic characters or whitespace
        param:
            name: string to check for non-alphabetic characters
            allow: non-alphabetic characters to allow as a 'word'"""
        name_lst = name.split(" ")
        if not all([x.isalpha() or (x in allow) for x in name_lst]):
            print(name," is not a name or major entry")
            return False
        return True


    def to_gpa(self, num:str):
        '''Method checks to see if given string is a valid GPA
            param:
                num: string to check if it is a valid GPA
            returns:
                if num is a valid gpa, it returns that gpa as a float
                else, it returns None'''
        num_lst = num.split(".")
        if all([x.isnumeric() for x in num_lst]):
            if len(num_lst) in range(1,3):
                num = float(num)
                if num>=0 and num<=4:
                    return num
        print(num,"is not a valid GPA value")
        return None

    def to_id(self, num:str):
        """
        function checks to see if input is a valid id number
        :param num: string to check if it is a valid id number
        :return: if num is a valid ID, returns that ID as an int, else
        returns None
        """
        if num.isnumeric(): 
            num = int(num)
            if num>=0:
                return num
        print(num, "is not a valid ID value")




            
        

