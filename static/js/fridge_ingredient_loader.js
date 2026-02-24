document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('addFridgeItemModal');
    const openBtn = document.getElementById('openAddFridgeModal');
    const form = document.getElementById('addFridgeItemForm');

    // Open modal
    openBtn.addEventListener('click', function(e) {
        e.preventDefault(); // stop navigation
        modal.style.display = 'block';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Close modal on Cancel button
    const cancelBtn = modal.querySelector('button.btn-secondary');
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Handle form submission without refreshing
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // stop page refresh

        const qty = parseFloat(document.getElementById('quantityInput').value);
        const EPSILON = 0.001;

        console.log('Entered quantity:', qty);

        if (!qty || qty <= 0 || qty < EPSILON) {
            console.log('Quantity failed the check');
            alert('Quantity must be greater than 0.');
        } else {
            console.log('Quantity passed the check');
            modal.style.display = 'none';

            // Optional: send data via fetch/ajax instead of normal submit
            // fetch(form.action, { method: 'POST', body: new FormData(form) })
        }
    });
});