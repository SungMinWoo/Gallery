const form = document.getElementById('account-form');
const email = document.getElementById('email');
const name = document.getElementById('name');
const submit_btn = document.getElementById('submit_btn'); // 제출버튼

var phoneNumber = document.getElementById('phoneNumber');

const showError = (input, message, text) => {
    /**
        에러 메세지를 보여주고 box의 border 색을 변화 시킴
    */
    const formControl = input.parentElement;
    formControl.className = 'form-control error';
    const small = formControl.querySelector('small');
    input.value = ''; // 필드 초기화
    submit_btn.setAttribute('data-'.concat(text), 'fail');
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

const isValidEmail = (email) => {
    /**
        이메일 유효성 검사
    */
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (re.test(email.value)) {
    showSuccess(email, 'email')
  } else {
    submit_btn.dataset.email = 'fail'
    showError(email, '이메일이 유효하지 않습니다.', 'email');
  }
}

const checkLength = (input, min, max) => {
    /**
        문자열 길이 확인
    */
    if (input.value.length === min) {
        showError(input, `이름을 입력해주세요.`, 'name')
    } else if (input.value.length > max) {
        showError(input, `이름은  ${max}이하로 입력해주시기 바랍니다.`, 'name')
    } else {
        showSuccess(input, 'name')
    }
}

// 각 필드 focusout 시
email.addEventListener('focusout', (event) => {
    isValidEmail(email);
});

name.addEventListener('focusout', (event) => {
    checkLength(name, 0, 16)
});

phoneNumber.addEventListener('focusout', (event) => {
    if (phoneNumber.value.length === 0){
        showError(phoneNumber, '핸드폰 번호를 입력해주세요.', 'phoneNumber')
    } else{
        showSuccess(phoneNumber, 'phoneNumber')
    }
});

function autoHypenPhone(str){
    /**
        핸드폰 번호 자동완선
    */
    str = str.replace(/[^0-9]/g, '');
    var tmp = '';
    if( str.length < 4){
        return str;
    }else if(str.length < 7){
        tmp += str.substr(0, 3);
        tmp += '-';
        tmp += str.substr(3);
        return tmp;
    }else if(str.length < 11){
        tmp += str.substr(0, 3);
        tmp += '-';
        tmp += str.substr(3, 3);
        tmp += '-';
        tmp += str.substr(6);
        return tmp;
    }else{
        tmp += str.substr(0, 3);
        tmp += '-';
        tmp += str.substr(3, 4);
        tmp += '-';
        tmp += str.substr(7);
        return tmp;
    }
    return str;
}


phoneNumber.onkeyup = function(event){
    /**
        phoneNumber 값이 입력될때마다
    */
    event = event || window.event;
    var _val = this.value.trim();
    this.value = autoHypenPhone(_val);
}



form.addEventListener('submit', e => {
    /**
        제출 버튼 클릭 시 submit btn의 dataset을 확인
    */
    if (submit_btn.dataset.name === 'fail'){
        alert('이름을 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (submit_btn.dataset.email === 'fail'){
        alert('이메일을 확인해주시기 바랍니다.');
        e.preventDefault();
    } else if (submit_btn.dataset.phoneNumber === 'fail'){
        alert('핸드폰 번호를 확인해주시기 바랍니다.');
        e.preventDefault();
    }
});
