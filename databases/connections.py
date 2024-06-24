from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from databases.mongo_connect import User_info, Gifty_info, Notice, Faq, Ad_main, Ad_create
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from routes.paginations import Paginations
from beanie import PydanticObjectId


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self): # 비동기화 되어 있으므로 즉각적인 반응이 있지는 않지만, 업무 자체는 완료할 수 있도록 한다.
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[User_info,Gifty_info,Notice,Faq,Ad_main,Ad_create])
        
    class Config:
        env_file = ".env"

class Database:
    # model = collection
    def __init__(self,model) -> None:
        self.model = model
        pass
    
    # 전체 리스트
    async def get_all(self):
        documents = await self.model.find_all().to_list() # find({})과 거의 같은 기능
        pass
        return documents
    
    # 상세 보기
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id) # find_one()과 거의 같은 기능
        if doc:
            return doc
        return False
    
    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict) -> [Any]:
        documents = await self.model.find(conditions).to_list()  # find({})
        if documents:
            return documents
        return False
        
    # 저장
    async def save(self, document) -> None:
        await document.create()
        return None
    
    async def getsbyconditionswithpagination(self
                                            , conditions:dict, page_number) -> [Any]:
        # find({})
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number)
        documents = await self.model.find(conditions).skip(pagination.start_record_number).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return False 
    
    # 삭제
    async def delete_one(self, id: PydanticObjectId) -> bool:
        doc = await self.model.get(id)
        if doc:
            await doc.delete()
            return True
        return False


