const form = document.getElementById('exhibit-form');
const title = document.getElementById('exhibitTitle');
const start_date = document.getElementById('startDate');
const end_date = document.getElementById('endDate'); // 제출버튼


let startDate = document.getElementById('startDate');
let start = new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, -5);

startDate.value = start;
startDate.setAttribute("min", start);

startDate.addEventListener('change', (event) => {
    /**
        시작일 종료일 맞추기
    */
    let endDate = document.getElementById('endDate');
    let getStartDate = document.getElementById('startDate');

    endDate.disabled = false;
    endDate.value = getStartDate.value;
    endDate.setAttribute("min", getStartDate.value);
});



form.addEventListener('submit', e => {
    /**
        입력값 검사
    */
    var check_value = document.querySelectorAll("input[name='selectData']:checked").length;

    if (title.value.length === 0){
        alert('제목을 입력해주시기 바랍니다.');
        e.preventDefault();
    } else if (end_date.value === ''){
        alert('종료일을 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (check_value === 0){
        alert('작품을 선택해주시기 바랍니다.');
        e.preventDefault();
    }
});