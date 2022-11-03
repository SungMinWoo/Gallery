from django.shortcuts import render
from django.contrib import messages


def logout_session(func):
    '''
        로그인 세션 확인 후 접속을 막음
        :param func: 데코레이터를 쓸 함수
        :return: 로그인 세션이 있을 경우 메인 페이지로 msg와 함께 render
    '''
    def wrap(request, *args, **kwargs):
        if 'Session' in request.session.keys():
            messages.warning(request, '로그아웃 후 이용해주세요.')
            return render(request, '../../main/templates/main.html')
        else:
            return func(request, *args, **kwargs)
    return wrap


def login_session(func):
    '''
        로그인 세션 확인 후 접속을 막음
        :param func: 데코레이터를 쓸 함수
        :return: 로그인 세션이 없을 경우 메인 페이지로 msg와 함께 render
    '''
    def wrap(request, *args, **kwargs):
        if 'Session' not in request.session.keys():
            messages.warning(request, '로그인 후 이용해주세요.')
            return render(request, '../../main/templates/main.html')
        else:
            return func(request, *args, **kwargs)
    return wrap


def authority_aritist(func):
    '''
        작가 페이지 접속 시 세션과 비교하여 접근을 막는 함수
        :param func: 데코레이터를 쓸 함수
        :return: 메인 홈페이지로 error msg와 함께 render 또는 view 함수 실행
    '''
    def wrap(request, *args, **kwargs):
        if 'Session' not in request.session.keys():
            messages.warning(request, '잘못된 요청입니다.')
            return render(request, '../../main/templates/main.html')
        else:
            login_session = request.session['Session']['authority']
            if login_session:
                if request.session['Session']['authority'] == 'A':
                    return func(request, *args, **kwargs)
            messages.warning(request, '작가 등록을 해주시기 바랍니다.')
            return render(request, '../../main/templates/main.html')
    return wrap


def authority_admin(func):
    '''
        관리자 페이지 접속 시 세션과 비교하여 접근을 막는 함수
        :param func: 데코레이터를 쓸 함수
        :return: 메인 홈페이지로 error msg와 함께 render 또는 view 함수 실행
    '''
    def wrap(request, *args, **kwargs):
        if 'Session' not in request.session.keys():
            messages.warning(request, '잘못된 요청입니다.')
            return render(request, '../../main/templates/main.html')
        else:
            login_session = request.session['Session']['authority']
            if login_session:
                if request.session['Session']['authority'] == 'M':
                    return func(request, *args, **kwargs)
            messages.warning(request, '잘못된 요청입니다.')
            return render(request, '../../main/templates/main.html')
    return wrap
