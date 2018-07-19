__author__ = 'nickyuan'

from pymongo import *
import os

# ------------------------- 通用配置 --------------------------
config_dict = dict(
    MOVIE_PIC_DIR=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "movie_pic"),
    MOVIE_FILE_DIR=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "movies"),
    USER_AVATAR_DIR=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "user_avatar"),
    MOVIE_PIC_EXT='png',
    # CDN_URL='http://opguqe876.bkt.clouddn.com/',
    # CDN_USER_AVATAR_DIR='/user_avatar/',
    # CDN_PRODUCT_PIC_DIR='/movie_pic/',
    # CDN_BUCKET='buy-suzumiya',
    # QINIU_CALLBACK_URL='https://buy.suzumiya.cc/callback/all',
    PIC_UPLOAD_URL='https://up-z1.qbox.me/',
    SEND_EMAIL_URL='https://api.mailgun.net/v3/mg.suzumiya.cc/messages',
    SEND_EMAIL_FROM='Suzumiya <no-replay@mg.suzumiya.cc>',
    BASE_URL='http://localhost:8001',
    MAX_CONTENT_LENGTH=20 * 1024 * 1024,
    ALLOWED_UPLOAD_TYPE=['jpg', 'jpeg', 'gif', 'png', 'ico', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'],
)

# mongodb config
db_name = 'YuanTube'
client = MongoClient("mongodb://localhost:27017")
db = client[db_name]
