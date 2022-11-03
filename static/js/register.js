const form = document.getElementById('account-form');
const nickname = document.getElementById('nickname');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password2 = document.getElementById('password2');
const submit_btn = document.getElementById('submit_btn');


const showError = (input, message, text) => {
    /**
    에러 메세지를 보여주고 box의 border 색을 변화 시킴
    */
    const formControl = input.parentElement;
    formControl.className = 'form-control error';
    const small = formControl.querySelector('small');
    submit_btn.setAttribute('data-'.concat(text), 'fail'); // dataset 값 변경
    input.value = '';
    small.innerText = message;
}

const showSuccess = (input, text) => {
    /**
        성공 시 box의 색을 변화시킴
    */
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
    submit_btn.setAttribute('data-'.concat(text), 'success');
}

const isValidEmail = (input) => {
    /**
        이메일 유효성 검사
    */
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (re.test(email.value)) {
        showSuccess(input, 'email');
    } else {
        showError(input, '이메일이 유효하지 않습니다.', 'email');
    }
}

const isValidPassword = (input) => {
    /**
        패스워드 유효성 검사, 제한사항: 8자 이상, 숫자/소문자/특수문자 좋랍
    */
    const re = /^(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;
    if (re.test(input.value)) {
        showSuccess(input, 'password');
    } else {
        showError(input, '비밀번호는 8자 이상, 숫자/소문자/특수문자를 포함해야 합니다.', 'password');
    }
}

const isValidNickname = (input) => {
    /**
        닉네임 유효성 검사, 제한사항: 2~10자 이내의 한글, 영문, 숫자
    */
    const re =  /^[a-zㄱ-ㅎ|ㅏ-ㅣ|가-힣0-9]{2,10}$/;
    if (re.test(input.value)) {
        showSuccess(input, 'nickname');
    } else{
        showError(input, '닉네임은 2~10자 이내의 한글, 영문, 숫자만 사용할 수 있습니다.', 'nickname');
    }
}

const checkPasswordsMatch = (input1, input2) => {
    /**
        패스워드 일치 여부 확인
    */
    if(input1.value !== input2.value) {
        showError(input2, '비밀번호가 일치하지 않습니다.', 'password2');
    }else {
        showSuccess(input2, 'password2')
    }
}

// 각 필드 focusout 시
nickname.addEventListener('focusout', (event) => {
    isValidNickname(nickname);
});

email.addEventListener('focusout', (event) => {
    isValidEmail(email);
});

password.addEventListener('focusout', (event) => {
    isValidPassword(password);
});

password2.addEventListener('focusout', (event) => {
    checkPasswordsMatch(password, password2);
});


form.addEventListener('submit', e => {
    /**
        제출 버튼 클릭 시 submit btn의 dataset을 확인
    */
    if (submit_btn.dataset.nickname === 'fail'){
        alert('닉네임을 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (submit_btn.dataset.email === 'fail'){
        alert('이메일을 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (submit_btn.dataset.password === 'fail'){
        alert('비밀번호를 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (submit_btn.dataset.password2 === 'fail'){
        alert('비밀번호를 확인해주시기 바랍니다.');
        e.preventDefault();
    }
});