import sqlite3
import pathlib

# This script is created to update several tables of data with the most current webscraped data.
# The script is run once a day with help of task scheduler.
# Important, the script is written to only be run once a day, otherwise necessary data for trend visualization will be overwritten.

def updateTables():

    currentdir = str(pathlib.Path(__file__).parent.absolute()) + "\\"
    
    try:
        conn = sqlite3.connect(currentdir+'Flask_Web_App\website\database.db')  
        c = conn.cursor()

        db_list = []
        for db_name in c.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
            db_list.append(db_name)
        

        #Clean list of tables, to ensure the list only contains tables which is related to daily discussion.
        db_list = [table for table in db_list if 'dd' in table[0]]
        db_list.reverse()

        for id in range(len(db_list)):

            #Delete and copy table data except last table. In turn the last table and the next last table will have the same data.
            #Although the last table will within a short amount of time get new webscraped data.
            if id < len(db_list)-1:
                current_table = db_list[id][0]
                next_table = db_list[id + 1][0]

                try:
                    #The data in the current table is deleted and then data from the next table is copied into the current table.
                    c.execute("DELETE FROM " + current_table)
                    conn.commit()

                    c.execute("INSERT INTO " + current_table + " SELECT * FROM " + next_table)
                    conn.commit()

                except sqlite3.Error as e:
                    print(e)


        c.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    updateTables()