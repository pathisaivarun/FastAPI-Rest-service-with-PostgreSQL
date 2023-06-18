from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import schemas
import database
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta

#Below we are configuring middleware 
app = FastAPI(title = "Rest API using FastAPI with PostgreSQL as Database")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Below we are declaring the session and default table variables
app.db_session = None
app.table = "ecommerce_activity_table"

#Below code will run whenever the application starts
@app.on_event("startup")
def startup():
    app.db_session = database.get_db() #Creating the DB connection
    print("Successfully started the service")

#Below code will run whenever the application stops/shutdown
@app.on_event("shutdown")
def shutdown():
    print("Closing the DB connection")
    database.close_db(app.db_session) #Closing the DB connection

#/get_data endpoint to read data from DB
@app.get("/get_data")
def get_data(source_id: int):
    #Here, we are using sqlalchemy to interact with Postgres DB and reading the data
    query = sqlalchemy.text("select * from {} where source_id={}".format(app.table, source_id))
    db_response = app.db_session.execute(query).mappings().all()
    if len(db_response) > 0:
        return db_response[0]
    else:
        return "No records found for source_id: {}".format(source_id)

#Below method is to check if a record for source_id exists or not. We are returning record status and record(if record available else returning failed message)
def record_exists(source_id: int):
    record = get_data(source_id)
    if record is None or type(record) == str or len(record) == 0:
        return False, {"status" : "failed", "Message" : record}
    return True, record

#Below method is to manipulate data. This will add frequency to from_date and to_date fields
def perform_data_trigger(record):
    frequency = record.get('frequency') or "0M"
    try:
        frequency = int(frequency.replace("M", ""))
        record['from_date'] = record['from_date'] + timedelta(minutes = frequency)
        record['to_date'] = record['to_date'] + timedelta(minutes = frequency)
    except Exception as e:
        print("Not able to add frequency to from_date and to_date. Error: {}".format(e))
        return None
    return record

#/get_data_trigger endpoint to read data with some changes to from_date and to_date
@app.get("/get_data_trigger")
def get_data_trigger(source_id: int):
    status, record = record_exists(source_id)
    if not status:
        return record
    return perform_data_trigger(dict(record))

#./update_data endpoint to update from_date, to_date and last_update_date for a record
@app.put("/update_data")
def update_data(record: schemas.UpdateDataSchema):
    try:
        status, current_record = record_exists(record.source_id)
        if not status:
            return current_record
        query = sqlalchemy.text("update {} set from_date = '{}', to_date = '{}', last_update_date = '{}' where source_id = {}".format(app.table, record.from_date.strftime("%Y-%m-%d %H:%M:%S"), record.to_date.strftime("%Y-%m-%d %H:%M:%S"), record.last_update_date.strftime("%Y-%m-%d %H:%M:%S"), record.source_id))
        app.db_session.execute(query)
    except Exception as e:
        print("Update failed. Error: {}".format(e))
        return {"status" : "failed"}
    return {"status" : "success"}

#./add_data endpoint to insert a new record into DB
@app.post("/add_data")
def add_data(record: schemas.AddDataSchema):
    try:
        query = sqlalchemy.text("insert into {} (source, source_type, source_tag, last_update_date, from_date, to_date, frequency) values('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(app.table, record.source, record.source_type, record.source_tag, record.from_date.strftime("%Y-%m-%d %H:%M:%S"), record.to_date.strftime("%Y-%m-%d %H:%M:%S"), record.last_update_date.strftime("%Y-%m-%d %H:%M:%S"), record.frequency))
        app.db_session.execute(query)
    except Exception as e:
        print("Insert failed. Error: {}".format(e))
        return {"status" : "failed"}
    return {"status" : "success"}

