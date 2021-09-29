
#. Each element of the population
# represents a construction heuristic and combines the problem
# characteristics together with a period selection heuristic. 
class Evaluator:
    def __init__(self, problems, rooms, courses, days, curricula, num_roooms, periods_per_day):
        self.problems = problems
        self.rooms = rooms
        self.courses = courses
        self.days = days
        self.curricula = curricula
        self.num_rooms = num_roooms

        self.timetable = Timetable(periods_per_day, days, self.num_rooms, self.rooms)

        self.evaluateSaturationDegree()

      

    def evaluate(self, tree):
        pass

    def evaluateHelper(self, node):
        pass

    def evaluateSaturationDegree(self):
        for course in self.courses:
            if self.allClassesScheduled(course): 
                course['SaturationDegree'] = 9999 # does not need to be scheduled anymore
            else: # needs to be scheduled
                course['SaturationDegree'] = self.lectureScheduleFeasibility(course['CourseID'])


        self.courses.sort(key=lambda x: x.count, reverse=True)


    def allClassesScheduled(self, course):
        num_scheduled = 0
        for day in self.timetable.days:
            for period in day:
                for room in period:
                    if room['slot']['CourseID'] == course['CourseID']:
                        num_scheduled = num_scheduled + 1

        if num_scheduled < course['Lectures']:
            return False
        else:
            return True

    def lectureScheduleFeasibility(self, courseID):
        feasible_periods = 0
        for day in self.timetable.days:
                for period in day:  
                    period_available = self.emptyRoomInPeriod(period)
                    if period_available["available"] == True: #there is room in period?
                        for room in period_available['rooms']:
                            if room['teacher'] == None:
                                teacher_available = True
                            else:
                                teacher_available = self.checkTeacherAvailibility(room['teacher'])
                            if teacher_available == True: # the teacher is available in the period?
                                room_big_enough = self.checkRoomCapacityEnough(room, courseID)
                                if room_big_enough == True: # the room is big enough?
                                    conflicts = not self.checkCurriculumConflicts(courseID, period)
                                    if conflicts == False: # the curriculum is not clashing?
                                        feasible_periods = feasible_periods + 1

        return feasible_periods


    def checkCurriculumConflicts(self, courseID, period):
        courses_in_curricula = self.findCurriculaCourses(courseID)
        for room in period:
            if room['slot']['CourseID'] in courses_in_curricula:
                return False

        return True

    def checkRoomCapacityEnough(self, room, courseID):
        for course in self.courses:
            if course['CourseID'] == courseID:
                if course['Lectures'] <= room['room']['capacity']:
                    return True
                else:
                    return False

    def checkTeacherAvailibility(self, period, teacher):
            for room in period:
                if room['slot']['Teacher'] == teacher:
                    return False

            return True

    def emptyRoomInPeriod(self, period):
        rooms_available = []
        available = False
        for room in period:
            if room['slot']['CourseID'] == None:
                rooms_available.append({
                    "room": room,
                    "availble": True,
                    "teacher": room['slot']['Teacher']
                }) 
                available = True

        if available == True:
            return {
                "available": True,
                "rooms": rooms_available
            } 
        
        else:
            return {
                "available": False,
                "rooms": rooms_available
            } 
        
        

    def evaluateNumberOfStudents(self):
        pass

    def evaluateLargestDegree(self):
        pass

    def evaluateLectures(self):
        pass

    def evaluateUnavailability(self):
        pass

    def evaluateMinimumNumOfWorkingDays(self):
        pass

    def evaluateRoomDegree(self):
        pass

    # Three options were considered for deciding which
    # period in the timetable to schedule the chosen lecture in:
    def evaluateFirstPeriod(self):
        pass

    def evaluateRandomPeriod(self):
        pass

    def evaluateMinimumPenaltyPeriod(self):
        pass

    def evaluateCombineCharacteristicPeriod(self):
        pass

    def evaluateCombineCharacteristic(self):
        pass

    

    def checkHardConstraints(self):
        pass

    def checkLectureAllocations(self):
        lectures_scheduled = True
        for c in self.courses:
            num_scheduled = self.numLectureScheduled(c['CourseID'])
            if num_scheduled < c['Lectures']:
                lectures_scheduled = False

        return lectures_scheduled

    def checkConflicts(self):
        clashes = []
        for d in self.timetable.days:
            for i in range(0, len(d)):
                for s in d[i]:
                    if s['slot']['CourseID'] != None:
                        clash = {
                            "CourseID": s['slot']['CourseID'],
                            "num_clashes": 0
                        }
                        all_courses = self.findCurriculaCourses(s['slot']['CourseID'])
                        for inner_room in d[i]:
                            if s['slot']['CourseID'] != inner_room['slot']['CourseID']:
                                if inner_room['slot']['CourseID'] in all_courses:
                                    clash["num_clashes"] = clash["num_clashes"] + 1
                        clashes.append(clash)

        return clashes
                   

    def checkAvailability(self):
        clashes = []
        for d in self.timetable.days:
            for i in range(0, len(d)):
                for s in d[i]:
                    if s['slot']['Teacher'] != None:
                        clash = {
                            "Teacher": s['slot']['Teacher'],
                            "num_clashes": 0
                        }
                        for inner_room in d[i]:
                            if s['slot']['Teacher'] == inner_room['slot']['Teacher']:
                            
                                clash["num_clashes"] = clash["num_clashes"] + 1
                        clashes.append(clash)

        return clashes
                    
    def findCurriculaCourses(self, courseID):
        all_courses = []
        for c in self.curricula:
            if courseID in c['courses']:
                all_courses = all_courses + c['courses']

        return all_courses
                                  
                                   

    def numLectureScheduled(self, lectureID):
        count = 0
        for d in self.timetable.days:
            
            for i in range(0, len(d)):
                for s in d[i]:
                    if s['slot']['CourseID'] == lectureID:
                        count = count + 1

        return count

    def checkSoftConstraints(self):
        pass

    def checkRoomCapacity(self):
        courses_over = []
        for d in self.timetable.days:
            for i in range(0, len(d)):
                for s in d[i]:
                    if s['slot']['CourseID'] != None:
                        num_students = self.getNumStudentInCourse(s['slot']['CourseID'])
                        if num_students > s['capacity']:
                            over = {
                                "CourseID": s['slot']['CourseID'],
                                "over": num_students - s['capacity']
                            }
                            courses_over.append(over)
        return courses_over

    def checkWorkingDays(self):
        temp_courses = []
        for s in self.courses:
            temp_course = {
                "CourseID": s['CourseID'],
                "Teacher": s['Teacher'],
                "Lectures": s['Lectures'],
                "MinWorkingDays": s['MinWorkingDays'],
                "WorkingDays": 0,
                "Students": s['Students']
            }

            temp_courses.append(temp_course)

            for course in temp_courses:
                for day in self.timetable.days:
                    course_found = False
                    for period in day:  
                        if period['course']['CourseID'] != None and period['course']['CourseID'] == course['CourseID']:
                            course_found = True
                    
                    if course_found == True:
                        course['WorkingDays'] = course['WorkingDays'] + 1
            return_courses = []
            for course in temp_course:
                if course['WorkingDays'] < course['MinWorkingDays']:
                    return_courses.append(course)


            return return_courses

    def calculateCurriculumCompactness(self):
        #bruh why
        pass

    def calculateRoomStability(self):
        #All the lectures for a course should be
        # scheduled in the same venue
        rooms_array = []
        num_mismatches = 0
        for day in self.timetable.days:
            for slot in day:
                for room in slot:
                    courses_in_curricula = self.getSetsOfCoursesInCurricula(room['slot']['CourseID'])
                 
                    for curriculum in courses_in_curricula:
                        for course in curriculum:
                            rooms = self.roomsAllocationCourses(course)
                            for rest_of_courses in curriculum:
                                if rest_of_courses != course:
                                    for r in rooms:
                                        room_courses = self.courseInRoom(r)
                                        if not rest_of_courses in room_courses:
                                            num_mismatches = num_mismatches + 1
                                    
        return num_mismatches


    def coursesInRooms(self, room):
        for day in self.timetable.days:
            for slot in day:
                for room in slot:
                    print(room)

    def roomsAllocationCourses(self, courseID):
        return_rooms = []
        for day in self.timetable.days:
            for slot in day:
                for room in slot:
                    if room['slot']['CourseID'] == courseID:
                        return_rooms.append(room['name'])

        return return_rooms
                
    def getSetsOfCoursesInCurricula(self, courseID):
        return_course_sets = []
        for curricular in self.curricula:
            if courseID in curricular['courses']:
                return_course_sets.append(curricular['courses'])

        return return_course_sets

    def courseInRoom(self, roomID, courseID):
        found = False
        for day in self.timetable.days:
            for slot in day:
                for room in slot:
                    if room['name'] == roomID and room['slot']['CourseID'] == courseID:
                        found = True
                        return found

        return found

    
    def getNumStudentInCourse(self, courseID):
        for s in self.courses:
            if s['CourseID'] == courseID:
                return s['Lectures']


class Timetable:
    def __init__(self, num_classes, num_days, num_rooms, rooms):
        self.num_classes = num_classes
        self.num_days = num_days
        self.rooms = rooms
        self.days = []
        for i in range(0, num_days):
            slots = []
            for j in range(0, num_classes):
                rooms = []
          
                for k in self.rooms:
              
                    rooms.append({
                        "name": k['name'],
                        "capacity": k['occupancy'],
                        "slot" : {
                            "CourseID": None,
                            "Teacher": None 
                        }
                    })
                slots.append(rooms)
       
            self.days.append(slots)

      