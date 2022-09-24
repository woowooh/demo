# demo

## 环境:
* ubuntu 16.04
* Python 2.7.12

## 功能:
* 用户模型，账户验证，登陆，注册(Flask-Login，itsdangerous，Flask-SQLAlchemy, Flask-WTF, Flaks-Mail)；
* 评论管理，权限管理，关注功能,gravatar头像；
* 前端bootstrap，markdown文章富文本，jinja2(PageDown, Flask-PageDown, MarkDown, Bleach)

## Requirements
pip install -r requirements.txt

* python manage.py db init
* python manage.py db migrate
* python manage.py db upgrade
* python manage.py shell -> Role.insert_roles
* python manage.py runserver

Demon at heroku [福蜡斯克](http://woowooh.herokuapp.com/) 略卡…… 
