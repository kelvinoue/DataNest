import csv
import datetime
import pathlib
import sqlite3
import sys



def welcome():

    print("------------------------------")
    print(" Welcome to Convtracker v0.11 ")
    print("------------------------------")



def main(newdb, sql, cur):

    # Todo: Redesign based on checking tables instead of newdb
    if newdb == True:
        print("- Database does not contain any characters. Please add a character.\n")
        addchar(sql, cur)


    # Todo: Add 'Delete'
    # Main menu
    while True:
        menu = getstr(">> Conversion Tracker\n[1]= View, [2]= Add/Update, [3]= Import, [4]= Export, [5]= Add characters, [Q]= Cancel: ").lower()


        # 1: View
        if menu == "1":
            print("\n>> View")

            # Gets char name
            ign = getstr("Character Name: ").lower()
            table = ign + "_conv"
            proceed = False

            # Checks char name and if char exists in db
            if namevalid(ign) == True:
                if tablevalid(table, sql, cur) == True:
                    proceed = True
                else:
                    print("- Character not found.")

            # Queries for avg, sum, count for char
            if proceed == True:
                action = """SELECT avg(armor), avg(wtd), avg(acc), sum(armor), sum(wtd), sum(acc), count(armor), count(wtd), count(acc) FROM """ + table + """;"""

                try:
                    cur.execute(action)
                    data = cur.fetchall()

                    # Prints stats if there is at least one row of data in table
                    if (data[0])[0] != None and (data[0])[1] != None and (data[0])[2] != None and (data[0])[3] != None and (data[0])[4] != None and (data[0])[5] != None:
                        # Calculates overall total, count and avg
                        ototal = (data[0])[3] + (data[0])[4] + (data[0])[5]
                        ocount = (data[0])[6] + (data[0])[7] + (data[0])[8]
                        oavg = round(ototal / ocount, 1)

                        print("")
                        print("[Armor] Avg:" + str(round((data[0])[0], 1)) + ", Count:" + str((data[0])[6]) + ", Total:" + str((data[0])[3]))
                        print("  [Wtd] Avg:" + str(round((data[0])[1], 1)) + ", Count:" + str((data[0])[7]) + ", Total:" + str((data[0])[4]))
                        print("  [Acc] Avg:" + str(round((data[0])[2], 1)) + ", Count:" + str((data[0])[8]) + ", Total:" + str((data[0])[5]))
                        print("  [All] Avg:" + str(oavg) + ", Count:" + str(ocount) + ", Total:" + str(ototal))

                    else:
                        print("- Data is missing or invalid.")

                # Note: Print errors for no table or columns
                except sqlite3.Error as e:
                    print(e)

            print("")
            continue


        # 2: Add/Update
        elif menu == "2":
            print("\n>> Add/Update")

            # Gets char name
            ign = getstr("Character Name: ").lower()
            table = ign + "_conv"
            proceed = False
            proceed2 = False
            proceed3 = False

            # Checks char name and if char exists in db
            if namevalid(ign) == True:
                if tablevalid(table, sql, cur) == True:
                    proceed = True
                else:
                    print("- Character not found.")

            # Checks if user wants to modify the current day's entry
            if proceed == True:
                date = datetime.datetime.now().strftime("%x")

                keepdate = getstr("\n- Add/Update data for today (" + date + ")?\n[Y]= Yes, [N]=Select another date: ").lower()

                if keepdate == "y":
                    proceed2 = True

                elif keepdate == "n":
                    month = getdate("Month (MM): ")
                    if month != "":
                        day = getdate("Day (DD): ")
                        if day != "":
                            year = getdate("Year (YY): ")
                            if year != "":
                                date = month + "/" + day + "/" + year
                                proceed2 = True

            # Queries to check if data for the selected date exists
            if proceed2 == True:
                action = """SELECT rowid FROM """ + table + """ WHERE date = ?;"""
                dateindb = False
                modifier = ""

                try:
                    cur.execute(action, (date,))
                    data = cur.fetchone()
                    # Triggers dateindb (to run a different query later) and modifier if data for selected date exists
                    if data is not None:
                        print("\n- Warning: Existing data for " + date + " found.")
                        dateindb = True
                        modifier = "new "

                except sqlite3.Error as e:
                    print(e)

                # Gets values for armor, wtd, acc
                print("\nEnter " + modifier + "values for " + date + ":")
                armor = getint("Armor: ")
                if armor != "":
                    wtd = getint("Wtd: ")
                    if wtd != "":
                        acc = getint("Acc: ")
                        if acc != "":
                            proceed3 = True

            # Updates/Adds data depending on whether dateindb is triggered
            if proceed3 == True:
                if dateindb == True:
                    action = """UPDATE """ + table + """ SET armor = ?, wtd = ?, acc = ? WHERE date = ?;"""
                    try:
                        cur.execute(action, (armor, wtd, acc, date))
                        sql.commit()
                        print("- Saved.")
                    except sqlite3.Error as e:
                        print(e)

                elif dateindb == False:
                    action = """INSERT INTO """ + table + """ (date, armor, wtd, acc) VALUES (?, ?, ?, ?);"""
                    try:
                        cur.execute(action, (date, armor, wtd, acc))
                        sql.commit()
                        print("- Saved.")
                    except sqlite3.Error as e:
                        print(e)

            print("")
            continue


        # 3: Import
        if menu == "3":
            print("\n>> Import")

            # Gets char name
            ign = getstr("Character Name: ").lower()
            table = ign + "_conv"
            proceed = False
            proceed2 = False
            proceed3 = False

            # Checks char name
            if namevalid(ign) == True:
                proceed = True

            # Gets permission from user to append OR to create table and insert
            if proceed == True:
                if tablevalid(table, sql, cur) == True:
                    consent = getstr("\nCharacter '" + ign + "' already exists in database. Append to existing data?\n[Y]= Yes, [N]= No: ").lower()
                    if consent == "y":
                        proceed2 = True

                if tablevalid(table, sql, cur) == False:
                    consent = getstr("\nCharacter '" + ign + "' not found. Add character to database?\n[Y]= Yes, [N]= No: ").lower()
                    # Creates new table
                    if consent == "y":
                        action = """CREATE TABLE """ + table + """ (date NUMERIC NOT NULL PRIMARY KEY, armor INTEGER NOT NULL, wtd INTEGER NOT NULL, acc INTEGER NOT NULL);"""
                        try:
                            cur.execute(action)
                            sql.commit()
                            proceed2 = True
                        except sqlite3.Error as e:
                            print(e)

            # Gets csv filename from user and checks if it exists
            if proceed2 == True:
                file = input("\nName of csv file: ")
                if file != "":
                    if file.endswith(".csv") == False:
                        file = file + ".csv"
                    if pathlib.Path(file).is_file() == True:
                        proceed3 = True
                    else:
                        print("- File '" + file + "' not found.")

            # Appends
            if proceed3 == True:
                action = """INSERT INTO """ + table + """ (date, armor, wtd, acc) VALUES (?, ?, ?, ?);"""

                # Inserts csv data row by row
                with open(file, "r") as f:
                    reader = csv.DictReader(f)

                    # i keeps track of total number of rows, j keeps track of the number of failed insertions
                    i = 0
                    j = 0

                    # Keeps track of whether errors are present to trigger help message later
                    errors = False

                    for row in reader:
                        i += 1
                        csvdate = (row["date"])
                        csvarmor = (row["armor"])
                        csvwtd = (row["wtd"])
                        csvacc = (row["acc"])

                        if datevalid(csvdate) == True and csvarmor.isdigit() == True and csvwtd.isdigit() == True and csvacc.isdigit() == True:
                            if len(csvdate) != 8:
                                fixdate(csvdate)
                            try:
                                cur.execute(action, (csvdate, csvarmor, csvwtd, csvacc))
                                sql.commit()
                            except sqlite3.Error:
                                print("- Error in row " + str(i) + ".")
                                errors = True
                                j += 1

                        else:
                            print("- Error in row " + str(i) + ".")
                            errors = True
                            j += 1

                    print("- " + str(i - j) + " row(s) added successfully.")

                    if errors == True:
                        print("""\n- Possible sources of error: Empty cells or duplicate dates in csv, dates not formatted as "MM/DD/YY" in csv, or date already exists in db.""")


            print("")
            continue


        # 4: Export
        if menu == "4":
            print("\n>> Export")

            # Gets char name
            ign = getstr("Character Name: ").lower()
            table = ign + "_conv"
            proceed = False

            # Checks char name and if char exists in db
            if namevalid(ign) == True:
                if tablevalid(table, sql, cur) == True:
                    proceed = True
                else:
                    print("- Character not found.")

            # Exports to csv
            if proceed == True:
                action = """SELECT * FROM """ + table + """ ORDER BY date DESC;"""
                try:
                    cur.execute(action)
                    data = cur.fetchall()
                    # Todo: Check if file already exists
                    with open(table + ".csv", "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(["date", "armor", "wtd", "acc"])
                        writer.writerows(data)
                        print("- Successfully exported to '" + table + ".csv'.")
                except sqlite3.Error as e:
                    print(e)

            print("")
            continue


        # Todo: Add view + delete chars function
        elif menu == "5":
            print("\n>> Add characters")
            addchar(sql, cur)
            continue


        elif menu == "q":
            print("\nGoodbye.")
            break


        else:
            print("- Invalid input.\n")
            continue

    # Closes connection
    sql.close()



# 5: Add character function
def addchar(sql, cur):

    # Gets char name
    ign = getstr("Character Name: ").lower()
    table = ign + "_conv"
    proceed = False

    # Checks char name and if char exists in db
    if namevalid(ign) == True:
        if tablevalid(table, sql, cur) == False:
            proceed = True
        else:
            print("- Character already in database.")

    # Creates table for char
    if proceed == True:
        action = """CREATE TABLE """ + table + """ (date NUMERIC NOT NULL PRIMARY KEY, armor INTEGER NOT NULL, wtd INTEGER NOT NULL, acc INTEGER NOT NULL);"""
        try:
            cur.execute(action)
            sql.commit()
            print("- Character added.")

        except sqlite3.Error as e:
            print(e)

    print("")



def namevalid(x):

    if len(x) <= 12 and len(x) > 0:
        return True
    else:
        return False



def tablevalid(x, sql, cur):

    action = """SELECT * FROM """ + x + """;"""
    try:
        cur.execute(action)
        return True
    except sqlite3.Error:
        return False



def datevalid(x):

    try:
        datetime.datetime.strptime(x, "%x")
        return True
    except ValueError:
        return False



def fixdate(x):

    if len(x) == 7:
        if x[1] == "/":
            x = "0" + x
        elif x[2] == "/":
            x = x[0:3] + "0" + x[3:7]
    elif len(x) == 6:
        x = "0" + x[0:2] + "0" + x[2:6]

    return x



def yesno():

    while True:
        try:
            response = input("[Y]= Yes, [Q]= No/Quit: ").lower()
        except:
            print("\n- Please select a valid option.")
            continue
        if response == "y":
            break
        elif response == "q":
            print("\nGoodbye.")
            sys.exit(1)
        else:
            print("\n- Please select a valid option.")
            continue



def getstr(x):

    while True:
        try:
            s = input(x)
        except:
            print("- Please use alphanumeric characters.\n")
            continue
        if s.isalnum() == True:
            break
        elif s == "":
            break
        else:
            print("- Please use alphanumeric characters.\n")
            continue
    return s



def getint(x):

    while True:
        try:
            i = input(x)
        except:
            print("- Please key in a number.")
            continue
        if i.isdigit() == True:
            break
        elif i == "":
            return str(i)
        else:
            print("- Please key in a number.")
            continue
    return int(i)



def getdate(x):

    while True:
        try:
            date = input(x)
        except:
            print("- Please key in a 2 digit number.")
            continue
        if date.isdigit() == True and len(date) == 2:
            break
        elif date == "":
            break
        else:
            print("- Please key in a 2 digit number.")
            continue
    return date



# Db checker
def dbcheck():

    db = "datanest.db"
    dbpath = pathlib.Path(db)
    newdb = False

    if dbpath.is_file() == False:
        open(db, "w").close()
        newdb = True
        print("- Database not found. New database '" + db + "' created.")

    return db, newdb



# SQL connector
def sqlconnect(db):

    # Todo: Handle failed connnections
    sql = sqlite3.connect(db)
    cur = sql.cursor()

    return sql, cur



welcome()
# db, newdbstatus = inicheck()
db, newdb = dbcheck()
sql, cur = sqlconnect(db)
main(newdb, sql, cur)