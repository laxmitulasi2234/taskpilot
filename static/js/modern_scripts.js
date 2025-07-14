document.addEventListener('DOMContentLoaded', function () {
    const toggleSwitch = document.getElementById('themeToggleSwitch');
    const root = document.documentElement;

    // Check if toggle exists (avoid JS errors)
    if (!toggleSwitch) return;

    // Load saved theme (default: light)
    const savedTheme = localStorage.getItem('theme') || 'light';
    root.setAttribute('data-theme', savedTheme);
    toggleSwitch.checked = savedTheme === 'dark';

    // When switch is toggled, change theme
    toggleSwitch.addEventListener('change', () => {
        const newTheme = toggleSwitch.checked ? 'dark' : 'light';
        root.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});

