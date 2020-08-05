import csv
import datetime
import pathlib
import sqlite3
import sys



def welcome():

    print("------------------------------")
    print(" Welcome to Convtracker v0.20 ")
    print("------------------------------")



def main(sql, cur):

    # Checks if conv tables exist. If False, triggers 'addchar' to create new table
    if havechars(sql, cur) == False:
        print("- Database does not contain any conversion data. Please add a character.")
        addchar(sql, cur)
        print("")

    # Main menu
    while True:
        menu = getstr(">> Conversion Tracker\n[1]= View, [2]= Add/Update, [3]= Delete, [4]= Import/Export, [5]= Manage chars, [Q]= Exit: ").lower()

        # 1: View
        if menu == "1":
            while True:
                menu1 = getstr("\n> View submenu\n[1]= View all, [2]= View single, [Q]= Back: ").lower()
                if menu1 == "1":
                    viewall(sql, cur)
                    break
                elif menu1 == "2":
                    viewone(sql, cur)
                    break
                elif menu1 == "q":
                    break
                else:
                    print("- Invalid input.")
                    continue

            print("")
            continue

        # 2: Add/Update
        elif menu == "2":
            addupdate(sql, cur)
            print("")
            continue

        # 3: Delete
        elif menu == "3":
            delete(sql, cur)
            print("")
            continue

        # 4: Import/Export
        elif menu == "4":
            while True:
                menu4 = getstr("\n> Import/Export submenu\n[1]= Import, [2]= Export, [3]= Instructions, [Q]= Back: ").lower()
                if menu4 == "1":
                    importdata(sql, cur)
                    break
                elif menu4 == "2":
                    exportdata(sql, cur)
                    break
                elif menu4 == "3":
                    importinstr()
                    break
                elif menu4 == "q":
                    break
                else:
                    print("- Invalid input.")
                    continue
            print("")
            continue

        # 5: Manage chars
        elif menu == "5":
            while True:
                menu5 = getstr("\n> Manage chars submenu\n[1]= Add char, [2]= Remove char, [3]= View chars, [Q]= Back: ").lower()
                if menu5 == "1":
                    addchar(sql, cur)
                    break
                elif menu5 == "2":
                    removechar(sql, cur)
                    break
                elif menu5 == "3":
                    viewchar(sql, cur)
                    break
                elif menu5 == "q":
                    break
                else:
                    print("- Invalid input.")
                    continue
            print("")
            continue

        elif menu == "q":
            print("\nGoodbye.")
            break

        else:
            print("- Invalid input.\n")
            continue

    # Closes connection
    sql.close()



# 1A: View all
def viewall(sql, cur):
    print("\n>> View all")

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

    # Queries for i) date of latest entry & ii) avg, sum, count for armor, wtd, acc
    if proceed == True:
        action = """SELECT date FROM """ + table + """ ORDER BY date DESC LIMIT 1;"""
        action2 = """SELECT avg(armor), avg(wtd), avg(acc), sum(armor), sum(wtd), sum(acc), count(armor), count(wtd), count(acc) FROM """ + table + """;"""

        try:
            cur.execute(action)
            latestdate = cur.fetchall()
            cur.execute(action2)
            data = cur.fetchall()

            # Prints info if there is at least one row of data in table
            if (data[0])[0] != None and (data[0])[1] != None and (data[0])[2] != None:
                # Calculates overall sum, count, avg
                ototal = (data[0])[3] + (data[0])[4] + (data[0])[5]
                ocount = (data[0])[6] + (data[0])[7] + (data[0])[8]
                oavg = round(ototal / ocount, 1)

                print("\n- Latest entry on " + (latestdate[0])[0] + ":")
                print("[Arm] Avg:" + str(round((data[0])[0], 1)) + ", Count:" + str((data[0])[6]) + ", Total:" + str((data[0])[3]))
                print("[Wtd] Avg:" + str(round((data[0])[1], 1)) + ", Count:" + str((data[0])[7]) + ", Total:" + str((data[0])[4]))
                print("[Acc] Avg:" + str(round((data[0])[2], 1)) + ", Count:" + str((data[0])[8]) + ", Total:" + str((data[0])[5]))
                print("[All] Avg:" + str(oavg) + ", Count:" + str(ocount) + ", Total:" + str(ototal))

            else:
                print("- Data is missing or invalid.")

        except sqlite3.Error as e:
            print(e)



