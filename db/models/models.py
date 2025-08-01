from pydantic import ConfigDict, BaseModel, Field
from bson.objectid import ObjectId
from datetime import datetime

class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    msisdn: str
    organization_id: str
    date: datetime = Field(default_factory=datetime.now)
    chat_history: str = ""
    status: int = 1

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        populate_by_name=True
    )
