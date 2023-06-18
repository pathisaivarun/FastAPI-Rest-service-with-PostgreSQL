from pydantic import BaseModel
import datetime

#Below schemas are for update_data and add_data endpoints

class UpdateDataSchema(BaseModel):
    source_id: int
    from_date: datetime.datetime
    to_date: datetime.datetime
    last_update_date: datetime.datetime

class AddDataSchema(BaseModel):
    source: str
    source_tag: str
    source_type: str
    from_date: datetime.datetime
    to_date: datetime.datetime
    last_update_date: datetime.datetime
    frequency: str