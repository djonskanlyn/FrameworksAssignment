// Define grid options with empty rowData
const gridOptions = {
    rowData: [],  // Initially empty, data will be fetched and set later
    columnDefs: [
        { field: "idMeal", headerName: "Recipe Id" },
        { field: "strMeal", headerName: "Recipe Name" },
        { field: "strCategory", headerName: "Category" },
        { field: "strArea", headerName: "Region" },
        { field: "strTags", headerName: "Tags" },
        { field: "strYoutube", headerName: "Youtube Link" },
    ],
    pagination: true,
    paginationPageSize: 50,
    paginationPageSizeSelector: [10,20,50,100],
    defaultColDef: {
        flex: 1,
        filter: true,
        sortable: true,
        floatingFilter: true
    }
};

// Array of letters (A-Z) to search recipes by
const letters = 'abcdefghijklmnopqrstuvwxyz'.split('');

// Function to fetch meals for a given letter
function fetchRecipesByLetter(letter) {
    return fetch(`https://www.themealdb.com/api/json/v1/1/search.php?s=${letter}`)
        .then(response => response.json())
        .then(data => data.meals || []);  // Return meals or an empty array if no results
}

// Function to remove duplicate recipes based on idMeal
function removeDuplicates(meals) {
    const uniqueMeals = [];
    const mealIds = new Set();

    meals.forEach(meal => {
        if (!mealIds.has(meal.idMeal)) {
            mealIds.add(meal.idMeal);
            uniqueMeals.push(meal);
        }
    });

    return uniqueMeals;
}

// Function to fetch all recipes starting with each letter
function fetchAllRecipes() {
    return Promise.all(letters.map(fetchRecipesByLetter))
        .then(allResponses => allResponses.flat())  // Flatten the array of arrays into one array
        .then(removeDuplicates);  // Remove duplicate recipes
}

document.addEventListener('DOMContentLoaded', function () {
    const eDiv = document.querySelector('#our_recipes_grid');
    
    // Create the grid with initial gridOptions
    const gridApi = agGrid.createGrid(eDiv, gridOptions);

    // Fetch all recipes by iterating over the alphabet
    fetchAllRecipes().then(allRecipes => {
        // Prepare the rowData in the format required by the grid
        const formattedData = allRecipes.map(meal => ({
            idMeal: meal.idMeal,
            strMeal: meal.strMeal,
            strCategory: meal.strCategory,
            strArea: meal.strArea,
            strTags: meal.strTags,
            strYoutube: meal.strYoutube
        }));

        // Set the fetched and formatted data as the new rowData for the grid
        gridApi.setGridOption('rowData', formattedData);
    }).catch(function (error) {
        console.error("Error fetching meal data:", error);
    });
});
