function open_popup() {
    let popup = document.getElementById('popup');
    popup.show();
}

function close_popup({target}) {
    let popup = document.getElementById('popup');
    let popup_but = document.getElementById('popup_but');

    if ((!(target === popup || popup.contains(target))) && target != popup_but) {
        popup.close()
    }
}

document.addEventListener('click', close_popup)

function show_cart() {
    let cart_div = document.getElementById('cart-menu');
    let cart_screen = document.getElementById('cart-screen');
    // cart_div.style.display = 'block';
    cart_div.classList.add('active')
    cart_screen.classList.add('active')
    document.body.style.overflowY = 'hidden';

}

function close_cart() {
    let cart_div = document.getElementById('cart-menu');
    let cart_screen = document.getElementById('cart-screen');
    cart_div.classList.remove('active')
    cart_screen.classList.remove('active')
    document.body.style.overflowY = 'scroll';
}

function show_favourite() {
    let favourite_div = document.getElementById('favourite-menu');
    let favourite_screen = document.getElementById('favourite-screen');
    favourite_div.classList.add('active')
    favourite_screen.classList.add('active')
    document.body.style.overflowY = 'hidden';

}

function close_favourite() {
    let cart_div = document.getElementById('cart-menu');
    let cart_screen = document.getElementById('cart-screen');
    cart_div.classList.remove('active')
    cart_screen.classList.remove('active')
    document.body.style.overflowY = 'scroll';
}