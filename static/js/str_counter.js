function counter(text, limit){
    /**
        실시간 글자수 세기
    */
    var str = text.value.length;
    if (str > limit){
        text.value = text.value.substring(0,limit);
        text.focus();
    }
    document.getElementById('counter').innerHTML = text.value.length + '/' + limit;
}