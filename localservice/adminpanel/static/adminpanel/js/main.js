// main.js
function confirmDelete() {
  return confirm("Are you sure you want to delete this item? This action cannot be undone.");
}
// Animate dashboard cards on load
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".stat-card");
    cards.forEach((card, index) => {
        card.style.opacity = 0;
        setTimeout(() => {
            card.style.transition = "opacity 0.6s ease";
            card.style.opacity = 1;
        }, index * 150);
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const bgImages = [
        "/static/adminpanel/images/bg1.jpg",
        "/static/adminpanel/images/bg2.jpg",
        "/static/adminpanel/images/bg3.jpg",
        "/static/adminpanel/images/bg4.jpg"
    ];

    let current = 0;
    const body = document.querySelector(".login-slideshow");

    function changeBackground() {
        body.style.backgroundImage = `url(${bgImages[current]})`;
        current = (current + 1) % bgImages.length;
    }

    // Set initial background and start changing every 5s
    changeBackground();
    setInterval(changeBackground, 5000);
});
// main.js
const slideshow = document.querySelector('.login-slideshow');

// Get image list from data attribute
const images = JSON.parse(slideshow.getAttribute('data-images'));

let index = 0;

// Function to change background
function changeBackground() {
    slideshow.style.backgroundImage = `url('${images[index]}')`;
    index = (index + 1) % images.length;
}

// Initial background
changeBackground();

// Change every 5 seconds
setInterval(changeBackground, 5000);
