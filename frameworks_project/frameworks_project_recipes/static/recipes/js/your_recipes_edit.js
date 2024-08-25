document.addEventListener('DOMContentLoaded', function() {
    const addIngredientBtn = document.getElementById('add-ingredient');
    const ingredientTableBody = document.getElementById('ingredient-tbody');
    let ingredientCount = document.querySelectorAll('#ingredient-tbody tr').length;  // Count the initial number of rows

    // Function to add a new ingredient row
    addIngredientBtn.addEventListener('click', function() {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" name="ingredient-${ingredientCount}" class="form-control" placeholder="Ingredient Name"></td>
            <td><input type="text" name="measure-${ingredientCount}" class="form-control" placeholder="Measure"></td>
            <td><button type="button" class="btn btn-danger delete-ingredient">Delete</button></td>
        `;
        ingredientTableBody.appendChild(newRow);
        ingredientCount++;  // Increment the ingredient counter for the next row
    });

    // Event delegation to handle delete buttons for dynamically created rows
    ingredientTableBody.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-ingredient')) {
            const row = event.target.closest('tr');
            row.remove();  // Remove the row from the table
        }
    });
});
