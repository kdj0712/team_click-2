from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr


# 광고 생성 리스트
class Ad_create(Document):
    type : Optional[str] = None
    brand : Optional[str] = None
    contents : Optional[str] = None
    thumnail : Optional[str] = None
    thumnail_url : Optional[str] = None
    detail_contents : Optional[str] = None
    point : Optional[int] = None

    class Settings:
        name = "ad_create"

# AD_main 메인페이지 광고
class Ad_main(Document):
    type : Optional[str] = None
    brand : Optional[str] = None
    contents : Optional[str] = None
    thumnail : Optional[str] = None

    class Settings:
        name = "ad_main"

# FAQ
class Faq(Document):
    categories : Optional[str] = None
    question_title : Optional[str] = None
    answer_main_text : Optional[str] = None

    class Settings:
        name = "faq"

# 기프티콘 정보들
class Gifty_info(Document):
    gifty_style : Optional[str] = None
    gifty_image : Optional[str] = None
    gifty_brand : Optional[str] = None
    gifty_name : Optional[str] = None
    gifty_price : Optional[str] = None
    gifty_detail : Optional[str] = None
    gifty_caution : Optional[str] = None
    class Settings:
        name = "gifty_info"

# 공지사항
class Notice(Document):
    notice_title : Optional[str] = None
    main_text : Optional[str] = None
    date : Optional[str] = None

    class Settings:
        name = "notice"

# 사용자 정보
class User_info(Document, BaseModel):
    user_name : Optional[str] = None
    user_id : Optional[str] = None
    user_pswd: Optional[str] = None
    user_phone_num1: Optional[str] = None
    user_phone_num2: Optional[str] = None
    user_phone_num3: Optional[str] = None
    user_email: Optional[str] = None
    user_terms1: Optional[str] = None
    user_terms2: Optional[str] = None
    user_terms3: Optional[str] = None
    user_terms4: Optional[str] = None
    point: Optional[int] = None

    class Settings:
        name = "user_info"

# 사용자 이용내역
