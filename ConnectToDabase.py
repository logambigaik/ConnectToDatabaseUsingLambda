import json
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

def lambda_handler(event, context):
    # TODO implement
    connection = mysql.connector.connect(host='mysqldb.c79sd2kyheg7.us-east-1.rds.amazonaws.com',
                                        database='employeedb',
                                        user='admin',
                                        password='Naresh#240')
    mysql_insert_query = "insert into employee (empid, ename, salary) values(%s, %s, %s)"
    
    rows=[['101','Naresh','1000'],['102','Suresh','2000']]
    cursor = connection.cursor()
    cursor.executemany(mysql_insert_query,rows)
    connection.commit()

    print(cursor.rowcount, " rows inserted successfully")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }        
