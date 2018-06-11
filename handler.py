try:
    import unzip_requirements
except ImportError:
    pass
import json
import sys
import logging
import rds_config
import pymysql

# rds settings
rds_host = rds_config.host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get(event, context):
    #get pathParameters
    #your-url/id
    id = event['pathParameters']['id']

    conn = connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `users` WHERE `id`=%s"
    result = {}
    try:
        # Execute the SQL command
        cursor.execute(sql, (id))
        # Fetch all the rows in a list of lists.
        data = cursor.fetchone()
        result['id'] = data['id']
        

    except Exception as e:
        result['error'] = e

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response

def store(event, context):
    data = json.loads(event['body'])
    result = {}
    conn = connection()
    try:
        sql = "INSERT INTO users (" \
            "first_name"\
            ",last_name" \
            ") VALUES (%s, %s)"
        with conn.cursor() as cur:
            cur.execute(sql, (data['first_name'], data['last_name']))
            conn.commit()
            result['data'] = "data inserted successfully"
    except Exception as e:
        result['error'] = str(e)

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response
    
    

def connection():
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        return conn
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
