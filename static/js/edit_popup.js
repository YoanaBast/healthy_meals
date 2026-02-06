function openEditModal(id) {
    fetch(`/ingredients/${id}/edit-popup/`)  // URL mapped to edit_ingredient_popup
        .then(res => res.text())
        .then(html => {
            const div = document.createElement('div');
            div.innerHTML = html;
            document.body.appendChild(div); // append modal to body
            const modal = div.querySelector('.modal-overlay');
            modal.style.display = 'flex';

            // attach AJAX submit handler
            const form = modal.querySelector('form');
            form.addEventListener('submit', function(e){
                e.preventDefault();
                const formData = new FormData(this);
                fetch(this.action, { method:'POST', body: formData, headers:{'X-Requested-With':'XMLHttpRequest'}})
                    .then(r=>r.json())
                    .then(data => {
                        if(data.success) location.reload();
                        else console.log(data.errors);
                    });
            });
        });
}

