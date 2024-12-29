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