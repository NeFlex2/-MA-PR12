from typing import List, Union

from pydantic import BaseModel

#class SQLDocumentBase(BaseModel):
#    title: str
#    body: str

class CreateDocumentModel(BaseModel):
    title: str
    body: str
    
    class Config:
        orm_mode = True
    
class SQLDocument(CreateDocumentModel):
    id: int
    
    class Config:
        orm_mode = True