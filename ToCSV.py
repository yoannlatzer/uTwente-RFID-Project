from eca import *
import exe_sql as sql

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
    filename = 'Order_list.csv'
    path = 'template_static/csv/{}'.format(filename)
    csv_out = open(path, 'w')
    csv_out.write(csv_data)     #fills the csv file with csv_data from the orders table
    csv_out.close()             #closes the csv file
   # urllib.request.urlretrieve("http://localhost:8080/%s" % filename, filename)
    sql.end()                   #ends the database connection
    emit('csv', {'data': filename})


