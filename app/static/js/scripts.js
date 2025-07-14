document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ TaskPilot ready!");

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            alert("✈️ Task added successfully!");
        });
    }
});
// app/static/js/scripts.js
