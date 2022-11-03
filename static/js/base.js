document.addEventListener('DOMContentLoaded', function(){
    const toogleBtn = document.querySelector('.navbar_btn');
    const menu = document.querySelector('.navbar_menu');
    const icons = document.querySelector('.navbar_login');

    toogleBtn.addEventListener('click', () => {
        menu.classList.toggle('active');
        icons.classList.toggle('active');
    });
});