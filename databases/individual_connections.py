# from typing import Any, List, Optional
# from beanie import init_beanie, PydanticObjectId, Document
# from models.user_info import User_info
# from motor.motor_asyncio import AsyncIOMotorClient
# from pydantic_settings import BaseSettings
# from pymongo import MongoClient
# from fastapi import FastAPI
# app = FastAPI()

# class Personal_Settings(BaseSettings):
#     USER_DATABASE_URL: Optional[str] = None

#     async def initialize_database(self, collections: List[Document]):
#         client = AsyncIOMotorClient(self.USER_DATABASE_URL)
#         await init_beanie(database=client.get_default_database(), document_models=collections)
        
#     class Config:
#         env_file = ".env"

# class Database:
#     # model = collection
#     def __init__(self,model) -> None:
#         self.model = model
#         pass
    
#     # 전체 리스트
#     async def get_all(self):
#         documents = await self.model.find_all().to_list() # find({})과 거의 같은 기능
#         pass
#         return documents
    
#     # 상세 보기
#     async def get(self, id: PydanticObjectId) -> Any:
#         doc = await self.model.get(id) # find_one()과 거의 같은 기능
#         if doc:
#             return doc
#         return False
    
#     # column 값으로 여러 Documents 가져오기
#     async def getsbyconditions(self, conditions:dict) -> [Any]:
#         documents = await self.model.find(conditions).to_list()  # find({})
#         if documents:
#             return documents
#         return False
        
#     # 저장
#     # async def save(self, document) -> None:
#         await document.create()
#         return None