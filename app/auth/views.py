#-*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user,current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from flask.ext.login import logout_user, login_required,current_app
from .. import db
from ..email import send_email 

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'无效的用户名或密码')
    return render_template('auth/login.html', form=form)  

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'注销成功')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, u'验证您的账户',
                'auth/email/confirm', user=user, token=token)
        flash(u'系统已经发送了一封验证邮件给您，请注意查收!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'感谢您，验证成功!')
    else:
        flash(u'验证信息无效或过期.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'验证您的账户',
                'auth/email/confirm', user=current_user, token=token)
    flash(u'系统已经发送了一封验证邮件给您，请注意查收!')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'密码已更改')
            return redirect(url_for('main.index'))
        else:
            flash(u'无效的密码.')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset', methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, u'重置您的密码',
                        'auth/email/reset_password',
                        user=user, token=token,
                        next=request.args.get('next'))
        flash(u'成功重置密码.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(u'修改成功.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, u'确认您的邮箱',
                    'auth/email/change_email',
                    user=current_user, token=token)
            flash(u'系统已经发送了一封验证邮件给您，请注意查收!')
            return redirect(url_for('main.index'))
        else:
            flash(u'无效的密码或邮箱')
    return render_template("auth/change_email.html", form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'更改成功.')
    else:
        flash(u'无效的请求.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

