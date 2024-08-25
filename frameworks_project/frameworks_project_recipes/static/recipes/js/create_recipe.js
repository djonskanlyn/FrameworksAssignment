document.addEventListener('DOMContentLoaded', function () {
    let rowCounter = 1;  // Start counting from 1 because the initial row is 0

    // Add a new row to the ingredients table
    document.getElementById('add-ingredient-btn').addEventListener('click', function() {
        const tbody = document.getElementById('ingredient-tbody');

        // Create a new row
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" name="ingredient-${rowCounter}" placeholder="Ingredient" class="form-control"></td>
            <td><input type="text" name="measure-${rowCounter}" placeholder="Measure" class="form-control"></td>
            <td><button type="button" class="btn btn-danger delete-ingredient">Delete</button></td>
        `;

        // Append the new row to the table
        tbody.appendChild(newRow);

        // Increment the row counter for unique name attributes
        rowCounter++;

        // Add event listener to the delete button of the new row
        newRow.querySelector('.delete-ingredient').addEventListener('click', function() {
            newRow.remove();
        });
    });

    // Handle deleting the initial ingredient row
    document.querySelectorAll('.delete-ingredient').forEach(button => {
        button.addEventListener('click', function() {
            button.closest('tr').remove();
        });
    });
});
