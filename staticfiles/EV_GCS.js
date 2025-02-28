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
fetchCartData();

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

function fetchCartData() {
    // const viewcarturl = this.dataset.url;
    // const viewcarturl = e.currentTarget.getAttribute('data-url');
    // const viewcarturl = document.querySelector('.cart-toggle').dataset.url || '/viewcart/';
    console.log(viewcarturl);
    console.log("demo");
    fetch(viewcarturl)
        .then(response => response.json())
        .then(data => {
            cart = data.cart; // Update the global cart
            console.log('Cart Data:', data.cart);  // Log the response
            updateCartDisplay(cart); // Refresh the cart UI
        })
        .catch(error => console.error('Error fetching cart:', error));    
}

// Add to cart functionality
document.querySelectorAll('.add-to-cart').forEach(button => {
button.addEventListener('click', (event) => {
    const productCard = event.target.closest('.product-card');
    const productId = productCard.getAttribute('data-id');
    const productName = productCard.querySelector('h3').textContent;
    const productPrice = productCard.querySelector('.price').textContent;
    const productImage = productCard.querySelector('img').src;

    //const existingProduct = cart.find(item => item.id === productId);

    /*if (existingProduct) {
    existingProduct.quantity += 1;
    } else {
    cart.push({
        id: productId,
        name: productName,
        price: productPrice,
        image: productImage,
        quantity: 1
    });
    }*/
	
	
	const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    console.log('CSRF Token:', csrfToken);
		
	// Get URL and productId directly from the clicked button
        const addToCartUrl = button.dataset.url;
        const productId1 = button.dataset.productId;

        fetch(addToCartUrl, {
            method: 'POST',
            body: JSON.stringify({ product_id: productId1 }),
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => console.log('Response from backend:', data))
        .catch(error => console.error('Error:', error));

        // Debug: Check the updated cart value
        console.log('Cart after adding:', cart);


    updateCartDisplay();
    updateOrdersDisplay(cart);
});
});

/*function updateCartDisplay() {
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
}*/

function updateCartDisplay(cart) {
    const cartItemsContainer = document.querySelector('.cart-items'); // Container to display cart items
    cartItemsContainer.innerHTML = ''; // Clear previous cart items

    // Loop through cart object
    Object.entries(cart).forEach(([productId, quantity]) => {
        // Find the product card in the HTML using the data-id attribute
        const productCard = document.querySelector(`.product-card[data-id="${productId}"]`);

        if (productCard) {
            // Extract product details from the product card
            const name = productCard.querySelector('.product-details h3').textContent;
            const price = productCard.querySelector('.product-details .price').textContent;
            const image = productCard.querySelector('.product-image img').src;

            // Create a cart item div dynamically
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
                <div class="left-container">
            <img src="${image}" alt="${name}">
            <div class="quantity-controls">
                <button class="decrease-button" data-product-id="${productId}">-</button>
                <span class="product-quantity">${quantity}</span>
                <button class="increase-button" data-product-id="${productId}">+</button>
            </div>
        </div>
        <div class="right-container">
        <h4>${name}</h4>
        <p>Price: ${price}</p>
            <button class="remove-item">Remove</button>
        </div>
            `;
            // Append the cart item to the container
            cartItemsContainer.appendChild(cartItem);

            // Add event listener for "Remove" button
            cartItem.querySelector(".remove-item").addEventListener("click", function () {
                delete cart[productId]; // Remove the item from the cart object
                updateCartDisplay(cart); // Refresh the cart display
            });
        } else {
            console.error(`Product with ID ${productId} not found in the HTML.`);
        }
    });
}

/*function updateCartDisplay(cart) {
    const cartItemsContainer = document.querySelector('.cart-items');
    cartItemsContainer.innerHTML = '';

    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
        <div class="left-container">
            <img src="${item.image}" alt="${item.name}">
            <div class="quantity-controls">
                <button class="decrease-button" data-product-id="${item.id}">-</button>
                <span class="product-quantity">${item.quantity}</span>
                <button class="increase-button" data-product-id="${item.id}">+</button>
            </div>
        </div>
        <div class="right-container">
            <h4>${item.name}</h4>
            <p>Price: ${item.price}</p>
            <button class="remove-item">Remove</button>
        </div>
        `;

        // Append the cart item to the container
        cartItemsContainer.appendChild(cartItem);

        // Add event listener for the remove button
        cartItem.querySelector(".remove-item").addEventListener("click", function () {
            const index = cart.indexOf(item);
            if (index > -1) {
                cart.splice(index, 1);
                updateCartDisplay();
            }
        });

        // Add event listener for the decrease button
        cartItem.querySelector(".decrease-button").addEventListener("click", function () {
            if (item.quantity > 1) {
                item.quantity -= 1;
                updateCartDisplay();
            } else {
                alert('Quantity cannot be less than 1');
            }
        });

        // Add event listener for the increase button
        cartItem.querySelector(".increase-button").addEventListener("click", function () {
            item.quantity += 1;
            updateCartDisplay();
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
}*/

// function updateCartDisplay(cart, totalPrice) {
//     const cartItemsContainer = document.querySelector('.cart-items');
//     cartItemsContainer.innerHTML = '';  // Clear previous cart items

//     Object.entries(cart).forEach(([productId, quantity]) => {
//         const productCard = document.querySelector(`.product-card[data-id="${productId}"]`);

//         if (productCard) {
//             const name = productCard.querySelector('.product-details h3').textContent;
//             const price = parseFloat(productCard.querySelector('.product-details .price').textContent.replace('₹', ''));
//             const image = productCard.querySelector('.product-image img').src;

//             const cartItem = document.createElement('div');
//             cartItem.classList.add('cart-item');
//             cartItem.innerHTML = `
//                 <img src="${image}" alt="${name}">
//                 <div>
//                     <h4>${name}</h4>
//                     <p>Price: ₹${price}</p>
//                     <p>Quantity: ${quantity}</p>
//                     <button class="remove-item" data-id="${productId}">Remove</button>
//                 </div>
//             `;

//             cartItemsContainer.appendChild(cartItem);
//         }
//     });

//     // Update total price display
//     document.querySelector(".total-price").textContent = `Total Price: ₹${totalPrice.toFixed(2)}`;
// }


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