document.querySelectorAll('.form-input').forEach(input => {
    // store initial value if needed
    const initial = input.value;

    input.addEventListener('focus', () => {
        if (input.value == '0') input.value = '';
    });

    input.addEventListener('blur', () => {
        if (input.value === '') input.value = initial; // restores 0
    });
});