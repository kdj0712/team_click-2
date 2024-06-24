from fastapi import FastAPI
app = FastAPI()
# database의 세팅을 바꾸면 한번씩 재실행 시켜줘야 함.
from databases.connections import Settings
settings = Settings()

@app.on_event("startup")
async def init_db() : 
    await settings.initialize_database()
    # database의 세팅을 바꾸면 한번씩 재실행 시켜줘야 함.


from fastapi import Request
from fastapi.templating import Jinja2Templates
from routes.usermain import router as main_router
from routes.manager import router as manager_router
# from routes.positionings import router as second_router
# from routes.users import router as users_router
# from routes.homes import router as home_router
# from routes.quests import router as quest_router
app.include_router(main_router, prefix="/clicktech")
app.include_router(manager_router, prefix="/manager")
# app.include_router(second_router, prefix="/positioning")
# app.include_router(users_router, prefix="/users")
# app.include_router(home_router, prefix="/home")
# app.include_router(quest_router, prefix="/quest")



# html 들이 있는 폴더 위치
templates = Jinja2Templates(directory="templates/")

from fastapi.middleware.cors import CORSMiddleware
# No 'Access-Control-Allow-Origin'
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 접근 가능한 도메인만 허용하는 것이 좋습니다.
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
app.mount("/css", StaticFiles(directory="resources\\css\\"), name="static_css")
app.mount("/img", StaticFiles(directory="resources\\img\\"), name="static_img")

@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse("biz/bizmain.html",{'request':request})

@app.get("/contact")
async def root(request:Request):
    return templates.TemplateResponse("biz/contactus.html",{'request':request})





# @app.get("/manager")
# async def root(request:Request):
#     return templates.TemplateResponse("managermain.html",{'request':request})


# @app.get("/manager")
# async def root(request:Request):
#     return templates.TemplateResponse("managermain.html",{'request':request})

# @app.get("/manager")
# async def root(request:Request):
#     return templates.TemplateResponse("managermain.html",{'request':request})

