#-*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class EditProfileForm(Form):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地点', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能包含字母，'
                                          u'数字，点和下划线哦')])
    confirmed = BooleanField(u'已验证')
    role = SelectField(u'权限', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地点', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在.')


class PostForm(Form):
    body = PageDownField(u"想说些什么呢?", validators=[Required()])
    submit = SubmitField(u'提交')


class CommentForm(Form):
    body = StringField(u'输入评论', validators=[Required()])
    submit = SubmitField(u'提交')

class EditProfileForm(Form):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地区', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')

class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                         u'用户名只能包含字母， '
                                         u'数字，点和下划线')])
    confirmed = BooleanField(u'已验证')
    role = SelectField(u'权限', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地点', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在.')

class PostForm(Form):
    body = PageDownField(u"想说些什么呢?", validators=[Required()])
    submit = SubmitField(u'提交')