# 1B: View single
def viewone(sql, cur):
    print("\n>> View single")

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

    # Gets date for query and checks if it is valid
    if proceed == True:
        date = datetime.datetime.now().strftime("%x")

        keepdate = getstr("\nView data for today (" + date + ")?\n[Y]= Yes, [N]= Change date: ").lower()

        if keepdate == "y":
            proceed2 = True

        elif keepdate == "n":
            month = getdate("\nMonth(MM): ")
            if month != "":
                day = getdate("Day(DD): ")
                if day != "":
                    year = getdate("Year(YY): ")
                    if year != "":
                        date = month + "/" + day + "/" + year
                        if datevalid(date) == True:
                            proceed2 = True
                        else:
                            print("\n- Invalid date.")

    # Checks if date exists in table
    if proceed2 == True:
        action = """SELECT rowid FROM """ + table + """ WHERE date = ?;"""

        try:
            cur.execute(action, (date,))
            data = cur.fetchone()
            if data is not None:
                proceed3 = True
            else:
                print("\n- Data is missing or invalid.")
        except sqlite3.Error as e:
            print(e)

    # Queries for armor, wtd, acc for the specified date
    if proceed3 == True:
        action = """SELECT armor, wtd, acc FROM """ + table + """ WHERE date = ?;"""

        try:
            cur.execute(action, (date,))
            data = cur.fetchall()

            print("\nData for " + date + ":")
            print("Arm:" + str((data[0])[0]) + ", Wtd:" + str((data[0])[1]) + ", Acc:" + str((data[0])[2]))

        except sqlite3.Error as e:
            print(e)



# 2: Add/Update
def addupdate(sql, cur):
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

    # Gets date for query and checks if it is valid
    if proceed == True:
        date = datetime.datetime.now().strftime("%x")

        keepdate = getstr("\nAdd/Update data for today (" + date + ")?\n[Y]= Yes, [N]= Change date: ").lower()

        if keepdate == "y":
            proceed2 = True

        elif keepdate == "n":
            month = getdate("\nMonth (MM): ")
            if month != "":
                day = getdate("Day (DD): ")
                if day != "":
                    year = getdate("Year (YY): ")
                    if year != "":
                        date = month + "/" + day + "/" + year
                        if datevalid(date) == True:
                            proceed2 = True
                        else:
                            print("\n- Invalid date.")

    # Checks if date exists in table
    if proceed2 == True:
        action = """SELECT rowid FROM """ + table + """ WHERE date = ?;"""
        action2 = """SELECT armor, wtd, acc FROM """ + table + """ WHERE date = ?;"""
        dateindb = False
        modifier = ""

        try:
            cur.execute(action, (date,))
            data = cur.fetchone()

            # Triggers dateindb + modifier if date exists, and tells user what the current values are
            if data is not None:
                try:
                    cur.execute(action2, (date,))
                    data2 = cur.fetchall()

                    print("\n- Warning: Existing data for " + date + " found:")
                    print("Arm:" + str((data2[0])[0]) + ", Wtd:" + str((data2[0])[1]) + ", Acc:" + str((data2[0])[2]))

                    dateindb = True
                    modifier = "new "

                except sqlite3.Error as e:
                    print(e)

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

    # Updates/Adds data (according to whether dateindb is triggered) for the specified date
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



