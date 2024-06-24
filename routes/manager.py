from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from databases.connections import Database
from typing import Optional
from routes.paginations import Paginations
from databases.mongo_connect import User_info, Gifty_info, Notice, Faq, Ad_main, Ad_create
from beanie import PydanticObjectId

collection_ad_create = Database(Ad_create)
collection_faq = Database(Faq)
collection_notice = Database(Notice)


router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# 로고 클릭했을 때 : 주소 /manager/
@router.get("/") # 펑션 호출 방식
async def usermain(request:Request):
    return templates.TemplateResponse(name="manager/manager_main.html", context={'request':request})

# 회원관리 클릭했을 때 : 주소 /manager/user
@router.get("/user") # 펑션 호출 방식
async def user(request:Request):
    return templates.TemplateResponse(name="manager/user_manage.html", context={'request':request})


# 포인트 통계 클릭했을 때 : 주소 /manager/point
@router.get("/point") # 펑션 호출 방식
async def point(request:Request):
    return templates.TemplateResponse(name="manager/point_data.html", context={'request':request})

# 광고 생성 클릭했을 때 : 주소 /manager/ad
@router.get("/ad") # 펑션 호출 방식
async def ad(request:Request):
    return templates.TemplateResponse(name="manager/ad_manage.html", context={'request':request})


# 광고 리스트 클릭했을 때 : 주소 /manager/adlist
@router.get("/adlist/{page_number}") # 펑션 호출 방식
@router.get("/adlist")
async def ad(request:Request, page_number: Optional[int] = 1):
    try : 
        user_dict = dict(request._query_params)
        ad_list = await collection_ad_create.get_all()
        conditions = { }
        # total = len(ad_list)
        # pagination = Paginations(total,page_number)
        try :
            if user_dict['key'] == "type" :
                if user_dict['word'] == "앱 설치" : user_dict['word'] ="download_app"
                elif  user_dict['word'] == "회원가입" :user_dict['word'] ="join" 
                elif user_dict['word'] == "뉴스레터 구독": user_dict['word'] ="newsletter"    
                elif user_dict['word'] =="사이트 접속": user_dict['word'] = "enter" 
                elif user_dict['word'] == "구매" : user_dict['word'] ="purchase"
            conditions = { user_dict['key'] : { '$regex': user_dict["word"] } }
        except :
            conditions = { }
        ad_list, pagination = await collection_ad_create.getsbyconditionswithpagination(conditions, page_number)
    except :
        pagination=1
        ad_list = await collection_ad_create.get_all()
    return templates.TemplateResponse(name="manager/ad_list.html", context={'request':request,
                                                                            'ad_list':ad_list,
                                                                            'pagination':pagination})


# 광고 생성 클릭했을 때 : 주소 /manager/ad
@router.post("/ad/submit") # 펑션 호출 방식
async def ad(request:Request):
    ad_dict = dict(await request.form())
    ad_info = Ad_create(**ad_dict)
    await collection_ad_create.save(ad_info)

    return templates.TemplateResponse(name="manager/ad_create.html", context={'request':request})

#-----------------------FAQ 부분임당------------------------#

# FAQ 생성/관리 클릭했을 때 : 주소 /manager/faq

@router.get("/faq/{page_number}")
@router.get("/faq") # 펑션 호출 방식
async def listfaq_get(request:Request, page_number: Optional[int] = 1):
    list_faq = await collection_faq.get_all()
    try : 
        user_dict = dict(request._query_params)
        conditions = { user_dict['key'] : { '$regex': user_dict["word"] } }
    except :
        conditions = { }
    list_faq, pagination = await collection_faq.getsbyconditionswithpagination(conditions, page_number)
    return templates.TemplateResponse(name="manager/faq_list.html", context={'request':request,
                                                                             'list_faq':list_faq,
                                                                             'pagination':pagination})
