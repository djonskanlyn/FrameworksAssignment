// Define grid options with empty rowData
const gridOptions = {
    rowData: [],
    columnDefs: [
        { field: "idMeal", headerName: "Recipe Id", flex: 0.75 },
        { field: "strMealThumb", headerName: "Image", filter: false,
            cellRenderer: function(params) {
                return `<img src="${params.value}" style="width: 100px; height: 100px; border-radius: 10px;" alt="Meal Image">`;
            }
         },
        { field: "strMeal", headerName: "Recipe Name", flex: 1.5 },
        { field: "strCategory", headerName: "Category" },
        { field: "strArea", headerName: "Region" },
        { field: "strTags", headerName: "Tags",
            cellRenderer: function(params) {
                // Replace commas with semicolons and spaces in the tags string
                if (params.value) { 
                    return params.value.replace(/,/g, '; ');
                }
                return '';
            }
        },
        { field: "allIngredients", headerName: "Ingredients", flex: 2,
            cellRenderer: function(params) {
                 return params.value || '';
            }
        },
        { field: "strYoutube", headerName: "Actions", filter: false, 
            cellRenderer: function(params) {
                // Generate a link to the YouTube video
                let youtubeLink = params.value ? `<a href="${params.value}" target="_blank" class="btn btn-outline-warning btn-sm" style="margin-bottom: 5px;">Youtube</a>` : '';

                // Generate a link to the recipe detail page
                let detailsLink = `<a href="/recipes/our_recipes_detail/${params.data.idMeal}" class="btn btn-outline-primary btn-sm" style="margin-bottom: 5px;">Instructions</a>`;

                // Return both links, styled with some space in between
                return `<div style="display: flex; flex-direction: column;"> ${youtubeLink} ${detailsLink} </div>`;
            }
        },
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

// Function to concatenate ingredients into one field
function getAllIngredients(meal) {
    const ingredients = [];
    for (let i = 1; i <= 20; i++) {
        const ingredient = meal[`strIngredient${i}`];
        if (ingredient) {
            ingredients.push(ingredient);
        }
    }
    return ingredients.join('; ');
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
            strMealThumb: meal.strMealThumb,
            strMeal: meal.strMeal,
            strCategory: meal.strCategory,
            strArea: meal.strArea,
            strTags: meal.strTags,
            strYoutube: meal.strYoutube,
            allIngredients: getAllIngredients(meal),
        }));

        // Set the fetched and formatted data as the new rowData for the grid
        gridApi.setGridOption('rowData', formattedData);
    }).catch(function (error) {
        console.error("Error fetching meal data:", error);
    });
});
