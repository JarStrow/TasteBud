const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

menu.addEventListener('click', function() {
    menu.classList.toggle('is-active')
    menuLinks.classList.toggle('active')
})

const navItems = document.querySelectorAll('.nav-item');

navItems.forEach(navItem => {
    navItem.addEventListener('mouseleave', () => {
        navItem.querySelector('.nav-link-sub').style.display = 'none';
    });
});