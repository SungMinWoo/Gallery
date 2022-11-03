from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, F, Count, Avg

from public_function.public_function import paginator_func
from public_function.decorator import authority_admin
from accounts.models import Artist, User


@authority_admin
def custom_bulk_update(request, available, approval):
    '''
        일괄 처리를 위해 bulk_update를 사용하고 message를 통해 상태를 관리자에게 알림
        :param available(str): 'P' or 'N'
        :param approval(str): '승인' or 반려'
        :return: messages를 반환하여 업데이트 유무를 html로 반환함
    '''
    bulk_update = []
    user_updates = []
    update_list = request.POST.getlist('updateList')
    query_lists = Artist.objects.filter(email__in=update_list)

    if available == 'N': # 반려
        for query_list in query_lists:
            query_list.check_available = available  # 작가 상태 업데이트
            bulk_update.append(query_list)
        try:
            Artist.objects.bulk_update(bulk_update, ['check_available'])
            messages.info(request, f'{len(query_lists)}개를 {approval}하였습니다.')
        except:
            messages.warning(request, f'{approval}에 실패하였습니다.')
    else: # 승인
        for query_list in query_lists:
            query_list.check_available = available # 작가 상태 업데이트
            query_list.user_nickname.authority = 'A' # 유저 권한 업데이트
            user_updates.append(query_list.user_nickname)
            bulk_update.append(query_list)
        try:
            Artist.objects.bulk_update(bulk_update, ['check_available'])
            User.objects.bulk_update(user_updates, ['authority'])
            messages.info(request, f'{len(query_lists)}개를 {approval}하였습니다.')
        except:
            messages.warning(request, f'{approval}에 실패하였습니다.')


@authority_admin
def custom_admin(request): # 승인 대기 페이지
    '''
        승인 대기 중인 작가 페이지
        :url: '/custom_admin/'
        :GET method: 검색어가 있다면 결과 반한 없다면 Artist check_available가 'W'인 데이터 전체 반환
        :POST method: custom_bulk_update 함수로 결과 반환
    '''
    available = 'W'
    if request.method == 'GET':
        if request.GET.get('search'): # 검색어가 있다면
            artist_data = search(request, available)
        else:
            artist = Artist.objects.filter(check_available=available).order_by('-joindate')
            artist_data = paginator_func(request, artist)
        return render(request, 'custom_admin.html', {'artist': artist_data, 'available': available})

    elif request.method == 'POST':
        if request.POST['approval'] == '승인':
            custom_bulk_update(request, 'P', request.POST['approval'])
        else:
            custom_bulk_update(request, 'N', request.POST['approval'])
        return redirect('/custom_admin')


@authority_admin
def admin_approval(request):
    '''
        승인된 작가 목록 페이지
        :url: '/custom_admin/approval'
        :GET method: 검색어가 있다면 결과 반한 없다면 Artist check_available가 P인 데이터 전체 반환
        :return(django.core.paginator.Page): paginator_func 결과 값과 권한을 반환
    '''
    available = 'P'
    if request.method == 'GET':
        if request.GET.get('search'): # 검색어가 있다면
            artist_data = search(request, available)
        else:
            artist = Artist.objects.filter(check_available=available).order_by('-joindate')
            artist_data = paginator_func(request, artist)
        return render(request, 'custom_admin.html', {'artist': artist_data, 'available': available})


@authority_admin
def admin_disapproval(request):
    '''
        작가 반려 페이지
        :url: '/custom_admin/disapproval'
        :GET method: 검색어가 있다면 결과 반한 없다면 Artist check_available가 N인 데이터 전체 반환
        :POST method: custom_bulk_update 함수로 결과 반환
    '''
    available = 'N'
    if request.method == 'GET':
        if request.GET.get('search'): # 검색어가 있다면
            artist_data = search(request, available)
        else:
            artist = Artist.objects.filter(check_available=available).order_by('-joindate')
            artist_data = paginator_func(request, artist)
        return render(request, 'custom_admin.html', {'artist': artist_data, 'available': available})
    elif request.method == 'POST':
        if request.POST['approval'] == '승인':
            custom_bulk_update(request, 'P', request.POST['approval'])
        else:
            custom_bulk_update(request, 'N', request.POST['approval'])
        return redirect('/custom_admin')


@authority_admin
def search(request, available): # 검색
    '''
        artist 검색 함수
        :param request: request
        :param available: 작가 등록 여부에 대한 parameter 'P': 통과, 'N': 불가, 'W': 대기
        :return(django.core.paginator.Page): paginator_func 결과 값을 반환
    '''
    keyword = request.GET.get('search')
    choice = request.GET.get('choice')
    artist_data = Artist.objects.filter(check_available=available)
    if choice == 'name':
        artist_data = artist_data.filter(name__icontains=keyword).order_by('-joindate')
    elif choice == 'gender':
        artist_data = artist_data.filter(gender__icontains=keyword).order_by('-joindate') ## value로 검색하는 법 찾아야함
    elif choice == 'birth':
        artist_data = artist_data.filter(birth_date__contains=keyword).order_by('-joindate')
    elif choice == 'email':
        artist_data = artist_data.filter(email__icontains=keyword).order_by('-joindate')
    elif choice == 'phonenumber':
        artist_data = artist_data.filter(phone_number__contains=keyword).order_by('-joindate')

    artist_data = paginator_func(request, artist_data, 10)
    return artist_data


@authority_admin
def artist_stats(request):
    '''
        작가 통계 페이지로 다양한 통계를 반환해줍니다.
        url: 'agadmin/stats'
        :param request: request
        :return(queryset): values 순서대로 작가 이름, 닉네임, 작품 개수, 평균 가격, 평균 사이즈, 100호 이하 작품
    '''
    artists = User.objects.filter(authority='A')\
        .annotate(product_count=Count(F('artist_product')))\
        .annotate(price_avg=Avg(F('artist_product__price')))\
        .annotate(size_avg=Avg(F('artist_product__size')))\
        .annotate(size_count=Count('artist_product__size', filter=(Q(artist_product__size__lte=100))))\
        .values('artist__name', 'nickname', 'product_count', 'price_avg', 'size_avg', 'size_count')

    return render(request, 'admin_stats.html', {'artists':artists})