const form = document.getElementById('account-form');
const email = document.getElementById('email');
const password = document.getElementById('password');

form.addEventListener('submit', e => {
    /**
        submit 버튼 클릭시 각 필드의 길이를 보고 이벤트 제한
    */
    if (email.value.length === 0){
        alert('이메일을 입력해주세요.');
        e.preventDefault();
    } else if (password.value.length === 0){
        alert('비밀번호를 입력해주세요.');
        e.preventDefault();
    }
});