let previousConversion = parseFloat(
    document.getElementById('unitSelect').selectedOptions[0].dataset.conversion
);

function convertQuantity(select) {
    const newConversion = parseFloat(select.selectedOptions[0].dataset.conversion);
    const quantityInput = document.getElementById('quantityInput');
    const currentQty = parseFloat(quantityInput.value);

    if (!isNaN(currentQty) && previousConversion && newConversion) {
        // convert to base, then to new unit
        const inBase = currentQty * previousConversion;
        const converted = inBase / newConversion;
        // round to 2 decimals and format as string with 2 decimal places
        quantityInput.value = (converted).toFixed(2);
    }

    previousConversion = newConversion;
}