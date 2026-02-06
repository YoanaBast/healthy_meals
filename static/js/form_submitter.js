document.getElementById('ingredient-form').addEventListener('submit', function (e) {
    e.preventDefault(); // stop redirect

    const form = this;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // close modal
            window.location.hash = '';

            // OPTIONAL: simplest update → reload page
            location.reload();
        } else {
            console.log(data.errors);
        }
    });
});
