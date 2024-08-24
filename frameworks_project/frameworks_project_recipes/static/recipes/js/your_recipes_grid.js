// Define the grid
const gridOptions = {
    rowData: [],
    columnDefs: [
        { field: "id", headerName: "Id", flex: 0.5},
        { field: "image", headerName: "Image", filter: false,
            cellRenderer: function(params) {
                if (params.value) {
                    return `<img src="${params.value}" style="width: 100px; height: 100px; border-radius: 10px;" alt="Recipe Image">`;
                }
                return "No Image";
            }
        },
        { field: "recipe", headerName: "Recipe Name", flex: 1.5 },
        { field: "category", headerName: "Category" },
        { field: "region", headerName: "Region" },
        { field: "ingredients_data", headerName: "Ingredients", flex: 2,
            cellRenderer: function(params) {
                 return params.value || '';
            }
        },
        { field: "youtube", headerName: "Actions", filter: false, 
            cellRenderer: function(params) {
                let youtubeLink = params.value ? `<a href="${params.value}" target="_blank" class="btn btn-outline-warning btn-sm" style="margin-bottom: 5px;">Youtube</a>` : '';

                let deleteButton = `<button class="btn btn-outline-danger btn-sm" style="margin-bottom: 5px;" onclick="deleteRecipe(${params.data.id})">Delete</button>`;

                let detailsLink = `<a href="/recipes/user-recipe-detail/${params.data.id}/" class="btn btn-outline-primary btn-sm" style="margin-bottom: 5px;">Instructions</a>`;

                return `<div style="display: flex; flex-direction: column;"> ${youtubeLink} ${deleteButton} ${detailsLink} </div>`;
            }
        },
    ],
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [5,10,20,50,100,200],
    defaultColDef: {
        flex: 1,
        filter: true,
        sortable: true,
        floatingFilter: true,
        resizable: true,
        wrapText: true,
        autoHeight: true,
        cellStyle: { display: 'flex', alignItems: 'center' }
    }
};

// Fetch data and populate grid
document.addEventListener('DOMContentLoaded', function () {
    const eDiv = document.querySelector('#your_recipes_grid');
    const gridApi = agGrid.createGrid(eDiv, gridOptions);

    fetch('/recipes/your-recipes-data/')
        .then(response => response.json())
        .then(data => {
            gridApi.setGridOption('rowData', data);
        })
        .catch(error => console.error('Error fetching recipes:', error));
});

// Function to delete a recipe
function deleteRecipe(recipeId) {
    if (!confirm('Are you sure you want to delete this recipe?')) {
        return;
    }

    fetch(`/recipes/delete-recipe/${recipeId}/`, {
        method: 'POST',  // Use POST instead of DELETE to trigger Django's form handling
        headers: {
            'X-CSRFToken': getCSRFToken(),  // Include CSRF token for security
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.redirected) {
            // If there's a redirect (after successful deletion), follow it
            window.location.href = response.url;
        } else {
            alert('Failed to delete recipe');
        }
    })
    .catch(error => console.error('Error deleting recipe:', error));
}

// Simplified function to get CSRF token
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}