# FAQ 생성 후 완료 클릭했을 때(post방식) : 주소 /manager/faq
@router.get("/faq/{page_number}")
@router.post("/faq") # 펑션 호출 방식
async def listfaq_post(request:Request, page_number: Optional[int] = 1):
    dict_faq = dict(await request.form())
    faq = Faq(**dict_faq)
    await collection_faq.save(faq)
    list_faq = await collection_faq.get_all()
    try : 
        user_dict = dict(request._query_params)
        conditions = { user_dict['key'] : { '$regex': user_dict["word"] } }
    except :
        conditions = { }
    list_faq, pagination = await collection_faq.getsbyconditionswithpagination(conditions, page_number)
    return templates.TemplateResponse(name="manager/faq_list.html", context={'request':request,
                                                                             'list_faq':list_faq,
                                                                             'pagination':pagination})
# FAQ 생성/관리에서 생성 클릭했을 때 : 주소 /manager/faq/delete/object_id
@router.get("/faq/delete/{object_id}")
async def delete_review(request: Request, object_id:PydanticObjectId):
    await collection_faq.delete_one(object_id)

    return templates.TemplateResponse(name="manager/faq_delete.html", context={'request':request})


# FAQ 생성/관리에서 생성 클릭했을 때 : 주소 /manager/faq/create
@router.post("/faq/create") # 펑션 호출 방식
async def createfaq(request:Request):
    return templates.TemplateResponse(name="manager/faq_create.html", context={'request':request})

# -------------------------------공지사항부분임당 ------------------------------------------#
# FAQ 생성/관리 클릭했을 때 : 주소 /manager/notice

@router.get("/notice/{page_number}")
@router.get("/notice") # 펑션 호출 방식
async def listfaq_get(request:Request, page_number: Optional[int] = 1):
    list_notice = await collection_notice.get_all()
    try : 
        user_dict = dict(request._query_params)
        try :
            conditions = { user_dict['key'] : { '$regex': user_dict["word"] } }
        except :
            conditions = { }
    except :
        list_notice, pagination = await collection_notice.getsbyconditionswithpagination(conditions, page_number)
    return templates.TemplateResponse(name="manager/notice_list.html", context={'request':request,
                                                                             'list_notice':list_notice,
                                                                             'pagination':pagination})
# FAQ 생성 후 완료 클릭했을 때(post방식) : 주소 /manager/faq
@router.get("/notice/{page_number}")
@router.post("/notice") # 펑션 호출 방식
async def listfaq_post(request:Request, page_number: Optional[int] = 1):
    dict_notice = dict(await request.form())
    notice = Faq(**dict_notice)
    await collection_faq.save(notice)
    list_notice = await collection_notice.get_all()
    try : 
        user_dict = dict(request._query_params)
        conditions = { user_dict['key'] : { '$regex': user_dict["word"] } }
    except :
        conditions = { }
    list_notice, pagination = await collection_notice.getsbyconditionswithpagination(conditions, page_number)
    return templates.TemplateResponse(name="manager/notice_list.html", context={'request':request,
                                                                             'list_notice':list_notice,
                                                                             'pagination':pagination})
# FAQ 생성/관리에서 생성 클릭했을 때 : 주소 /manager/faq/delete/object_id
@router.get("/notice/delete/{object_id}")
async def delete_review(request: Request, object_id:PydanticObjectId):
    await collection_notice.delete_one(object_id)

    return templates.TemplateResponse(name="manager/notice_delete.html", context={'request':request})

# FAQ 생성/관리에서 생성 클릭했을 때 : 주소 /manager/faq/create
@router.post("/notice/create") # 펑션 호출 방식
async def createfaq(request:Request):
    return templates.TemplateResponse(name="manager/notice_create.html", context={'request':request})




# 관리자 관리 클릭했을 때 : 주소 /manager/manager
@router.get("/manager") # 펑션 호출 방식
async def manager(request:Request):
    return templates.TemplateResponse(name="manager/manager_manage.html", context={'request':request})

