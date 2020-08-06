import csv
import datetime
import pathlib
import sqlite3
import sys



def welcome():

    print("------------------------------")
    print(" Welcome to Convtracker v0.35 ")
    print("------------------------------")



def main(sql, cur, cchar):

    # Checks if any entries have been made for today
    updatecheck(sql, cur)

    # Main menu
    while True:
        menu = getstr(">> Conversion Tracker  // Current char: " + cchar.capitalize() + "\n[1]= View, [2]= Add/Update, [3]= Delete, [4]= Import/Export, [5]= Manage chars, [Q]= Exit: ").lower()

        # 1: View
        if menu == "1":
            while True:
                menu1 = getstr("\n> View submenu\n[1]= View all, [2]= View single, [Q]= Back: ").lower()
                if menu1 == "1":
                    cchar = viewall(sql, cur, cchar)
                    break
                elif menu1 == "2":
                    cchar = viewone(sql, cur, cchar)
                    break
                elif menu1 == "q":
                    break
                else:
                    print("- Invalid input.")
                    continue

            print("")
            continue

        # 2: Add/Update (Todo: Fix overflow, input one frag at a time)
        elif menu == "2":
            cchar = addupdate(sql, cur, cchar)
            print("")
            continue

        # 3: Delete
        elif menu == "3":
            cchar = delete(sql, cur, cchar)
            print("")
            continue

        # 4: Import/Export
        elif menu == "4":
            while True:
                menu4 = getstr("\n> Import/Export submenu\n[1]= Import, [2]= Export, [3]= Instructions, [Q]= Back: ").lower()
                if menu4 == "1":
                    cchar = importdata(sql, cur, cchar)
                    break
                elif menu4 == "2":
                    cchar = exportdata(sql, cur, cchar)
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
                    cchar = addchar(sql, cur, cchar)
                    break
                elif menu5 == "2":
                    cchar = removechar(sql, cur, cchar)
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



