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

        self.courses = []
        self.rooms = []
        self.curricula = []
        self.days = []
        self.periods_per_day = []
        self.num_rooms = []
        for i in data['problems']:
            self.problems.append(i)
         
            new_courses = []
            for course in i["COURSES"]:
                for r in range(0, course['Lectures']):
                    new_course = {
                        "CourseID": course['CourseID'],
                        "Teacher": course['Teacher'] ,
                        "Lectures": course['Lectures'],
                        "MinWorkingDays": course['MinWorkingDays'],
                        "Students": course['Students'],
                        "SaturationDegree": 0,
                        "Degree": 0,
                        "WorkingDays": 0,
                        "RoomDegree": 0
                    }
                    new_courses.append(new_course)
            self.courses.append(new_courses)
            self.rooms.append(i["ROOMS"])
            self.curricula.append(i["CURRICULA"])
            self.days.append(i["Days"])
            self.periods_per_day.append(i["Periods_per_day"])
            self.num_rooms.append(i['Rooms'])

        
        
        # Closing file
        f.close()
