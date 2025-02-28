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

            // Get elements
            const addressDisplay = document.getElementById('address-display');
            const changeButton = document.getElementById('change-button');
            const saveButton = document.getElementById('save-button');
            
            // Enable editing when "Change" button is clicked
            changeButton.addEventListener('click', () => {
                addressDisplay.removeAttribute('readonly');
                addressDisplay.focus();
                changeButton.style.display = 'none';
                saveButton.style.display = 'inline-block';
            });
        
            // Save the address and disable editing when "Save" button is clicked
            saveButton.addEventListener('click', () => {
                const updatedAddress = addressDisplay.value;
                console.log("Updated Address: ", updatedAddress);
                addressDisplay.setAttribute('readonly', 'readonly');
                changeButton.style.display = 'inline-block';
                saveButton.style.display = 'none';
            });
            document.addEventListener("DOMContentLoaded", function () {
                const placeOrderBtn = document.querySelector(".checkout-button");  // Selecting by class
                if (placeOrderBtn) {
                    placeOrderBtn.addEventListener("click", function () {
                        placeOrder();
                    });
                }
            
                const placeSingleOrderBtn = document.getElementById("place-single-order-btn");
                if (placeSingleOrderBtn) {
                    placeSingleOrderBtn.addEventListener("click", function () {
                        const productId = this.getAttribute("data-product-id");
                        placeOrder(productId);
                    });
                }
            });
            
            function getCSRFToken() {
                return document.querySelector("input[name='csrfmiddlewaretoken']").value;
            }
            
            document.addEventListener("DOMContentLoaded", function () {
                console.log("Script Loaded!");
            
                function placeOrder(productId = null) {
                    console.log("placeOrder() function called!");
            
                    const address = document.getElementById("address-input")?.value;
                    const paymentMode = document.querySelector("input[name='payment']:checked")?.value;
            
                    if (!address || !paymentMode) {
                        console.log("Missing address or payment mode");
                        return;
                    }
            
                    let bodyData = new FormData();
                    bodyData.append("address", address);
                    bodyData.append("payment_mode", paymentMode);
            
                    if (productId) {
                        bodyData.append("product_id", productId);
                    }
            
                    fetch("/place_order/", {
                        method: "POST",  // ✅ Ensure the request is POST
                        headers: {
                            "X-CSRFToken": getCSRFToken(),  // ✅ Include CSRF token for security
                        },
                        body: bodyData,
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("Response:", data);
                        if (data.success) {
                            alert("Order placed successfully!");
                            window.location.href = "/place_order/";
                        } else {
                            alert("Error: " + data.message);
                        }
                    })
                    .catch(error => console.error("Error:", error));
                }
            
                function getCSRFToken() {
                    return document.querySelector("input[name='csrfmiddlewaretoken']").value;
                }
            
                const orderButton = document.getElementById("place-order-btn");
                if (orderButton) {
                    orderButton.addEventListener("click", function () {
                        placeOrder();
                    });
                }
            });
            