# 0A: Current char
def curchar(sql, cur):

    action = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""
    action2 = """SELECT name FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""
    cchar = "---"

    try:
        # Checks if conv tables (chars) exist
        cur.execute(action)
        data = cur.fetchall()

        if (data[0])[0] == 0:
            print("- Database does not contain any conversion data. Please add a character.")
            cchar = addchar(sql, cur, cchar)
            print("")
            return cchar

        # If 1 char exists, sets char as current char
        elif (data[0])[0] == 1:
            try:
                cur.execute(action2)
                data2 = cur.fetchall()
                cchar = ((data2[0])[0])[:-5]
                return cchar
            except sqlite3.Error as e:
                print(e)

        # If multiple chars exist, prompts user to set current char
        elif (data[0])[0] >= 1:
            try:
                cur.execute(action2)
                data3 = cur.fetchall()

                print(">> Characters in database:")
                i = 0
                while i < len(data3):
                    print("- " + ((data3[i])[0])[:-5].capitalize())
                    i += 1

                ign = getstr("\nName of character to manage: ")
                if namevalid(ign) == True:
                    table = ign + "_conv"
                    if tablevalid(table, sql, cur) == True:
                        cchar = ign
                        print("")
                        return cchar
                    else:
                        print("- Character not found.")
                print("")

            except sqlite3.Error as e:
                print(e)
        
    except sqlite3.Error as e:
        print(e)

    return cchar



# 0B: Updatecheck
def updatecheck(sql, cur):

    date = datetime.datetime.now().strftime("%x")
    characters = ["none"]
    action = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""
    action2 = """SELECT name FROM sqlite_master WHERE type='table' AND name LIKE "%_conv";"""

    try:
        # Checks if conv tables exist
        cur.execute(action)
        data = cur.fetchall()

        # If there is at least 1 conv table, checks for names of chars
        if (data[0])[0] != 0:
            cur.execute(action2)
            data2 = cur.fetchall()

            # Checks each char's table for an entry with today's date
            i = 0
            updated = False
            while i < len(data2):
                table = (data2[i])[0]
                action3 = """SELECT date FROM """ + table + """ ORDER BY date DESC LIMIT 1;"""
                cur.execute(action3)
                data3 = cur.fetchone()
                
                # Adds char to list if there is an entry with today's date
                if data3 != None:
                    cur.execute(action3)
                    data4 = cur.fetchall()
                    if (data4[0])[0] == date:
                        characters.append(((data2[i])[0])[:-5])
                        updated = True
                i += 1
            if updated == True:
                characters.remove("none")

    except sqlite3.Error as e:
        print(e)
    
    # Prints list
    print(">> Characters updated today (" + date + "):")
    i = 0
    while i < len(characters):
        print("- " + characters[i].capitalize())
        i += 1
    print("")



# 1A: View all
def viewall(sql, cur, cchar):
    print("\n>> View all")

    proceed = False
    proceed2 = False

    # Checks whether to proceed with current char
    consent = getstr("View data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            if tablevalid(table, sql, cur) == True:
                cchar = ign
                proceed2 = True
            else:
                print("- Character not found.")

    # Queries for i) date of latest entry & ii) avg, sum, count for armor, wtd, acc
    if proceed2 == True:
        action = """SELECT date FROM """ + table + """ ORDER BY date DESC LIMIT 1;"""
        action2 = """SELECT avg(armor), avg(wtd), avg(acc), sum(armor), sum(wtd), sum(acc), count(armor), count(wtd), count(acc) FROM """ + table + """;"""

        try:
            cur.execute(action)
            latestdate = cur.fetchall()
            cur.execute(action2)
            data = cur.fetchall()

            # Prints info if there is at least one row of data in table
            if (data[0])[0] == None and (data[0])[1] == None and (data[0])[2] == None:
                print("- Data is missing or invalid.")

            else:
                # Arm avg
                if (data[0])[0] != None:
                    armavg = round((data[0])[0], 1)
                else:
                    armavg = 0
                
                # Wtd avg
                if (data[0])[1] != None:
                    wtdavg = round((data[0])[1], 1)
                else:
                    wtdavg = 0

                # Acc avg
                if (data[0])[2] != None:
                    accavg = round((data[0])[2], 1)
                else:
                    accavg = 0
                
                # Arm count
                if (data[0])[6] == None:
                    armcount = 0
                else:
                    armcount = (data[0])[6]

                # Wtd count
                if (data[0])[7] == None:
                    wtdcount = 0
                else:
                    wtdcount = (data[0])[7]

                # Acc count
                if (data[0])[8] == None:
                    acc_count = 0
                else:
                    acc_count = (data[0])[8]

                # Arm total
                if (data[0])[3] == None:
                    armtotal = 0
                else:
                    armtotal = (data[0])[3]

                # Wtd total
                if (data[0])[4] == None:
                    wtdtotal = 0
                else:
                    wtdtotal = (data[0])[4]

                # Acc total
                if (data[0])[5] == None:
                    acctotal = 0
                else:
                    acctotal = (data[0])[5]

                # Calculates overall sum, count, avg
                ototal = armtotal + wtdtotal + acctotal
                ocount = armcount + wtdcount + acc_count
                oavg = round(ototal / ocount, 1)

                print("\n- Latest entry on " + (latestdate[0])[0] + ":")
                print("[Arm]  Avg: " + str(armavg) + ",  Count: " + str(armcount) + ",  Total: " + str(armtotal))
                print("[Wtd]  Avg: " + str(wtdavg) + ",  Count: " + str(wtdcount) + ",  Total: " + str(wtdtotal))
                print("[Acc]  Avg: " + str(accavg) + ",  Count: " + str(acc_count) + ",  Total: " + str(acctotal))
                print("[All]  Avg: " + str(oavg) + ",  Count: " + str(ocount) + ",  Total: " + str(ototal))
                
        except sqlite3.Error as e:
            print(e)
    
    return cchar



# 1B: View single
def viewone(sql, cur, cchar):
    print("\n>> View single")

    proceed = False
    proceed2 = False
    proceed3 = False
    proceed4 = False

    # Checks whether to proceed with current char
    consent = getstr("View data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            if tablevalid(table, sql, cur) == True:
                cchar = ign
                proceed2 = True
            else:
                print("- Character not found.")

    # Gets date for query and checks if it is valid
    if proceed2 == True:
        date = datetime.datetime.now().strftime("%x")

        keepdate = getstr("\nView data for today (" + date + ")?\n[Y]= Yes, [N]= Change date: ").lower()

        if keepdate == "y":
            proceed3 = True

        elif keepdate == "n":
            month = getdate("\nMonth(MM): ")
            if month != "":
                day = getdate("Day(DD): ")
                if day != "":
                    year = getdate("Year(YY): ")
                    if year != "":
                        date = month + "/" + day + "/" + year
                        if datevalid(date) == True:
                            proceed3 = True
                        else:
                            print("\n- Invalid date.")

    # Checks if date exists in table
    if proceed3 == True:
        action = """SELECT rowid FROM """ + table + """ WHERE date = ?;"""

        try:
            cur.execute(action, (date,))
            data = cur.fetchone()
            if data is not None:
                proceed4 = True
            else:
                print("\n- Data is missing or invalid.")
        except sqlite3.Error as e:
            print(e)

    # Queries for armor, wtd, acc for the specified date
    if proceed4 == True:
        action = """SELECT armor, wtd, acc FROM """ + table + """ WHERE date = ?;"""

        try:
            cur.execute(action, (date,))
            data = cur.fetchall()

            print("\nData for " + date + ":")
            print("- Arm: " + str((data[0])[0]) + ",  Wtd: " + str((data[0])[1]) + ",  Acc: " + str((data[0])[2]))

        except sqlite3.Error as e:
            print(e)

    return cchar



# 2: Add/Update
def addupdate(sql, cur, cchar):
    print("\n>> Add/Update")

    proceed = False
    proceed2 = False
    proceed3 = False
    proceed4 = False

    # Checks whether to proceed with current char
    consent = getstr("Add/Update data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            if tablevalid(table, sql, cur) == True:
                cchar = ign
                proceed2 = True
            else:
                print("- Character not found.")

    # Gets date for query and checks if it is valid
    if proceed2 == True:
        date = datetime.datetime.now().strftime("%x")

        keepdate = getstr("\nAdd/Update data for today (" + date + ")?\n[Y]= Yes, [N]= Change date: ").lower()

        if keepdate == "y":
            proceed3 = True

        elif keepdate == "n":
            month = getdate("\nMonth (MM): ")
            if month != "":
                day = getdate("Day (DD): ")
                if day != "":
                    year = getdate("Year (YY): ")
                    if year != "":
                        date = month + "/" + day + "/" + year
                        if datevalid(date) == True:
                            proceed3 = True
                        else:
                            print("\n- Invalid date.")

    # Checks if date exists in table
    if proceed3 == True:
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

                    print("\nWarning: Existing data for " + date + " found:")
                    print("- Arm: " + str((data2[0])[0]) + ",  Wtd: " + str((data2[0])[1]) + ",  Acc: " + str((data2[0])[2]))

                    dateindb = True
                    modifier = "new "

                except sqlite3.Error as e:
                    print(e)

        except sqlite3.Error as e:
            print(e)

        # Gets values for armor, wtd, acc
        print("\nEnter " + modifier + "values for " + date + """:\n- Note: Key in "n" to to enter blank values.""")
        armor = getfrag("Armor: ")
        if armor != "":
            wtd = getfrag("Wtd: ")
            if wtd != "":
                acc = getfrag("Acc: ")
                if acc != "":
                    if armor == "n":
                        armor = None
                    if wtd == "n":
                        wtd = None
                    if acc == "n":
                        acc = None
                    proceed4 = True

    # Updates/Adds data (according to whether dateindb is triggered) for the specified date
    if proceed4 == True:
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

    return cchar



# 3: Delete
def delete(sql, cur, cchar):
    print("\n>> Delete")

    proceed = False
    proceed2 = False
    proceed3 = False
    proceed4 = False
    proceed5 = False

    # Checks whether to proceed with current char
    consent = getstr("Delete data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            if tablevalid(table, sql, cur) == True:
                cchar = ign
                proceed2 = True
            else:
                print("- Character not found.")

    # Gets date for query and checks if it is valid
    if proceed2 == True:
        date = datetime.datetime.now().strftime("%x")

        keepdate = getstr("\nDelete data for today (" + date + ")?\n[Y]= Yes, [N]= Change date: ").lower()

        if keepdate == "y":
            proceed3 = True

        elif keepdate == "n":
            month = getdate("\nMonth (MM): ")
            if month != "":
                day = getdate("Day (DD): ")
                if day != "":
                    year = getdate("Year (YY): ")
                    if year != "":
                        date = month + "/" + day + "/" + year
                        if datevalid(date) == True:
                            proceed3 = True
                        else:
                            print("\n- Invalid date.")

    # Checks if date exists in table
    if proceed3 == True:
        action = """SELECT rowid FROM """ + table + """ WHERE date = ?;"""
        action2 = """SELECT armor, wtd, acc FROM """ + table + """ WHERE date = ?;"""

        try:
            cur.execute(action, (date,))
            data = cur.fetchone()

            if data is not None:
                try:
                    cur.execute(action2, (date,))
                    data2 = cur.fetchall()

                    print("\nExisting data for " + date + ":")
                    print("- Arm: " + str((data2[0])[0]) + ",  Wtd: " + str((data2[0])[1]) + ",  Acc: " + str((data2[0])[2]))

                    proceed4 = True

                except sqlite3.Error as e:
                    print(e)

        except sqlite3.Error as e:
            print(e)

    # Gets permission from user to delete data
    if proceed4 == True:
        consent = input("""\nTo delete data for """ + date + """, please enter "Delete data": """).lower()
        if consent == "delete data":
            proceed5 = True

    # Deletes data for the specified date
    if proceed5 == True:
        action = """DELETE FROM """ + table + """ WHERE date = ?;"""
        try:
            cur.execute(action, (date,))
            sql.commit()
            print("- Deleted.")
        except sqlite3.Error as e:
            print(e)

    return cchar



# 4A: Import
def importdata(sql, cur, cchar):
    print("\n>> Import")

    proceed = False
    proceed2 = False
    proceed3 = False
    proceed4 = False

    # Checks whether to proceed with current char
    consent = getstr("Import data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            proceed2 = True

    # Gets permission from user to i) append to table OR ii) create table and insert
    if proceed2 == True:
        if tablevalid(table, sql, cur) == True:
            consent = getstr("\nCharacter '" + ign + "' already exists in database. Append to existing data?\n[Y]= Yes, [N]= No: ").lower()
            if consent == "y":
                proceed3 = True

        if tablevalid(table, sql, cur) == False:
            consent = getstr("\nCharacter '" + ign + "' not found. Add character to database?\n[Y]= Yes, [N]= No: ").lower()
            # Creates new table
            if consent == "y":
                action = """CREATE TABLE """ + table + """ (date NUMERIC NOT NULL PRIMARY KEY, armor INTEGER, wtd INTEGER, acc INTEGER);"""
                try:
                    cur.execute(action)
                    sql.commit()
                    proceed3 = True
                except sqlite3.Error as e:
                    print(e)

    # Gets csv filename from user and checks if it exists
    if proceed3 == True:
        file = input("\nName of csv file: ")
        if file != "":
            if file.endswith(".csv") == False:
                file = file + ".csv"
            if pathlib.Path(file).is_file() == True:
                proceed4 = True
            else:
                print("- File '" + file + "' not found. File name is case-sensitive.")

    # Appends data to table
    if proceed4 == True:
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

    return cchar



# 4B: Export
def exportdata(sql, cur, cchar):
    print("\n>> Export")

    proceed = False
    proceed2 = False
    proceed3 = False

    # Checks whether to proceed with current char
    consent = getstr("Delete data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            if tablevalid(table, sql, cur) == True:
                cchar = ign
                proceed2 = True
            else:
                print("- Character not found.")

    # Gets csv filename from user and checks if it exists, requests permission to overwrite if necessary
    if proceed2 == True:
        file = getstr("\nName of csv file: ")
        if file != "":
            if file.endswith(".csv") == False:
                file = file + ".csv"
            if pathlib.Path(file).is_file() == True:
                consent = getstr("\n- File '" + file + "' already exists. Overwrite file?\n[Y]= Yes, [N]= No: ").lower()
                if consent == "y":
                    proceed3 = True
            elif pathlib.Path(file).is_file() == False:
                proceed3 = True

    # Exports to csv
    if proceed3 == True:
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

    return cchar



# 4C: Instructions
def importinstr():
    print("\n>> Instructions for importing csv files")
    print("""- The first row of your csv should contain the headers "date", "armor", "wtd", "acc" (case-sensitive).""")
    print("- Rows should not have blank cells.")
    print("""- Values in the "date" column should formatted as such: "MM/DD/YY".""")



# 5A: Add character
def addchar(sql, cur, cchar):
    print("\n>> Add char")

    proceed = False

    # Gets char name
    ign = getstr("Character Name: ").lower()
    table = ign + "_conv"

    # Checks char name and if char exists in db
    if namevalid(ign) == True:
        if tablevalid(table, sql, cur) == False:
            proceed = True
        else:
            print("- Character already in database.")

    # Creates table for char
    if proceed == True:
        action = """CREATE TABLE """ + table + """ (date NUMERIC NOT NULL PRIMARY KEY, armor INTEGER, wtd INTEGER, acc INTEGER);"""
        try:
            cur.execute(action)
            sql.commit()
            print("- Character added.")
            cchar = ign

        except sqlite3.Error as e:
            print(e)

    return cchar



# 5B: Remove character
def removechar(sql, cur, cchar):
    print("\n>> Remove char")

    proceed = False
    proceed2 = False
    proceed3 = False

    # Checks whether to proceed with current char
    consent = getstr("Delete data for '" + cchar.capitalize() + "'?\n[Y]= Yes, [N]= Change char: ").lower()
    if consent == "y":
        ign = cchar
        table = ign + "_conv"
        proceed = True
    elif consent == "n":
        ign = getstr("\nCharacter Name: ").lower()
        table = ign + "_conv"
        proceed = True

    # Checks char name and if char exists in db
    if proceed == True:
        if namevalid(ign) == True:
            if tablevalid(table, sql, cur) == True:
                cchar = ign
                proceed2 = True
            else:
                print("- Character not found.")

    # Gets permission from user to delete data
    if proceed2 == True:
        consent = input("""\nTo delete all data for '""" + ign + """', please enter "Delete character": """).lower()
        if consent == "delete character":
            proceed3 = True

    # Drops table for char
    if proceed3 == True:
        action = """DROP TABLE """ + table + """;"""
        try:
            cur.execute(action)
            sql.commit()
            print("- Deleted.")
            cchar = curchar(sql, cur)

        except sqlite3.Error as e:
            print(e)

    return cchar



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
def getfrag(x):

    while True:
        try:
            i = input(x)
        except:
            print("- Please key in a number from 10 - 1000.")
            continue
        if i.isdigit() == True and int(i) <= 1000 and int(i) >= 10:
            break
        elif i == "" or i == "n":
            return str(i)
        else:
            print("- Please key in a number from 10 - 1000.")
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
cchar = curchar(sql, cur)
main(sql, cur, cchar)