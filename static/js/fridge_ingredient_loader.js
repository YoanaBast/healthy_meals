function loadUnits() {
    const select = document.getElementById('ingredientSelect');
    const unitSelect = document.getElementById('unitSelect');

    // Clear completely
    unitSelect.innerHTML = '';
    unitSelect.value = '';

    const selectedOption = select.options[select.selectedIndex];
    if (!selectedOption || !selectedOption.value) return;

    const unitsData = selectedOption.getAttribute('data-units');

    if (!unitsData) return;

    const units = JSON.parse(unitsData);

    units.forEach((u, index) => {
        const opt = document.createElement('option');
        opt.value = u.id;
        opt.textContent = u.name;
        unitSelect.appendChild(opt);
    });

    // Force first unit selected
    if (unitSelect.options.length > 0) {
        unitSelect.selectedIndex = 0;
    }

    console.log("Units loaded:", units);
    console.log("Selected unit:", unitSelect.value);
}

function closeModal() {
    const modal = document.getElementById('addFridgeItemModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

