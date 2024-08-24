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
                return `<div style="display: flex; flex-direction: column;"> ${youtubeLink} </div>`;
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