# 3: Delete
def delete(sql, cur):
    print("\n>> Delete")

    # Gets char name
    ign = getstr("Character Name: ").lower()
    table = ign + "_conv"
    proceed = False
    proceed2 = False
    proceed3 = False
    proceed4 = False

    # Checks char name and if char exists in db
    if namevalid(ign) == True:
        if tablevalid(table, sql, cur) == True:
            proceed = True
        else:
            print("- Character not found.")

    # Gets date for query and checks if it is valid
    if proceed == True:
        date = datetime.datetime.now().strftime("%x")

        keepdate = getstr("\nDelete data for today (" + date + ")?\n[Y]= Yes, [N]= Change date: ").lower()

        if keepdate == "y":
            proceed2 = True

        elif keepdate == "n":
            month = getdate("\nMonth (MM): ")
            if month != "":
                day = getdate("Day (DD): ")
                if day != "":
                    year = getdate("Year (YY): ")
                    if year != "":
                        date = month + "/" + day + "/" + year
                        if datevalid(date) == True:
                            proceed2 = True
                        else:
                            print("\n- Invalid date.")

    # Checks if date exists in table
    if proceed2 == True:
        action = """SELECT rowid FROM """ + table + """ WHERE date = ?;"""
        action2 = """SELECT armor, wtd, acc FROM """ + table + """ WHERE date = ?;"""

        try:
            cur.execute(action, (date,))
            data = cur.fetchone()

            if data is not None:
                try:
                    cur.execute(action2, (date,))
                    data2 = cur.fetchall()

                    print("\n- Existing data for " + date + ":")
                    print("Arm:" + str((data2[0])[0]) + ", Wtd:" + str((data2[0])[1]) + ", Acc:" + str((data2[0])[2]))

                    proceed3 = True

                except sqlite3.Error as e:
                    print(e)

        except sqlite3.Error as e:
            print(e)

    # Gets permission from user to delete data
    if proceed3 == True:
        consent = input("""\nTo delete data for """ + date + """, please enter "Delete data": """).lower()
        if consent == "delete data":
            proceed4 = True

    # Deletes data for the specified date
    if proceed4 == True:
        action = """DELETE FROM """ + table + """ WHERE date = ?;"""
        try:
            cur.execute(action, (date,))
            sql.commit()
            print("- Deleted.")
        except sqlite3.Error as e:
            print(e)



# 4A: Import
def importdata(sql, cur):
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

    # Gets permission from user to i) append to table OR ii) create table and insert
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
                print("- File '" + file + "' not found. File name is case-sensitive.")

    # Appends data to table
    if proceed3 == True:
        action = """INSERT INTO """ + table + """ (date, armor, wtd, acc) VALUES (?, ?, ?, ?);"""

        # Inserts csv data row by row
        with open(file, "r") as f:
            reader = csv.DictReader(f)

            # i keeps track of total number of rows, j keeps track of the number of failed insertions
            i = 0
            j = 0

            for row in reader:
                i += 1
                csvdate = (row["date"])
                csvarmor = (row["armor"])
                csvwtd = (row["wtd"])
                csvacc = (row["acc"])

                # Appends to table if date, armor, wtd, acc are valid
                if datevalid(csvdate) == True and csvarmor.isdigit() == True and csvwtd.isdigit() == True and csvacc.isdigit() == True:
                    # Corrects date to ensure that day/mth values are zero padded
                    if len(csvdate) != 8:
                        fixdate(csvdate)
                    try:
                        cur.execute(action, (csvdate, csvarmor, csvwtd, csvacc))
                        sql.commit()
                    except sqlite3.Error:
                        print("- Error in row " + str(i) + """ (duplicate entry for "date").""")
                        j += 1
                else:
                    print("- Error in row " + str(i) + """ (invalid value(s) detected).""")
                    j += 1

            print("- " + str(i - j) + " row(s) added successfully.")



# 4B: Export
def exportdata(sql, cur):
    print("\n>> Export")

    # Gets char name
    ign = getstr("Character Name: ").lower()
    table = ign + "_conv"
    proceed = False
    proceed2 = False

    # Checks char name and if char exists in db
    if namevalid(ign) == True:
        if tablevalid(table, sql, cur) == True:
            proceed = True
        else:
            print("- Character not found.")

    # Gets csv filename from user and checks if it exists, requests permission to overwrite if necessary
    if proceed == True:
        file = getstr("Name of csv file: ")
        if file != "":
            if file.endswith(".csv") == False:
                file = file + ".csv"
            if pathlib.Path(file).is_file() == True:
                consent = getstr("\n- File '" + file + "' already exists. Overwrite file?\n[Y]= Yes, [N]= No: ").lower()
                if consent == "y":
                    proceed2 = True
            elif pathlib.Path(file).is_file() == False:
                proceed2 = True

    # Exports to csv
    if proceed2 == True:
        action = """SELECT * FROM """ + table + """ ORDER BY date DESC;"""
        try:
            cur.execute(action)
            data = cur.fetchall()
            with open(file, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "armor", "wtd", "acc"])
                writer.writerows(data)
                print("- Successfully exported to '" + file + "'")
        except sqlite3.Error as e:
            print(e)



