import datetime
import pathlib
import sqlite3
import sys



def welcome():

    print("------------------------------")
    print(" Welcome to Convtracker v0.10 ")
    print("------------------------------")



def main(newdb, sql, cur):

    # Todo: Redesign based on checking tables instead of newdb
    if newdb == True:
        print("- Database does not contain any characters. Please add a character.\n")
        addchar(sql, cur)

    while True:
        menu = getstr(">> Conversion Tracker\n[1]= View, [2]= Add/Update, [3]= Import/Export, [4]= Add character, [Q]= Cancel: ").lower()


        if menu == "1":
            print("\n>> View")
            charname = getstr("Character Name: ").lower()

            if len(charname) <= 12 and len(charname) > 0:
                tablename = charname + "_conv"
                action = """SELECT avg(armor), avg(wtd), avg(acc), sum(armor), sum(wtd), sum(acc), count(armor), count(wtd), count(acc) FROM """ + tablename + """;"""

                try:
                    cur.execute(action)
                    data = cur.fetchall()

                    if (data[0])[0] != None and (data[0])[1] != None and (data[0])[2] != None and (data[0])[3] != None and (data[0])[4] != None and (data[0])[5] != None:

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

                except sqlite3.Error:
                    print("- Character not found.")

            print("")
            continue


        # Todo: Handle no character earlier
        elif menu == "2":
            print("\n>> Add/Update")
            charname = getstr("Character Name: ").lower()

            if len(charname) <= 12 and len(charname) > 0:
                tablename = charname + "_conv"
                date = datetime.datetime.now().strftime("%x")
                dateindb = False
                proceed = False

                keepdate = getstr("\n- Add/Update data for today (" + date + ")?\n[Y]= Yes, [N]=Select another date: ").lower()

                if keepdate == "y":
                    proceed = True

                elif keepdate == "n":
                    month = getdate("Month (MM): ")
                    if month != "":
                        day = getdate("Day (DD): ")
                        if day != "":
                            year = getdate("Year (YY): ")

                    if month != "" and day != "" and year != "":
                        date = month + "/" + day + "/" + year
                        proceed = True

                if proceed == True:
                    action = """SELECT rowid FROM """ + tablename + """ WHERE date = ?;"""
                    modifier = ""

                    try:
                        cur.execute(action, (date,))
                        checkdate = cur.fetchone()
                        if checkdate is not None:
                            print("\n- Existing data for " + date + " found.")
                            dateindb = True
                            modifier = "new "
                    except sqlite3.Error as e:
                        print(e)

                    print("\nEnter " + modifier + "values for " + date + ":")
                    armor = getint("Armor: ")
                    if armor != "":
                        wtd = getint("Wtd: ")
                        if wtd != "":
                            acc = getint("Acc: ")

                    if armor != "" and wtd != "" and acc != "":
                        if dateindb == False:
                            action = """INSERT INTO """ + tablename + """ (date, armor, wtd, acc) VALUES (?, ?, ?, ?);"""
                            try:
                                cur.execute(action, (date, armor, wtd, acc))
                                sql.commit()
                                print("- Saved.")
                            except sqlite3.Error as e:
                                print(e)

                        elif dateindb == True:
                            action = """UPDATE """ + tablename + """ SET armor = ?, wtd = ?, acc = ? WHERE date = ?;"""
                            try:
                                cur.execute(action, (armor, wtd, acc, date))
                                sql.commit()
                                print("- Saved.")
                            except sqlite3.Error as e:
                                print(e)

            print("")
            continue


        # Todo: Csv handling
        elif menu == "3":
            print("")
            continue


        elif menu == "4":
            print("\n>> Add character")
            addchar(sql, cur)
            continue


        elif menu == "q":
            print("\nGoodbye.")
            break


        else:
            print("* Invalid input.\n")
            continue

    # Closes connection
    sql.close()



def addchar(sql, cur):

    charname = getstr("Character Name: ").lower()

    if len(charname) <= 12 and len(charname) > 0:
        tablename = charname + "_conv"
        action = """CREATE TABLE """ + tablename + """ (date NUMERIC NOT NULL PRIMARY KEY, armor INTEGER NOT NULL, wtd INTEGER NOT NULL, acc INTEGER NOT NULL);"""
        try:
            cur.execute(action)
            sql.commit()
            print("- Character added.")

        except sqlite3.Error:
            print("- Character already in database.")

    print("")



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



# Yes/No response handler
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



welcome()
# db, newdbstatus = inicheck()
db, newdb = dbcheck()
sql, cur = sqlconnect(db)
main(newdb, sql, cur)