// Define grid options with updated column definitions
const gridOptions = {
    rowData: [],  // Initial empty data
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
    ],
    pagination: true,
    paginationPageSize: 5,
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

// Fetch saved recipes from the database and update the grid
document.addEventListener('DOMContentLoaded', function () {
    const eDiv = document.querySelector('#your_recipes_grid');
    const gridApi = agGrid.createGrid(eDiv, gridOptions);

    // Fetch data from the API
    fetch('/recipes/your-recipes-data/')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);
            gridApi.setGridOption('rowData', data);
        })
        .catch(error => console.error('Error fetching recipes:', error));
});