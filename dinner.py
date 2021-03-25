import random

# you can choose different number of people and tables by setting the following variables
PEOPLE_NUMBER = 30
TABLES_NUMBER = 5
TABLE_SIZE = 6

class Person:
    def __init__(self, id):
        self.id = id
        self.satWith = set()
        self.lastSeat = None

def update_satWith(tables):
    for table in range(TABLES_NUMBER):
        for seat in range(TABLE_SIZE):
            for neighbour in range(TABLE_SIZE):
                if(tables[table][neighbour] is not tables[table][seat]):
                    tables[table][seat].satWith.add(tables[table][neighbour])

def course(tables, people):
    endLoop = False
    while(not endLoop): # make sure "people" array is shuffled properly and every person has changed seat
        random.shuffle(people) # shuffle "people" array to make sure person will change seat

        for person in people:
            # for each table find number of people that the person sat with
            tableSatWithNumber = list()
            for table in range(TABLES_NUMBER):
                satWith = 0

                for neighbour in tables[table]:
                    if(neighbour in person.satWith):
                        satWith = satWith+1
                
                tableSatWithNumber.append(tuple([table,satWith]))
            
            # person sit at table
            tableSatWithNumber = sorted(tableSatWithNumber, key = lambda x : x[1])

            b = False
            for table in tableSatWithNumber:
                for seat in range(TABLE_SIZE):
                    if(tables[table[0]][seat] == None and table[0]*TABLE_SIZE + seat != person.lastSeat):
                        tables[table[0]][seat] = person
                        person.lastSeat = table[0]*TABLE_SIZE + seat
                        b = True
                        break
                
                if(b):
                    break

            for table in tables:
                if(None in table):
                    break
            else:
                endLoop = True

    update_satWith(tables)

maxSumSatWith = 0
resTables = []

for trial in range(1000): # do 1000 simulations and choose the result(max sum of number of people that every person has sat with)
    tables = [[None for i in range(TABLE_SIZE)] for j in range(TABLES_NUMBER)]
    people = [Person(i+1) for i in range(PEOPLE_NUMBER)]

    # first course
    for table in range(TABLES_NUMBER):
        for seat in range(TABLE_SIZE):
            tables[table][seat] = people[table*TABLE_SIZE + seat]
            tables[table][seat].lastSeat = table*TABLE_SIZE + seat

    update_satWith(tables)

    # second course
    tables = [[None for i in range(TABLE_SIZE)] for j in range(TABLES_NUMBER)] # clear the list
    course(tables,people)

    # third course
    tables = [[None for i in range(TABLE_SIZE)] for j in range(TABLES_NUMBER)] # clear the list
    course(tables, people)

    # calculate sum of number of people that every person has sat with
    sumSatWith = 0
    for person in people:
        sumSatWith = sumSatWith + len(person.satWith)
    
    if(sumSatWith > maxSumSatWith):
        maxSumSatWith = sumSatWith
        resTables = tables[:]

# print the result in format "<table_letter><seat_number>:<person_id>"
tableLetter = "A"
for table in resTables:
    for i in range(len(table)):
        print(f"{tableLetter}{i+1}: {table[i].id}")
    
    tableLetter = chr(ord(tableLetter)+1)



