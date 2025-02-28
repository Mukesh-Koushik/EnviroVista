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
                addressDisplay.setAttribute('readonly', 'readonly');
                changeButton.style.display = 'inline-block';
                saveButton.style.display = 'none';
            });