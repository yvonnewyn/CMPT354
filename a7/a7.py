#importing module  
import pypyodbc  
import numpy as np
import pandas as pd
import random
import string

def main():
    global user
    while(True):
        user = input("Enter user id: ")
        query = "SELECT * FROM user_yelp WHERE user_id='" + user + "'"
        cursor.execute(query)
        validuser=False
        for i in cursor: 
            validuser=True
            print("Hello", i[1])
        if validuser:
            break
        else:
            print("Invalid user.")
    running=True
    while(running):
        running = funcs()

def funcs():
    print("1. Search business")
    print("2. Search user")
    print("3. Make friends :)")
    print("4. Write a review")
    print("5. Log out and exit")
    func = input("What would you like to do (enter a number 1 - 5 that corresponds to the functionalities): ").strip()
    if func == "1":
        searchbiz()
    elif func == "2":
        searchppl()
    elif func == "3":
        makefriends()
    elif func == "4":
        writereview()
    elif func == "5":
        return False
    else:
        print("Sorry, that's not a valid choice.")
    return True

def searchbiz():
    minstar = input("Enter the minimum number of stars (1-5) (leave blank if you don't wish to have this search criteria): ").strip()
    maxstar = input("Enter the maximum number of stars (1-5) (leave blank if you don't wish to have this search criteria): ").strip()
    city = input("Enter the city (leave blank if you don't wish to have this search criteria): ").lower().strip()
    name = input("Enter the name or part of the name of the business (leave blank if you don't wish to have this search criteria): ").lower().strip()
    if minstar=="":
        minstar="1"
    if maxstar=="":
        maxstar="5"
    query = "SELECT business_id, name, address, city, stars FROM business WHERE stars >= " + minstar + "AND stars <= " + maxstar
    if city != "":
        query += " AND city = '" + city + "'"
    if name != "":
        query += " AND name LIKE '%" + name + "%'"
    query += " ORDER BY name"

    try: 
        cursor.execute(query)
        if cursor.rowcount==0:
            print("There are no results for this search")
        else:
            print("-----Results-----------------------------------------------------------------------------------------")
            data = []
            for i in cursor:
                data.append(i)
            df = pd.DataFrame(data, columns=['business_id', 'name', 'address', 'city', 'stars'])
            print(df.to_string())
            print("-----End of esults-----------------------------------------------------------------------------------")
    except:
        print("Oh nose! An error occurred :(")



def searchppl():
    name = input("Enter the user name (leave blank if you don't wish to have this search criteria): ").strip().lower()
    useful = input("Is user useful (yes/no) (leave blank if you don't wish to have this search criteria): ").strip().lower()
    funny = input("Is user funny (yes/no) (leave blank if you don't wish to have this search criteria): ").lower().strip()
    cool = input("Is user cool (yes/no) (leave blank if you don't wish to have this search criteria): ").lower().strip()

    query = "SELECT user_id, name, useful, funny, cool, yelping_since FROM user_yelp WHERE name LIKE '%" + name  + "%'"
    if useful == "yes" or useful == "y":
        query += " AND useful > 0"
    if useful == "no" or useful == "n":
        query += " AND useful = 1"
    if funny == "yes" or funny == "y":
        query += " AND funny > 0"
    if funny == "no" or funny == "n":
        query += " AND funny = 1"
    if cool == "yes" or cool == "y":
        query += " AND cool > 0"
    if cool == "no" or cool == "n":
        query += " AND cool = 1"
    query += " ORDER BY name"

    try:
        cursor.execute(query)
        if cursor.rowcount==0:
            print("There are no results for this search")
        else:
            print("-----Results-----------------------------------------------------------------------------------------")
            data = []
            for i in cursor:
                data.append(i)
            df = pd.DataFrame(data, columns=['user_id', 'name', 'useful', 'funny', 'cool', 'yelping since'])
            df['useful'] = np.where(df['useful'] > 0, 'yes', 'no')
            df['funny'] = np.where(df['funny'] > 0, 'yes', 'no')
            df['cool'] = np.where(df['cool'] > 0, 'yes', 'no')
            print(df.to_string())
            print("-----End of esults-----------------------------------------------------------------------------------")
    except:
        print("Oh nose! An error occurred :(")



def makefriends():
    friend = input("Enter the user id of the user you would like to befriend: ").strip()
    query = "INSERT INTO friendship VALUES('" + user + "', '" + friend + "')"

    try:
        cursor.execute(query)
        connection.commit()

        query = "SELECT name FROM user_yelp WHERE user_id='" + friend + "'"
        cursor.execute(query)
        for i in cursor:
            print("You are now friends with", i[0], ":)")
    except pypyodbc.IntegrityError:
        print("It seems like you are already friends with this user!")
    except:
        print("Oh nose! An error occurred :(")

def writereview():
    biz = input("Enter the business id of the business you would like to write a review of: ").strip()
    stars = input("How many stars would you like to give this business (1-5): ").strip()
    reviewid = generate_reviewid()
    query = "INSERT INTO review (review_id, user_id, business_id, stars) VALUES('" + reviewid + "', '" + user + "', '" + biz + "', " + stars + ")"

    try:
        cursor.execute(query)
        connection.commit()

        query = "SELECT name FROM business WHERE business_id='" + biz + "'"
        cursor.execute(query)
        for i in cursor:
            print("Your review for", i[0], "is now published.")

    except:
        print("Oh nose! An error occurred :(")


def generate_reviewid():
    chars = string.ascii_letters + string.digits + "_"
    id = "".join(random.choice(chars) for i in range(22))
    return id

#creating connection Object which will contain SQL Server Connection  
connection = pypyodbc.connect('Driver={SQL Server};Server=CYPRESS.csil.sfu.ca;Database=ynw2354;uid=s_ynw2;pwd=Lm33fJ267AaAj23r')  

# cursor
cursor = connection.cursor()  

main()

#closing connection  
connection.close()  


    