# 4C: Instructions
def importinstr():
    print("\n>> Instructions for importing csv files")
    print("""- The first row of your csv should contain the headers "date", "armor", "wtd", "acc" (case-sensitive).""")
    print("- Rows should not have blank cells.")
    print("""- Values in the "date" column should formatted as such: "MM/DD/YY".""")



# 5A: Add character
def addchar(sql, cur):
    print("\n>> Add char")

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



# 5B: Remove character
def removechar(sql, cur):
    print("\n>> Remove char")

    # Gets char name
    ign = getstr("Character Name: ").lower()
    table = ign + "_conv"
    proceed = False
    proceed2 = False

    # Checks char name and if char exists in db
    if namevalid(ign) == True:
        if tablevalid(table, sql, cur) == True:
            proceed = True
        else:
            print("- Character not found.")

    # Gets permission from user to delete data
    if proceed == True:
        consent = input("""\nTo delete all data for '""" + ign + """', please enter "Delete character": """).lower()
        if consent == "delete character":
            proceed2 = True

    # Drops table for char
    if proceed2 == True:
        action = """DROP TABLE """ + table + """;"""
        try:
            cur.execute(action)
            sql.commit()
            print("- Deleted.")

        except sqlite3.Error as e:
            print(e)



# 5C: View characters
def viewchar(sql, cur):
    print("\n>> View chars")

    action = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""
    action2 = """SELECT name FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""

    try:
        # Checks if conv tables exist
        cur.execute(action)
        data = cur.fetchall()

        # Prints names of chars
        if (data[0])[0] != 0:
            cur.execute(action2)
            data2 = cur.fetchall()

            print("Characters in database:")
            i = 0
            while i < len(data2):
                print("- " + ((data2[i])[0])[:-5].capitalize())
                i += 1
        else:
            print("- No characters in database.")

    except sqlite3.Error as e:
        print(e)



# Db checker
def dbcheck():

    db = "datanest.db"
    dbpath = pathlib.Path(db)

    if dbpath.is_file() == False:
        open(db, "w").close()
        print("- Database not found. New database '" + db + "' created.")

    return db



# SQL connector
def sqlconnect(db):

    # Todo: Handle failed connnections
    sql = sqlite3.connect(db)
    cur = sql.cursor()

    return sql, cur



# Conv tables checker
def havechars(sql, cur):

    action = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""
    try:
        cur.execute(action)
        data = cur.fetchall()
        if (data[0])[0] != 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(e)



# Character name checker
def namevalid(x):

    if len(x) <= 12 and len(x) > 0:
        return True
    else:
        return False



# Character table checker
def tablevalid(x, sql, cur):

    action = """SELECT * FROM """ + x + """;"""
    try:
        cur.execute(action)
        return True
    except sqlite3.Error:
        return False



# Date format checker
def datevalid(x):

    try:
        datetime.datetime.strptime(x, "%x")
        return True
    except ValueError:
        return False



# Date format fixer
def fixdate(x):

    if len(x) == 7:
        if x[1] == "/":
            x = "0" + x
        elif x[2] == "/":
            x = x[0:3] + "0" + x[3:7]
    elif len(x) == 6:
        x = "0" + x[0:2] + "0" + x[2:6]

    return x



# Response handler (KIV)
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



# Response handler
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



# Response handler
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



# Response handler
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



welcome()
db = dbcheck()
sql, cur = sqlconnect(db)
main(sql, cur)