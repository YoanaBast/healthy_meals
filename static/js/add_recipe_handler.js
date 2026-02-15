document.addEventListener("DOMContentLoaded", function () {

    const prefix = "recipe_ingredient";

    const totalFormsInput = document.querySelector(
        `[name="${prefix}-TOTAL_FORMS"]`
    );

    if (!totalFormsInput) {
        console.error("Management form not found");
        return;
    }

    let formIndex = parseInt(totalFormsInput.value);

    const addBtn = document.getElementById("addIngredientBtn");
    const modal = document.getElementById("ingredientModal");

    addBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    window.closeModal = function () {
        modal.style.display = "none";
    };

    window.loadUnits = function () {
        const ingredientSelect = document.getElementById("ingredientSelect");
        const unitSelect = document.getElementById("unitSelect");

        unitSelect.innerHTML = "";

        const selectedOption =
            ingredientSelect.options[ingredientSelect.selectedIndex];

        if (!selectedOption?.dataset.units) return;

        const units = JSON.parse(selectedOption.dataset.units);

        units.forEach(u => {
            const option = document.createElement("option");
            option.value = u.id;
            option.text = u.name;
            unitSelect.add(option);
        });
    };

    window.addIngredient = function () {

        const ingredientSelect = document.getElementById("ingredientSelect");
        const ingredient = ingredientSelect.value;
        const ingredientText =
            ingredientSelect.options[ingredientSelect.selectedIndex]?.text;

        const quantity = parseFloat(
            document.getElementById("quantityInput").value
        );

        const unitSelect = document.getElementById("unitSelect");
        const unit = unitSelect.value;
        const unitText =
            unitSelect.options[unitSelect.selectedIndex]?.text;

        if (!ingredient || !unit || !quantity || quantity <= 0) {
            alert("Invalid values");
            return;
        }

        const container =
            document.getElementById("ingredientsContainer");

        container.insertAdjacentHTML("beforeend", `
            <div class="ingredient-item">
                <input type="hidden"
                    name="${prefix}-${formIndex}-ingredient"
                    value="${ingredient}">
                <input type="hidden"
                    name="${prefix}-${formIndex}-quantity"
                    value="${quantity}">
                <input type="hidden"
                    name="${prefix}-${formIndex}-unit"
                    value="${unit}">
                <p><strong>${ingredientText}</strong> - ${quantity} ${unitText}</p>
            </div>
        `);

        formIndex++;
        totalFormsInput.value = formIndex;

        document.getElementById("quantityInput").value = "";
        document.getElementById("unitSelect").innerHTML = "";

        modal.style.display = "none";
    };

});
