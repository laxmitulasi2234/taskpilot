// Show Toast Function
function showToast(message, category = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${category} border-0 show mb-2`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Auto remove toast after 5 sec
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Add loading spinner on submit
document.getElementById('taskForm')?.addEventListener('submit', function () {
    const submitBtn = this.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding...';

    setTimeout(() => {
        this.reset();
        submitBtn.disabled = false;
        submitBtn.innerHTML = '➕ Add Task';
    }, 1000); // fallback to reset UI
});
