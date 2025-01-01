// Show sidebar
function showsidebar() {
    document.querySelector('.sidebar').classList.toggle('show'); // Toggle the 'show' class for animation
}

// Hide sidebar
function hidebar() {
    document.querySelector('.sidebar').classList.remove('show');
}
// Close sidebar if clicked outside
document.addEventListener('click', function(event) {
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menubtn');
    if (!event.target.closest('.sidebar') && !event.target.closest('.menubtn')) {
        sidebar.classList.remove('show');
    }
});

document.querySelector('.cart-toggle').addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelector('.cart-container').classList.add('show');
});

// Close the cart when clicking the close button
document.querySelector('.close-cart').addEventListener('click', () => {
    document.querySelector('.cart-container').classList.remove('show');
});

// Show and hide the orders
document.querySelector('.orders-toggle').addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelector('.orders-container').classList.add('show');
});

// Close the orders when clicking the close button
document.querySelector('.close-orders').addEventListener('click', () => {
    document.querySelector('.orders-container').classList.remove('show');
});

const slides = document.querySelector('.slides');
const slide = document.querySelectorAll('.slide');
const prev = document.querySelector('.prev');
const next = document.querySelector('.next');

let currentIndex = 0;

function updateSlider() {
    slides.style.transform = `translateX(-${currentIndex*100}%)`;
}

prev.addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : slide.length - 1;
    updateSlider();
});

next.addEventListener('click', () => {
    currentIndex = (currentIndex < slide.length - 1) ? currentIndex + 1 : 0;
    updateSlider();
});
setInterval(() => {
currentIndex = (currentIndex < slide.length - 1) ? currentIndex + 1 : 0;
updateSlider();
    }, 3000);


let cart = [];

const cartToggle = document.querySelector('.cart-toggle');
const cartContainer = document.querySelector('.cart-container');
const closeCartButton = document.querySelector('.close-cart');
const ordersToggle = document.querySelector('.orders-toggle');
const ordersContainer = document.querySelector('.orders-container');
const closeOrdersButton = document.querySelector('.close-orders');

cartToggle.addEventListener('click', () => {
cartContainer.style.display = cartContainer.style.display === 'none' || !cartContainer.style.display ? 'block' : 'none';
});

closeCartButton.addEventListener('click', () => {
cartContainer.style.display = 'none';
});

ordersToggle.addEventListener('click', () => {
ordersContainer.style.display = ordersContainer.style.display === 'none' || !ordersContainer.style.display ? 'block' : 'none';
});

closeOrdersButton.addEventListener('click', () => {
ordersContainer.style.display = 'none';
});

// Add to cart functionality
document.querySelectorAll('.add-to-cart').forEach(button => {
button.addEventListener('click', (event) => {
    const productCard = event.target.closest('.product-card');
    const productId = productCard.getAttribute('data-id');
    const productName = productCard.querySelector('h3').textContent;
    const productPrice = productCard.querySelector('.price').textContent;
    const productImage = productCard.querySelector('img').src;

    const existingProduct = cart.find(item => item.id === productId);

    if (existingProduct) {
    existingProduct.quantity += 1;
    } else {
    cart.push({
        id: productId,
        name: productName,
        price: productPrice,
        image: productImage,
        quantity: 1
    });
    }

    updateCartDisplay();
    updateOrdersDisplay();
});
});

function updateCartDisplay() {
const cartItemsContainer = document.querySelector('.cart-items');
cartItemsContainer.innerHTML = '';

cart.forEach(item => {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart-item');
    cartItem.innerHTML = `
    <img src="${item.image}" alt="${item.name}">
    <div>
        <h4>${item.name}</h4>
        <p>Price: ${item.price}</p>
        <p>Quantity: ${item.quantity}</p>
        <button class="remove-item">Remove</button>
    </div>
    `;
    cartItemsContainer.appendChild(cartItem);
    cartItem.querySelector(".remove-item").addEventListener("click", function () {
        const index = cart.indexOf(item);
        if (index > -1) {
            cart.splice(index, 1);
            updateCartDisplay();
        }
    });
});
}

function updateOrdersDisplay() {
const orderList = document.getElementById('order-list'); // Select the order list
orderList.innerHTML = '';

cart.forEach(item => {
    const orderItem = document.createElement('li');
    orderItem.innerHTML = `
    <img src="${item.image}" alt="${item.name}">
    <div>
    <h4>${item.name}</h4>
    <p>Price: ${item.price}</p>
    <p>Quantity: ${item.quantity}</p>
    </div>
    `;
    orderList.appendChild(orderItem);
});
}

document.addEventListener('touchstart', function(event) {
    event.preventDefault();
}, false);

document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    const toast = document.getElementById("toast");

    addToCartButtons.forEach(button => {
      button.addEventListener("click", () => {
        // Show the toast
        toast.classList.add("show");
        
        // Hide the toast after 3 seconds
        setTimeout(() => {
          toast.classList.remove("show");
        }, 3000);
      });
    });
  });