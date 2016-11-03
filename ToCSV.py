from eca import *
import exe_sql as sql
import datetime
import urllib.request

def getcsv():

    sql.begin()     #starts a connection to the database
    result = sql.cur.execute('SELECT * FROM ORDERS')        #selects all data from the orders table
    data = result.fetchall()
    csv_data = ''
    for item in [data]:
        z = len(item) - 1
        while z >= 0:
            csv_data += '{},{},{},{}\r\n'.format(data[z][0], data[z][1], data[z][2], data[z][3])
            z -= 1
    filename = './template_static/csv/Order_list_{0}.csv'.format(datetime.datetime.now().strftime('%d-%m-%Y'))   #creates a csv file
    csv_out = open(filename, 'w')
    csv_out.write(csv_data)     #fills the csv file with csv_data from the orders table
    csv_out.close()             #closes the csv file
    urllib.request.urlretrieve("http://localhost:8080/%s" % filename, filename)
    sql.end()                   #ends the database connection


