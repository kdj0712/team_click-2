from fastapi import FastAPI, APIRouter, Request, Form, Depends, HTTPException, status, Response, Cookie
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from databases.connections import Database
from databases.mongo_connect import User_info, Gifty_info, Notice, Faq, Ad_main, Ad_create
from typing import Optional
from routes.paginations import Paginations
from databases.mongo_connect import User_info
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import secrets
import bcrypt
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import PyJWTError
templates = Jinja2Templates(directory="templates/")
collection_ad_main = Database(Ad_main)
router = APIRouter()
app = FastAPI()
collection_user = Database(User_info)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Credentials are not valid")
    except PyJWTError:
        raise HTTPException(status_code=400, detail="Credentials are not valid")
    return username 

async def authenticate(userid, userpw):
    user = await User_info.find_one(User_info.user_id == userid) 
    if not user:
        return False
    
    if bcrypt.check_password_hash(user.user_pswd, userpw):
        return user

    return False


@router.post("/")
async def login(userid: str, userpw: str):

    user = await authenticate(userid, userpw)  
    if user:
        token = create_access_token({"sub": str(user.id), "name": user.name})
        response = RedirectResponse("/")  
        response.set_cookie(key="token", value=token)
        return response
    
    return {"error": "Invalid login"}


SECRET_KEY = secrets.token_urlsafe(32)

@app.get("/")
async def index(token: str = Cookie(None)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) 
    username = payload.get("name")

    return templates.TemplateResponse("usermain.html", {"request": Request, "username": username}) 





# 로고 클릭했을 때 : 주소 /clicktech/
@router.get("/") # 펑션 호출 방식
async def usermain(request:Request):
    ad_main = await collection_ad_main.get_all()
    return templates.TemplateResponse(name="usermain.html", context={'request':request,
                                                                     'ad_main':ad_main})

# Log-in 클릭했을 때 : 주소 /clicktech/login # !!html 수정 전!! #
@router.get("/login") # 펑션 호출 방식
async def login(request:Request):
    return templates.TemplateResponse(name="login/new_login.html", context={'request':request}) 

# Sign-in 클릭했을 때 : 주소 /clicktech/join
@router.get("/join") # 펑션 호출 방식
async def join(request:Request):
    return templates.TemplateResponse(name="join/step2.html", context={'request':request})

# Sign-in 클릭했을 때 : 주소 /clicktech/join/step2
# @router.get("/join/step2") # 펑션 호출 방식
# async def join(request:Request):
#     return templates.TemplateResponse(name="join/step2.html", context={'request':request})
@router.get("/join/step3")
@router.post("/join/step3")
async def read_item(request: Request, user_terms1: str = Form('off'), user_terms2: str = Form('off'), user_terms3: str = Form('off'), user_terms4: str = Form('off')):
    return templates.TemplateResponse(name="join/step3.html",context={"request": request, "user_terms1": user_terms1 == 'on', "user_terms2": user_terms2 == 'on', "user_terms3": user_terms3 == 'on', "user_terms4": user_terms4 == 'on'})

app.include_router(router)

# database 의 connections에 정의된 Database 클래스와 user_info collection을 정의한 User_info 클래스를 import

from databases.mongo_connect import User_info
collection_user = Database(User_info)
@router.post("/join/step4") # 펑션 호출 방식
async def user_input_post(request:Request):
    user_dict = dict(await request.form())
    user_dict['point'] = 1000
    try:
        user_dict['user_terms1'] = user_dict.get('user_terms1', 'off')
        user_dict['user_terms2'] = user_dict.get('user_terms2', 'off')
        user_dict['user_terms3'] = user_dict.get('user_terms3', 'off')
        user_dict['user_terms4'] = user_dict.get('user_terms4', 'off')
        user = User_info(**user_dict)
        await collection_user.save(user)
    except Exception as e:
        print(f"Error occurred: {e}") # 키 값에 해당되는 input이 없으면 빈 값이 주어지도록 설정
        user = User_info(user_terms1="on", user_terms2="on", user_terms3="off", user_terms4="off")
        await collection_user.save(user)
    # 리스트 정보
    user_list = await collection_user.get_all()
    return templates.TemplateResponse(name="join/step4.html"
                                      , context={'request':request, "user_info":user_list})

# # Sign-in 클릭했을 때 : 주소 /clicktech/join
# @router.get("/join/step4") # 펑션 호출 방식
# async def join(request:Request):
#     return templates.TemplateResponse(name="join/step4.html", context={'request':request})

from databases.mongo_connect import Ad_create
collection_ad_create = Database(Ad_create)
# 전체리스트 클릭했을 때 : 주소 /clicktech/alllist
@router.get("/alllist/") # 펑션 호출 방식
async def allad(request:Request):
    ad_list = await collection_ad_create.get_all()
    return templates.TemplateResponse(name="offerwall/allad.html", context={'request':request,
                                                                            "ad_list":ad_list})

@router.get("/alllist/{type}") # 펑션 호출 방식
async def allad(request:Request, type):
    conditions = {'type': { '$regex': type }}
    ad_list= await collection_ad_create.getsbyconditions(conditions)
    return templates.TemplateResponse(name="offerwall/allad.html", context={'request':request,
                                                                            "ad_list":ad_list})

