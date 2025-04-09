// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            // Create a new bootstrap dismiss instance
            const alert = new bootstrap.Alert(message);
            alert.close();
        }, 5000);
    });
    
    // Add timestamp to quick post form
    const quickPostForm = document.querySelector('.card form[action*="new_post"]');
    if (quickPostForm) {
        quickPostForm.addEventListener('submit', function(event) {
            // For now, we're just adding form validation
            const textarea = this.querySelector('textarea');
            if (!textarea.value.trim()) {
                event.preventDefault();
                alert('Please enter some content before posting.');
            }
        });
    }
    
    // Add confirm dialog to delete buttons that don't already have it
    const deleteButtons = document.querySelectorAll('form[action*="delete"] button[type="submit"]');
    deleteButtons.forEach(function(button) {
        const form = button.closest('form');
        if (!form.hasAttribute('onsubmit')) {
            form.onsubmit = function() {
                return confirm('Are you sure you want to delete this?');
            };
        }
    });
    
    // Add like functionality animations
    const likeButtons = document.querySelectorAll('form[action*="like"] button');
    likeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Add a brief animation when clicking like
            this.classList.add('btn-animate');
            setTimeout(() => {
                this.classList.remove('btn-animate');
            }, 300);
        });
    });
    
    // Add responsive table functionality
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        if (!table.parentElement.classList.contains('table-responsive')) {
            // If table is not already in a responsive wrapper, add the class to its parent
            const parent = table.parentElement;
            if (parent && !parent.classList.contains('table-responsive')) {
                parent.classList.add('table-responsive');
            }
        }
    });
});

// Add custom filter for newlines in content
function nl2br(str) {
    if (typeof str === 'string') {
        return str.replace(/\n/g, '<br>');
    }
    return str;
}
