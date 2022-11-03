const form = document.getElementById('product-form');
const title = document.getElementById('artTitle');
const price = document.getElementById('artPrice');
const size = document.getElementById('artSize');
const image = document.getElementById('artImage');

form.addEventListener('submit', e => {
    /**
        submit 클릭 시 각 필드 문자열 검사 후 제한
    */
    if (title.value.length === 0){
        alert('제목을 입력해주시기 바랍니다.');
        e.preventDefault();
    } else if (price.value.length === 0){
        alert('가격을 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (size.value.length === 0){
        alert('호수를 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (image.value.length === 0){
        alert('이미지를 골라주세요');
        e.preventDefault();
    }
});

function minMaxCheck(object){
    /**
        size의 최대값 최소값 제한
    */
    if(object.value>500){
        object.value=500;
    }
    else if (object.value<1){
        object.value=1;
    }
}

function getNumber(obj){
    /**
        각 자리수마다 숫자 자르기
    */
    var num01;
    var num02;
    num01 = obj.value;
    num02 = num01.replace(/\D/g,"");

    num01 = setComma(num02);
    obj.value =  num01;

}
function setComma(n) {
    /**
        특수문자를제거하고 3개씩 나누어 리턴
    */
    var reg = /(^[+-]?\d+)(\d{3})/;
    n += '';
    while (reg.test(n)) {
    n = n.replace(reg, '$1' + ',' + '$2');
    }
    return n;
}


