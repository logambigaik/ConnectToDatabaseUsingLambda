import json
import boto3
import csv
import mysql.connector
import os
s3_client = boto3.client('s3')
session = boto3.session.Session()
client = session.client(
            service_name='secretsmanager',
            region_name=os.environ['MY_AWS_REGION']
        )
def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    csv_file_obj = s3_client.get_object(Bucket=bucket, Key=csv_file)
    lines = csv_file_obj['Body'].read().decode('utf-8').split()
    results = []
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results)
    print(event)

    get_secret_value_response = client.get_secret_value(
                SecretId=os.environ['SECRET_NAME']
            )
    print(get_secret_value_response)
    mysql_username_secret=get_secret_value_response['SecretString']
    print(mysql_username_secret)
    secret = get_secret_value_response['SecretString']
    j = json.loads(secret)
    password = j['password']
    engine = j['engine']
    host = j['host']
    port = j['port']
    dbname = j['dbname']
    print(password)
    print(engine)
    connection = mysql.connector.connect(host=j['host'],
                                         database=j['dbname'],
                                         port=j['port'],
                                         user=j['username'],
                                         password=j['password'])
    print(connection)
    mycursor = connection.cursor()
    mysql_insert = "insert into employee(empid,empname,empaddres) values(%s,%s,%s)"
    
    cursor = connection.cursor()
    cursor.executemany(mysql_insert, results)
    connection.commit()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
