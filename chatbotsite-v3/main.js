document.addEventListener('DOMContentLoaded', function () {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(element => {
        observer.observe(element);
    });

    // Navbar scroll effect
    window.addEventListener('scroll', function () {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(14, 17, 23, 0.9)';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'var(--background-color)';
            navbar.style.boxShadow = 'none';
        }
    });
});


window.addEventListener('scroll', function () {
    var navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('shadow');
    } else {
        navbar.classList.remove('shadow');
    }
});
