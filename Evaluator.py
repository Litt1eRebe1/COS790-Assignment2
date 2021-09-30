import random
#. Each element of the population
# represents a construction heuristic and combines the problem
# characteristics together with a period selection heuristic. 
class Evaluator:
    def __init__(self, seed, problems, rooms, courses, days, curricula, num_roooms, periods_per_day):
        self.problems = problems
        self.rooms = rooms
        self.courses = courses
        self.days = days
        self.curricula = curricula
        self.num_rooms = num_roooms
        self.seed = seed
        random.seed(seed)
        self.timetable = Timetable(periods_per_day, days, self.num_rooms, self.rooms)

        # self.evaluateRandomPeriod(self.courses[0]) # works so far
        # self.evaluateFirstPeriod(self.courses[1])
        # self.evaluateFirstPeriod(self.courses[2])
        # self.evaluateFirstPeriod(self.courses[3])
        # self.evaluateFirstPeriod(self.courses[4])

        # self.evaluateRandomPeriod(self.courses[0]) # works so far
        # self.evaluateRandomPeriod(self.courses[1])
        # self.evaluateRandomPeriod(self.courses[2])
        # self.evaluateRandomPeriod(self.courses[3])
        # self.evaluateRandomPeriod(self.courses[4])


        # self.evaluateMinimumPenaltyPeriod(self.courses[0]) # works so far
        # self.evaluateMinimumPenaltyPeriod(self.courses[1])
        # self.evaluateMinimumPenaltyPeriod(self.courses[2])
        # self.evaluateMinimumPenaltyPeriod(self.courses[3])
        # self.evaluateMinimumPenaltyPeriod(self.courses[4])
        # self.evaluateMinimumPenaltyPeriod(self.courses[5])
        # self.timetable.print()

      

    def evaluate(self, tree):
     
        self.evaluateHelper(tree.root)
        self.timetable.print()

    def evaluateHelper(self, node):
        if node == None: #end it is finished
            return
        if node.terminal == False:
            # continue going
            for child in node.children:
                self.evaluateHelper(child)
        else:
            if node.id == 0: #Saturation degre
                self.evaluateSaturationDegree()
            elif node.id == 1: #Number of student
                self.evaluateNumberOfStudents()
            elif node.id == 2: #Largest degree
                self.evaluateLargestDegree()
            elif node.id == 3: #Lectures
                self.evaluateLectures()
            elif node.id == 4: #"Minimum number of working days
                self.evaluateMinimumNumOfWorkingDays()
            elif node.id == 5: #Room degree
                self.evaluateRoomDegree()
            elif node.id == 6: #First Period
                self.evaluateFirstPeriod()
            elif node.id == 7: #Random Period
                self.evaluateRandomPeriod()
            elif node.id == 8: #Minimum Penalty Period
                self.evaluateMinimumPenaltyPeriod()



    def evaluateSaturationDegree(self): #- The lectures with the least
                                        #number of feasible periods in the timetable at the current
                                        #point of construction are given priority
        for course in self.courses:
            if self.allClassesScheduled(course): 
                course['SaturationDegree'] = 9999 # does not need to be scheduled anymore
            else: # needs to be scheduled
                course['SaturationDegree'] = self.lectureScheduleFeasibility(course['CourseID'])


        self.courses.sort(key=lambda x: x['SaturationDegree'], reverse=False)


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
        self.courses.sort(key=lambda x: x['Students'], reverse=True)

    def evaluateLargestDegree(self): #- The lectures that have the largest
                                    # number of potential clashes are given priority to be
                                    # scheduled.
        for course in self.courses:
            course['Degree'] = self.getNumberOfPotentialClashes(course['CourseID'])

        self.courses.sort(key=lambda x: x['Degree'], reverse=True)
      
        
    def getNumberOfPotentialClashes(self, courseID):
        potential_clashes = 0
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
                                    if conflicts == True: # the curriculum is not clashing?
                                        potential_clashes = potential_clashes + 1

        return potential_clashes

    def evaluateLectures(self):
        self.courses.sort(key=lambda x: x['Lectures'], reverse=True)
      

    def evaluateMinimumNumOfWorkingDays(self):
        self.courses.sort(key=lambda x: x['MinWorkingDays'], reverse=True)

    def evaluateRoomDegree(self):
        for course in self.courses:
            course['RoomDegree'] = self.roomDegree(course)

        self.courses.sort(key=lambda x: x['RoomDegree'], reverse=False)


    def roomDegree(self, course):
        degree = 0
        for day in self.timetable.days:
            for period in day: 
                for room in period:
                    if room['slot']['CourseID'] == None: # not shceduled yet
                        if room['capacity'] >= course['Students']:
                            degree = degree + 1

        return degree

    # Three options were considered for deciding which
    # period in the timetable to schedule the chosen lecture in:
    def evaluateFirstPeriod(self):
        course = self.getCourse()
        scheduled = False
        while scheduled == False:
            for day in range(0, len(self.timetable.days)):
                for period in range(0, len(self.timetable.days[day])):
                    for room in range(0, len(self.timetable.days[day][period])):
                        if self.timetable.days[day][period][room]['slot']['CourseID'] == None: #room is empty
                            self.timetable.days[day][period][room] = self.scheduleExam(course, self.timetable.days[day][period][room])
                            hard_constraints = self.checkHardConstraintCourseForPeriod(course, self.timetable.days[day][period])
                            if hard_constraints == False: #hard constraints violated
                                self.timetable.days[day][period][room] = self.removeExam(self.timetable.days[day][period][room])
                            else:
                                scheduled = True
                                return True #it has been scheduled
        return scheduled

    def getCourse(self):
        if len(self.courses) > 0:
            return self.courses[0]
        else:
            return 0

    def scheduleExam(self, course, room):
        room['slot']['CourseID'] = course['CourseID']
        room['slot']['Teacher'] = course['Teacher']

        return room

    def removeExam(self, room):
        room['slot']['CourseID'] = None
        room['slot']['Teacher'] = None

        return room

    def evaluateRandomPeriod(self):
        course = self.getCourse()
        available_rooms = self.getFeasibleRooms(course)
        if len(available_rooms) > 0:
            self.seed = self.seed + 1
            random.seed(self.seed)
            choice = random.randint(0, len(available_rooms) - 1)

            available_rooms[choice] = self.scheduleExam(course, available_rooms[choice])
            return True
        else:
            return False

    def getFeasibleRooms(self, course):
        availble_rooms = []
       
        for day in range(0, len(self.timetable.days)):
            for period in range(0, len(self.timetable.days[day])):
                for room in range(0, len(self.timetable.days[day][period])):
                    if self.timetable.days[day][period][room]['slot']['CourseID'] == None: #can try schedule
                        self.timetable.days[day][period][room] = self.scheduleExam(course, self.timetable.days[day][period][room])
                        available = self.checkHardConstraintCourseForPeriod(course, self.timetable.days[day][period])
                        if available == True:
                            availble_rooms.append(self.timetable.days[day][period][room])
                        
                        self.timetable.days[day][period][room] = self.removeExam(self.timetable.days[day][period][room])
        return availble_rooms

    def evaluateMinimumPenaltyPeriod(self):
        course = self.getCourse()
        availble_rooms = self.getFeasibleRooms(course)

        soft_constraint = self.checkSoftConstraints(course, availble_rooms[0])
        softest_room = {
            "room" : availble_rooms[0],
            "soft_score": soft_constraint
        }
        for room in range(1, len(availble_rooms)):
            soft_constraint = self.checkSoftConstraints(course, availble_rooms[room])
            if soft_constraint < softest_room['soft_score']:
                softest_room['room'] = availble_rooms[room]
                softest_room['soft_score'] = soft_constraint
                
        softest_room['room'] = self.scheduleExam(course, softest_room['room'])


    def evaluateCombineCharacteristicPeriod(self):
        pass  # @TODO

    def evaluateCombineCharacteristic(self):
        pass  # @TODO

    

    def checkHardConstraints(self):
        num_violations = 0
        for day in self.timetable.days:
            for periods in day:
                for rooms in periods:
                    violates = self.checkHardConstraintCourseForPeriod(rooms['CourseID'], periods)
                    if violates == True:
                        num_violations = num_violations + 1

        return num_violations

    def checkHardConstraintCourseForPeriod(self, course, period):
   
        num_to_be_scheduled = course['Lectures'] - self.numLectureScheduled(course['CourseID'])
        clashes = self.checkConflictsTimetableCourse(course)
        teacher_available = self.checkAvailabilityInPeriod(course['Teacher'], period)
        
        if num_to_be_scheduled >= 0 and clashes[0]['num_clashes'] == 0 and teacher_available == True:
            return True
        else:
            return False

    def checkAvailabilityInPeriod(self, teacher, period):
        count_teacher = 0
        for room in period:
            if room['slot']['Teacher'] == teacher:
                count_teacher = count_teacher + 1

        return count_teacher <= 1

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

    def checkConflictsTimetableCourse(self, course): 
        clashes = []
        for day in self.timetable.days:
            for period in day:
                for room in period:
                    if room['slot']['CourseID'] == course['CourseID']:
                        clash = {
                            "CourseID": course['CourseID'],
                            "num_clashes": 0
                        }
                        all_courses = self.findCurriculaCourses(course['CourseID'])
                        for inner_room in period:
                            if course['CourseID'] != inner_room['slot']['CourseID']:
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

    def checkSoftConstraints(self, course, room):
        room_capacity = self.checkRoomCapacityPerRoom(course, room)
        course_working_days =  self.checkWorkingDaysPerRoom(course, room)
        room = self.scheduleExam(course, room)
        num_rooms_used = self.calculateRoomStabilityPerCourse(course) - 1

        room = self.removeExam(room)

        

        constraint_cost = course_working_days
        constraint_cost = constraint_cost + num_rooms_used
        if room_capacity == False:
            constraint_cost = constraint_cost * 1.5
        else:
            constraint_cost = constraint_cost * 1
        

        return constraint_cost


    def checkRoomCapacityPerRoom(self, course, room):
        return course['Students'] > room['capacity']

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

    def checkWorkingDaysPerRoom(self, course, room):
        room = self.scheduleExam(course, room)
        for c in self.checkWorkingDays():
            if c['CourseID'] == course['CourseID']:
                # found course
                room = self.removeExam(room)
                return abs(c['MinWorkingDays'] - c['WorkingDays'])
        return course['WorkingDays']

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
                        for room in period: 
                            if room['slot']['CourseID'] != None and room['slot']['CourseID'] == course['CourseID']:
                                course_found = True
                    
                        if course_found == True:
                            course['WorkingDays'] = course['WorkingDays'] + 1
            return_courses = []
            for course in temp_courses:
            
                if course['WorkingDays'] < course['MinWorkingDays']:
                    return_courses.append(course)


            return return_courses


    def calculateRoomStability(self):
        #All the lectures for a course should be
        # scheduled in the same venue
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

    def calculateRoomStabilityPerCourse(self, course):
        rooms_used = []
        for day in self.timetable.days:
            for slot in day:
                for room in slot:
                    if room['slot']['CourseID'] == course['CourseID']:
                        rooms_used.append(room['name'])
                  
        mismatches = []
        for room in rooms_used:
            if room not in mismatches:
                mismatches.append(room)

        return len(mismatches)

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

    def print(self):
        i = 1
        for day in self.days:
            print("--------- DAY ( " + str(i) + " ) -----------")
            i = i + 1
            p = 1
            for period in day:
                print("\n ++++++ PERIOD ( " + str(p) + " ) ++++++")
                p = p + 1
                for room in period:
                    print(room)

    def copy(self):
        new_timetable = Timetable(self.num_classes, self.num_days, self.num_rooms, self.rooms)
        new_timetable.days = []

        for day in self.days:
            slots = []
            for slot in day:
                rooms = []
                for room in slot:
                    rooms.append({
                        "name": room['name'],
                        "capacity": room['occupancy'],
                        "slot" : {
                            "CourseID": room['slot']['CourseID'],
                            "Teacher": room['slot']['Teacher'] 
                        }
                    })
                slots.append(rooms)
            new_timetable.days.append(slots)
        return new_timetable