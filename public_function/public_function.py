from django.core.paginator import Paginator


def paginator_func(request, data, page=10): # 페이지 기능하는 함수
    '''
        Paginator을 쓰기 위한 함수로 여러 곳에 반복하여 쓰이기 때문에 따로 만듦
        :param data: 페이지를 나눌 데이터
        :param page: 페이지 별로 보여줄 최대 데이터 수
        :return ('django.core.paginator.Page'): 페이지로 나뉜 데이터
    '''
    try:
        paginator = Paginator(data, page)
        page = request.GET.get('page')  # Get 요청시 page 파라미터를 읽음
        paginator_list = paginator.get_page(page)
    except:
        paginator_list = data
    return paginator_list


