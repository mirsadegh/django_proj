// Frontend JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all wishlist buttons
    document.querySelectorAll('.add-to-wishlist').forEach(button => {
        // Set initial color state
        const icon = button.querySelector('i');
        if (button.classList.contains('active')) {
            icon.style.color = '#E74C3C';
        }

        button.addEventListener('click', handleWishlistClick);
    });
});

function handleWishlistClick(e) {
    e.preventDefault();
    
    const button = this;
    const icon = button.querySelector('i');
    const tooltip = button.querySelector('.tooltipp');
    const url = button.dataset.url;
    
    // Disable button during request to prevent double-clicks
    button.disabled = true;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin' // Important for CSRF
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        updateWishlistUI(button, icon, tooltip, data);
        updateInterestCounts(data.interest_count);
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('مشکلی پیش آمد. لطفا دوباره تلاش کنید.');
    })
    .finally(() => {
        button.disabled = false;
    });
}

function updateWishlistUI(button, icon, tooltip, data) {
    if (data.is_interested) {
        icon.className = 'fa fa-heart text-red';
        button.classList.add('active');
        tooltip.textContent = 'حذف از علاقه مندی';
    } else {
        icon.className = 'fa fa-heart-o';
        button.classList.remove('active');
        tooltip.textContent = 'افزودن به علاقه مندی';
    }
    
    icon.style.color = data.is_interested ? '#E74C3C' : '#666';
}

function updateInterestCounts(count) {
    document.querySelectorAll('.interest-count').forEach(el => {
        el.textContent = count;
    });
}

function showErrorMessage(message) {
    // Create a toast notification
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add CSS for error toast
const style = document.createElement('style');
style.textContent = `
    .error-toast {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #f44336;
        color: white;
        padding: 16px;
        border-radius: 4px;
        z-index: 1000;
    }
`;
document.head.appendChild(style);