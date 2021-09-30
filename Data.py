import json
 

class Reader:
    def __init__(self):
        # Opening JSON file
        self.problems = []
        f = open('Resources/Data.json',)
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list

        
        for i in data['problems']:
            self.problems.append(i)
         
            new_courses = []
            for course in i["COURSES"]:
                new_course = {
                    "CourseID": course['CourseID'],
                    "Teacher": course['Teacher'] ,
                    "Lectures": course['Lectures'],
                    "MinWorkingDays": course['MinWorkingDays'],
                    "Students": course['Students'],
                    "SaturationDegree": 0,
                    "Degree": 0,
                    "RoomDegree": 0
                }
                new_courses.append(new_course)
            self.courses = new_courses
            self.rooms = i["ROOMS"]
            self.curricula = i["CURRICULA"]
            self.days = i["Days"] 
            self.periods_per_day = i["Periods_per_day"]
            self.num_rooms = i['Rooms']

        
        # Closing file
        f.close()
