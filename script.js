document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();

    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const root = document.documentElement;

    themeToggle.addEventListener('click', () => {
        const currentTheme = root.getAttribute('data-theme');
        
        if (currentTheme === 'light') {
            root.removeAttribute('data-theme');
            updateIcon('moon');
        } else {
            root.setAttribute('data-theme', 'light');
            updateIcon('sun');
        }
    });

    function updateIcon(iconName) {
        // Reemplaza el contenido del icono y vuelve a llamar a lucide
        themeToggle.innerHTML = `<i data-lucide="${iconName}" id="theme-icon"></i>`;
        lucide.createIcons();
    }

    // Efecto de brillo interactivo en tarjetas
    document.querySelectorAll('.glass-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(0, 112, 243, 0.1) 0%, var(--glass-bg) 70%)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.background = 'var(--glass-bg)';
        });
    });
});
