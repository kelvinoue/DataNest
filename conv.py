# import configparser
import datetime
import pathlib
import sqlite3
import sys


def welcome():

    # Welcome message
    print("------------------------------")
    print(" Welcome to Convtracker v0.01 ")
    print("------------------------------")



def main(sql, cur):

    while True:
        menu = getstr(">> Conversion Tracker\n[1]= View, [2]= Add entry, [3]= Modify entry, [4]= New database, [5]= Export, [Q]= Cancel: ").lower()


        if menu == "1":
            print("\n>> View")
            charname = getstr("Main character name: ").lower()

            if len(charname) <= 12 and len(charname) > 0:
                tablename = charname + "_conv"

                action = """SELECT avg(armor), count(armor), sum(armor), avg(wtd), count(wtd), sum(wtd), avg(acc), count(acc), sum(acc) FROM """ + tablename

                try:
                    cur.execute(action)
                    view = cur.fetchall()

                    ocount = (view[0])[1] + (view[0])[4] + (view[0])[7]
                    ototal = (view[0])[2] + (view[0])[5] + (view[0])[8]
                    oavg = round(ototal / ocount, 1)

                    print("")
                    print("[Armor] Avg:" + str(round((view[0])[0], 1)) + ", Count:" + str((view[0])[1]) + ", Total:" + str((view[0])[2]))
                    print("  [Wtd] Avg:" + str(round((view[0])[3], 1)) + ", Count:" + str((view[0])[4]) + ", Total:" + str((view[0])[5]))
                    print("  [Acc] Avg:" + str(round((view[0])[6], 1)) + ", Count:" + str((view[0])[7]) + ", Total:" + str((view[0])[8]))
                    print("  [All] Avg:" + str(oavg) + ", Count:" + str(ocount) + ", Total:" + str(ototal))

                except sqlite3.Error:
                    print("* Error: Character not found.")

            print("")
            continue


        elif menu == "2":
            print("\n>> Add entry")
            charname = getstr("Main character name: ").lower()

            if len(charname) <= 12 and len(charname) > 0:
                tablename = charname + "_conv"
                date = datetime.datetime.now().strftime("%x")

                print("\nValues for " + date + ":")
                armor = getint("Armor: ")
                wtd = getint("Wtd: ")
                acc = getint("Acc: ")

                if armor != "" and wtd != "" and acc != "":
                    action = """INSERT INTO """ + tablename + """ (date, armor, wtd, acc) VALUES (?, ?, ?, ?)"""

                    try:
                        cur.execute(action, (date, armor, wtd, acc))
                        sql.commit()
                        print("* Added to database.")

                    except sqlite3.Error:
                        print("* Error: Data has already been updated today or character does not exist.")

            print("")
            continue


        elif menu == "3":
            print("")
            continue


        elif menu == "4":
            print("\n>> New database")
            charname = getstr("Main character name: ").lower()

            if len(charname) <= 12 and len(charname) > 0:
                tablename = charname + "_conv"
                action = """CREATE TABLE """ + tablename + """ (date NUMERIC NOT NULL PRIMARY KEY, armor INTEGER NOT NULL, wtd INTEGER NOT NULL, acc INTEGER NOT NULL)"""

                try:
                    cur.execute(action)
                    sql.commit()
                    print("* Added to database.")

                except sqlite3.Error:
                    print("* Error: Character already in database.")

            print("")
            continue


        elif menu == "5":
            print("")
            continue


        elif menu == "q":
            print("\nGoodbye.")
            break

        else:
            print("* Invalid input.\n")
            continue


    # Closes connection
    sql.close()



"""
# Ini/Config checker
def inicheck():

    # Defines ini path + local variables for checking ini and db
    inipath = pathlib.Path('config.ini')
    configexists = False
    configreset = False
    newdbstatus = False

    # Triggers configreset if ini file is missing
    if inipath.is_file() == False:
        configreset = True

    # Triggers configexists + configreset if ini file exists but keys and/or values are invalid
    else:
        configcheck = configparser.ConfigParser()
        configcheck.read("config.ini")

        if configcheck.has_option("Settings", "convdb") == False or configcheck.get("Settings","convdb") == "" or configcheck.get("Settings","convdb").endswith(".db") == False:
            configexists = True
            configreset = True
        else:
            db = configcheck.get("Settings","convdb")

    # Resets ini file
    if configreset == True:

        # Requests permission from user if file already exists
        if configexists == True:
            print("Configuration error detected. Reset to default configuration?")
            yesno()
            print("")

        while True:
            dbname = getstr("Enter a name for your conversion database: ")

            if len(dbname) <= 10 and len(dbname) > 0:
                configset = configparser.ConfigParser()
                configset.add_section("Settings")
                configset.set("Settings","convdb", dbname + ".db")

                ini = open("config.ini", "w")
                configset.write(ini)
                ini.close()

                db = dbname + ".db"
                newdbstatus = True

                print("* Configuration saved to 'config.ini'.\n")
                break

            elif dbname == "":
                print("* No input detected. Try again?")
                yesno()
                print("")
                continue

            else:
                print("* Database name must be 1 to 10 alphanumeric characters long.\n")
                continue

    return db, newdbstatus
    """



# Db checker
def dbcheck():

    # Creates new db file if missing
    db = "conv.db"
    dbpath = pathlib.Path(db)

    if dbpath.is_file() == False:

        """
        if newdbstatus == False:
            print("Database not found. Create new database '" + db + "'?")
        else:
        """

        print("Create new database '" + db + "'?")
        yesno()

        open(db, "w").close()
        print("* Database created.\n")

    return db



# SQL connector
def sqlconnect(db):

    # Todo: Handle failed connnections
    # Connects to db file
    sql = sqlite3.connect(db)
    cur = sql.cursor()

    return sql, cur



# Yes/No response handler
def yesno():

    while True:
        try:
            response = input("[Y]= Yes, [Q]= No/Quit: ").lower()
        except:
            print("\n* Please select a valid option.")
            continue
        if response == "y":
            break
        elif response == "q":
            print("\nGoodbye.")
            sys.exit(1)
        else:
            print("\n* Please select a valid option.")
            continue



def getstr(x):

    while True:
        try:
            s = input(x)
        except:
            print("* Please use alphanumeric characters.\n")
            continue
        if s.isalnum() == True:
            break
        elif s == "":
            break
        else:
            print("* Please use alphanumeric characters.\n")
            continue

    return s



def getint(x):

    while True:
        try:
            i = input(x)
        except:
            print("* Please key in a number.")
            continue
        if i.isdigit() == True:
            break
        elif i == "":
            return str(i)
        else:
            print("* Please key in a number.")
            continue

    return int(i)



welcome()
# db, newdbstatus = inicheck()
db = dbcheck()
sql, cur = sqlconnect(db)
main(sql, cur)