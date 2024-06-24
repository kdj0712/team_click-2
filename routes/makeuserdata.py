# from fastapi import FastAPI, APIRouter, Request, Form
# from starlette.responses import HTMLResponse
# from beanie import init_beanie, Document, PydanticObjectId
# from databases.individual_connections import Personal_Settings
# from models.user_info import User_info
# from pymongo import MongoClient
# import os
# router = APIRouter()
# app = FastAPI()
# collection_user = Personal_Settings()


# class User(Document):
#     class Settings:
#         collection = "user_info" 



# # @app.on_event("startup")
# # async def on_startup():
# #     await collection_user.initialize_database()



# # @app.post("/activity/{user_id}")
# # async def ne(user_id: str, activity: Activity):
# #     activity.user_id = PydanticObjectId(user_id)
# #     await activity.insert()
# #     return {"activity_id": str(activity.id)}




# # @app.post("/join/step4")
# # async def signup_user(user: User):
# #     await user.insert()
# #     user_db_client = MongoClient(os.getenv("USER_DATABASE_URL"))
# #     user_db = user_db_client['User_database']
# #     user_db.create_collection(str(user.id))
# #     return {"id": str(user.id)}