# 광고 하나를 클릭했을 때 : 주소 /clicktech/alllist/detail
@router.get("/alllist/detail/{object_id}") # 펑션 호출 방식
async def detailad(request:Request, object_id):
    ad_detail = await collection_ad_create.get(object_id)
    return templates.TemplateResponse(name="offerwall/allad_detail.html", context={'request':request,
                                                                                   "ad_detail":ad_detail})

from databases.mongo_connect import Gifty_info
collection_gifty = Database(Gifty_info)
# 쿠폰교환 클릭했을 때 : 주소 /clicktech/exchange
@router.get("/exchange") # 펑션 호출 방식
async def exchange(request:Request):
    gifty_list = await collection_gifty.get_all()
    return templates.TemplateResponse(name="exchange/gifticon_main.html", context={'request':request, "gifty_list" : gifty_list})

@router.get("/exchange/{gifty_style}") # 펑션 호출 방식
async def exchange(request:Request, gifty_style):
    if gifty_style =="cafe" : gifty_style ="카페"
    if gifty_style =="bake" : gifty_style ="베이커리/도넛/떡"
    if gifty_style =="mart" : gifty_style ="백화점/마트"
    if gifty_style =="icecream" : gifty_style ="아이스크림"
    if gifty_style =="convin" : gifty_style ="편의점"
    if gifty_style =="burger" : gifty_style ="버거/피자"
    if gifty_style =="chicken" : gifty_style ="치킨"
    if gifty_style =="korean" : gifty_style ="한식/중식/분식"
    if gifty_style =="jokbal" : gifty_style ="구이/족발"
    if gifty_style =="restaurant" : gifty_style ="레스토랑/뷔페"
    if gifty_style =="fusion" : gifty_style ="외국/퓨전/기타"
    if gifty_style =="movie" : gifty_style ="영화/음악/도서"
    if gifty_style =="commu" : gifty_style ="kt/통신"
    if gifty_style =="beauty" : gifty_style ="뷰티/헤어/바디"
    if gifty_style =="health" : gifty_style ="건강/리빙/식품관"
    if gifty_style =="enter" : gifty_style ="생활/가전/엔터"
    condition = {'gifty_style':{'$regex':gifty_style}}
    gifty_list = await collection_gifty.getsbyconditions(condition)
    return templates.TemplateResponse(name="exchange/gifticon_main.html", context={'request':request,"gifty_list" : gifty_list})

from beanie import PydanticObjectId
# 쿠폰교환페이지에서 쿠폰 하나를 클릭했을 때 : 주소 /clicktech/exchange/detail
@router.get("/exchange/detail/{object_id}") # 펑션 호출 방식
async def exchange(request:Request, object_id : PydanticObjectId):
    gifty = await collection_gifty.get(object_id)
    return templates.TemplateResponse(name="exchange/gifticon_detail.html", context={'request':request, "gifty": gifty})

# 쿠폰교환페이지에서 쿠폰구매를 눌렀을 때 : 주소 /
@router.get("/exchange/order/{object_id}")  # 구매하는 사용자의 ID 필요
async def order(request : Request, object_id : PydanticObjectId ) :
    # collection_user.get_all 엥 근데 이거 나중에 해야할듯....? 그럼 모든 페이지에 사용자의 ID가 있어야 함
    gifty = await collection_gifty.get(object_id)
    return templates.TemplateResponse(name="exchange/gifticon_order.html", context= {'request':request, "gifty":gifty})


# 쿠폰교환페이지에서 쿠폰구매를 눌렀을 때(로그인이 되지 않았을 경우 로그인 페이지로 이동) : 주소 /


from databases.mongo_connect import Notice
collection_notice = Database(Notice)
# notice_title, main_text, date
# 공지사항 클릭했을 때 : 주소 /clicktech/notice
@router.get("/notice/{page_number}") # 펑션 호출 방식
async def notice(request:Request):
    notice_list = await collection_notice.get_all()
    return templates.TemplateResponse(name="notice/notice_main.html", context={'request':request, 'notice_list' : notice_list})

# 공지사항의 글 하나를 클릭했을 때 : 주소 /clicktech/notice/{id}
@router.get("/notice/{page_number}/{object_id}") # 펑션 호출 방식
async def notice(request:Request, object_id : PydanticObjectId):
    notice = await collection_notice.get(object_id)
    return templates.TemplateResponse(name="notice/notice_detail.html", context={'request':request, 'notice' : notice})

from databases.mongo_connect import Faq
from typing import Optional
# # FAQ 클릭했을 때 : 주소 /clicktech/faq
collection_faq = Database(Faq)
@router.get("/faq/{page_number}")
@router.get("/faq")
async def faq_list(request:Request, page_number: Optional[int] = 1):
    await request.form()
    list_faq = await collection_faq.get_all()
    print(list_faq)
    conditions = { }
    list_faq, pagination = await collection_faq.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="faq/faq_main.html"
                                      , context={'request':request,
                                                 'list_faq' : list_faq,
                                                'pagination': pagination })


