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