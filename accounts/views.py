from django.shortcuts import render, redirect
from django.contrib import messages

from argon2 import PasswordHasher

from .models import User, Artist
from public_function.decorator import login_session, logout_session


@logout_session
def login(request):
    '''
        로그인 페이지
        :url: '/accounts/register'
        :GET method: 로그인 페이지
        :POST method: 유저의 존재 유무를 먼저 확인 후 PasswordHasher로 암호화된 비밀번호와 사용자가 입력한 비밀번호를
                      비교하여 맞다면 세션 생성과 함께 메인 페이지로 이동
    '''
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST['userEmail']
        password = request.POST['userPassword']

        if User.objects.filter(email=email).exists(): # 유저가 존재한다면
            user = User.objects.get(email=email)
            if user.authority == 'M': # 관리자일 경우 데이터베이스에서 생성하여 PasswordHasher가 안된 상태로 저장됨
                if user.password == password:
                    check_password = True
                else:
                    check_password = False
            else:
                check_password = PasswordHasher().verify(user.password, password)  # 비밀번호 암호화
            if check_password:
                request.session['Session'] = {'nickname':user.nickname, 'authority':user.authority} # 세션생성
                return redirect('/')
            else:
                messages.warning(request, '이메일 혹은 비밀번호가 일치하지 않습니다.')
                return render(request, 'login.html')
        else:
            messages.warning(request, '이메일 혹은 비밀번호가 일치하지 않습니다.')
            return render(request, 'login.html')


@login_session
def logout(request):
    '''
        로그아웃
        :url: '/accounts/logout'
        :GET method: 세션 삭제
    '''
    del request.session['Session']
    return redirect('/')


@logout_session
def register(request):
    '''
        회원가입 페이지
        :url: '/accounts/register'
        :GET method: 회원 가입 신청 페이지
        :POST method: 이메일과 닉네일을 찾고 있다면 입력한 값과 함께 다시 신청 페이지로 반환 없다면 password에 Hash 암호화 후 저장
    '''
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        email = request.POST['userEmail']
        nickname = request.POST['userNickname']
        password = request.POST['userPassword']

        user = User.objects.filter(email=email).exists() # 이메일 찾기
        user_nick = User.objects.filter(nickname=nickname).exists()  # 닉네임 찾기
        if not user and not user_nick:
            user = User(
                email=email,
                nickname=nickname,
                password=PasswordHasher().hash(password),
            )
            try:
                user.save()
                messages.info(request, '회원가입이 완료되었습니다.')
                return render(request, '../../main/templates/main.html')  # 메인화면으로 이동
            except:
                messages.error(request, '오류가 발생하여 다시 시도해주시기 바랍니다.')
                return render(request, 'register.html')
        elif user:
            context = {'nickname':nickname, 'email':email}
            messages.error(request, '이미 존재하는 이메일 입니다.')
            return render(request, 'register.html', context)
        elif user_nick:
            context = {'nickname': nickname, 'email': email}
            messages.error(request, '이미 존재하는 이메일 입니다.')
            return render(request, 'register.html', context)


@login_session
def register_artist(request):
    '''
        작가의 신청 페이지
        :url: '/accounts/register/artist'
        :GET method: 이미 작가로 등록이 되어 있다면 메인 페이지로 반환
        :POST method: 등록하려는 이메일과 같으면 이전에 입력한 값과 함께 반환하고 없다면 Artist 신청서 저장
    '''
    if request.method == 'GET':
        nickname = request.session['Session']['nickname']
        user = User.objects.get(nickname=nickname)
        if Artist.objects.filter(user_nickname=user).exists():
            messages.warning(request, '이미 등록하셨습니다.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return render(request, 'register_artist.html')
    elif request.method == 'POST':
        nickname = request.session['Session']['nickname']
        name = request.POST['userName']
        gender = request.POST['userGender']
        birth = request.POST['userBirth']
        email = request.POST['userEmail']
        phonenumber = request.POST['userPhoneNumber']

        if Artist.objects.filter(email=email).exists():
            context = {
                'name':name,
                'email':email,
                'phonenumber':phonenumber,
                'gender':gender,
                'birth': birth,
            }
            messages.error(request, '이미 존재하는 이메일 입니다.')
            return render(request, 'register_artist.html', context)
        else:
            user = User.objects.get(nickname=nickname)
            artist = Artist(
                user_nickname=user,
                name=name,
                gender=gender,
                birth_date=birth,
                email=email,
                phone_number=phonenumber,
            )
            try:
                artist.save()
                messages.info(request, '작가 등록이 완료되었습니다.')
                return render(request, '../../main/templates/main.html')
            except:
                messages.error(request, '오류가 발생하여 다시 시도해주시기 바랍니다.')
                return render(request, 'register_artist.html')


