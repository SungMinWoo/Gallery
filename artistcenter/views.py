from django.shortcuts import render, redirect
from django.db.models import OuterRef, Subquery
from django.contrib import messages

from accounts.models import Artist, User
from .models import Product, Exhibit
from public_function.public_function import paginator_func
from public_function.decorator import authority_aritist


@authority_aritist
def artistcenter(request): # 작가 개인 정보 페이지
    '''
        작가의 개인정보 페이지
        :url: '/artistcenter'
        :GET method: 작가의 개인정보를 반환
    '''
    nickname = request.session['Session']['nickname']
    artist = Artist.objects.get(user_nickname__nickname=nickname)
    return render(request, 'artistcenter.html', {'artist':artist})


def product_list(request): # 전체 작품 페이지
    '''
        전체 작품 페이지
        :url: '/artistcenter/product/list'
        :GET method: search가 있으면 product_search 함수로 결과값 반환
    '''
    if request.GET.get('search'):
        products = product_search(request)
    else:
        product = Product.objects.all().order_by('-createdate')
        products = paginator_func(request, product)
    return render(request, 'product_list.html', {'products':products})


def artist_list(request):
    '''
        전체 작가 페이지 작가의 최신 Product와 함께 반환
        :url: '/artistcenter/artist/list'
        :GET method: search가 있으면 artist_search 함수로 결과값 반환
    '''
    if request.GET.get('search'):
        artists = artist_search(request)
    else:
        artist = Artist.objects.filter(check_available='P').annotate(
            photo=Subquery(
                Product.objects.filter(
                    artist_id=OuterRef('user_nickname_id')
                ).order_by('-createdate').values('photo')[:1]
            )
        ).order_by('-joindate')

        artists = paginator_func(request, artist)
    return render(request, 'artist_list.html', {'artists':artists})


@authority_aritist
def artist_product_list(request):
    '''
        작가 제품 등록 및 목록, 가격은 콤마를 제거하여 저장
        :url: '/artistcenter/artist/product/list'
        :GET method: Artist가 등록한 Product를 paginator_func 결과 값을 반환
        :POST method: 작가 페이지 제품 목록으로 redirect
    '''
    if request.method == 'GET':
        nickname = request.session['Session']['nickname']
        user = User.objects.get(nickname=nickname)
        product = Product.objects.filter(artist=user).order_by('-createdate')
        products = paginator_func(request, product)
        return render(request, 'artist_product_list.html', {'products':products})
    elif request.method == 'POST':
        nickname = request.session['Session']['nickname']
        user = User.objects.get(nickname=nickname)
        title = request.POST['artTitle']
        price = request.POST['artPrice']
        size = request.POST['artSize']
        image = request.FILES['artImage']

        product = Product(
            artist=user,
            title=title,
            price=int(price.replace(',', '')),
            size=size,
            photo=image,
        )
        try:
            product.save()
            return redirect('/artistcenter/artist/product/list')
        except:
            messages.warning(request, '오류가 발생하여 다시 시도해주시기 바랍니다.')
            return redirect('/artistcenter/artist/product/list')



@authority_aritist
def exhibit_list(request):
    '''
        작가 전시 일정 등록 및 조회 페이지
        :url: '/artistcenter/exhibit/list'
        :GET method: 작가가 등록한 product와 일정을 반환
        :POST method: 전시 일정 저장 후 현재 페이지로 redirect
    '''
    nickname = request.session['Session']['nickname']
    user = User.objects.get(nickname=nickname)
    if request.method == 'GET':
        products = Product.objects.filter(artist=user)
        exhibit = Exhibit.objects.filter(artist_exhibit=user)
        return render(request, 'exhibit_list.html', {'products':products, 'exhibits':exhibit})
    elif request.method == 'POST':
        art_title = request.POST['artTitle']
        start_date = request.POST['startDate']
        end_date = request.POST['endDate']
        artdata = request.POST.getlist('selectData')

        products = Product.objects.filter(id__in=artdata)
        exhibit = Exhibit(
            artist_exhibit=user,
            exhibit_title=art_title,
            start_date=start_date,
            end_date=end_date,
        )
        try:
            exhibit.save()
            exhibit.exhibit_list.add(*products)
            return redirect('/artistcenter/exhibit/list')
        except:
            messages.warning(request, '오류가 발생하여 다시 시도해주시기 바랍니다.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def product_search(request): # 제품검색
    '''
        제품 검색 함수, Product price는 0.5~1.5 배수로 검색하여 반환
        :return(django.core.paginator.Page): paginator_func 결과 값을 반환
    '''
    keyword = request.GET.get('search')
    choice = request.GET.get('choice')
    if choice == 'title':
        artist_data = Product.objects.filter(title__icontains=keyword).order_by('-createdate')
    elif choice == 'price':
        artist_data = Product.objects.filter(price__gte=int(keyword)*0.5, price__lte=int(keyword)*1.5).order_by('-createdate') ## 범위 검색
    elif choice == 'size':
        artist_data = Product.objects.filter(size__contains=keyword).order_by('-createdate')

    artist_data = paginator_func(request, artist_data)
    return artist_data


def artist_search(request):
    '''
        작가 검색 함수, 개인정보를 위해 이름과 email로만 진행
        subquery를 이용하여 Artist와 Product의 user을 비교하고 photo url 값을 받아옴
        :return(django.core.paginator.Page): paginator_func 결과 값을 반환
    '''
    keyword = request.GET.get('search')
    choice = request.GET.get('choice')
    if choice == 'name':
        artist_data = Artist.objects.filter(check_available='P', name__icontains=keyword).annotate(
            photo=Subquery(
                Product.objects.filter(
                    artist_id=OuterRef('user_nickname_id')
                ).order_by('-createdate').values('photo')[:1]
            )
        ).order_by('-joindate')
    elif choice == 'email':
        artist_data = Artist.objects.filter(check_available='P', email__contains=keyword).annotate(
            photo=Subquery(
                Product.objects.filter(
                    artist_id=OuterRef('user_nickname_id')
                ).order_by('-createdate').values('photo')[:1]
            )
        ).order_by('-joindate')
    artist_data = paginator_func(request, artist_data)
    return artist_data
