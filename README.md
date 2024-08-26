# Readme

The link to the website can be found here: [frameworks project website](https://frameworksassignment.onrender.com).

The link to the github for the project can be found here: [frameworks project github](https://github.com/djonskanlyn/FrameworksAssignment).

There is a file with the relevant environment variables (names and values); and some usernames abd passwords for existing profiles included in the zip file uploaded with the assignment submission (it is not included in the github repository.) This is only provided for use by the person who is grading the assignment.

This website is built using the django framework. If the user is logged in as a superuser they can acess the [admin section](https://frameworksassignment.onrender.com/admin/login/?next=/admin/). 

The project has four apps:
* main app: frameworks_project
* users app: frameworks_project_users (facilitates the user profile)
* blog app: frameworks_project_blog (facilitates the blog functionality)
* recipes app: frameworks_project_recipes (facilitates the viewing recipes and details to our connected api; and storage, edit and creations of user recipes.)

## Project features:
* User registration;
* Profile update, including profile image uploads (stored using AWS S3);
* Password reset for users though email (via gmail app);
* Blog for registered users to post culinary related posts;
* Recipes (Our Recipes) supplied by connection to API: (www.themealdb.com);
* Facility to users to view our list of receipes, view the details including instructions and ingredients, and if they choose, to save it to their private user recipes.
* From their user recipes can be edited, faciliitating changes to iamge, yotube video, instructions and ingredients.
* Users can also create their own recipes from scratch and store them in their recipes list.
* Uploaded recipe images are stored on AWS S3, youtube video links are verified using the  youtube google cloud api.
* The Recipes list (both from the mealdb api and the users) are provided using [AG Grid](https://www.ag-grid.com).

The general page structure is consistent across the website with a nav bar and side section with links to the key sections not listed in the nav bar. The side section is only removed for the pages that list recipes [Our Recipes](https://frameworksassignment.onrender.com/recipes/our_recipes) and [Your Recipes](https://frameworksassignment.onrender.com/recipes/your_recipes/). The links for those two pages were added to the navbar.

## Home Page / Our Blog
The [home page](https://frameworksassignment.onrender.com) is the blog page. All blogs are visible whether the user is logged in or not. Clicking on the author link will bring you to a list of all posts from that author. Users can login or register as a user to be able to login from this page.

## About Page
The [about page](https://frameworksassignment.onrender.com/about/) gives details about the blog website in general it can be accessed whether someone is logged in or not.

## Login Page
The [login page](https://frameworksassignment.onrender.com/login/) allows users to login or allows users to request a password reset. To reset their password theuser enters their e-mail and if the e-mail is linked to a user profile an email will be sent to that address to facilitate reseeting their password. There is also a link so they can register for an account if they don't have one.

## Register Page
The [register page](https://frameworksassignment.onrender.com/register/) allows users to register as a user. They can then add blog posts, edit their own posts, view our recipes and add to their own recipes.

## New Post Page
The [new post page](https://frameworksassignment.onrender.com/post/new/) allows logged on users to make a new post to the blog.

## Profile Page
The [profile page](https://frameworksassignment.onrender.com/profile/) allows logged on users to update their profile. They can update allaspects of their profile including profile pic, username, email, first name, last name. All images are uploaded to AWS S3 cloud storage.

## Our Recipes Page
The [Our Recipes Page](https://frameworksassignment.onrender.com/recipes/our_recipes) can be accessed from the side section. It is only accessible by users who are logged in. It calls an api at www.themealdb.com. There are approximately 200 recipes in this api and through the use of AG Grid via javascript the recipes are rendered in a grid that is highly manipulable (including reorganising the positions of fields) and provides excellent filtering functionality. There is an actions field that has two buttons; one that takes you to a youtube video (if available) for the recipe. The second button (instructions) brings you to another page that gives the user the full details of the recipe, including instructions, ingredients and measures.

## Our Recipes: Instruction (Our Recipes Detail)
The [Dur Recipes Detail Page](https://frameworksassignment.onrender.com/recipes/our_recipes_detail/52844) (example provided for Lasagne) Shows the details for one recipe and gives extra details such as recipe instructions, listed ingredient and measures and the urls for the image and youtube video. There are three buttons under the image that bring you to the youtube video, bring you back to the list of recipes, and the third button allows you to save the recipe to your recipes. This is facilitated via a posgresql database. You can only save recipes from the detail view, you can't save them from the list view. You can't delete a recipe from Our Receipes.

## Your Recipes Page
The [Your Recipes Page](https://frameworksassignment.onrender.com/recipes/your_recipes/) can be accessed from the side section. It is only accessible by users who are logged in. It dsiplays all recipes the suer has saved to the postgres database through the use of AG Grid via javascript. There is an actions field that has three buttons; one that takes you to a youtube video (if available) for the recipe. The second botton allows the user to delete a recipe from thir list. The third button (instructions) brings you to another page that gives the user the full details of the recipe, including instructions, ingredients and measures, they can edit the recipe in the detail view. There is also a create recipe button at the top of the page that allows the user create a recipe from scratch.

## Your Recipes: Instruction (Our Recipes Detail)
The Your Recipes Detail Page shows the details for one recipe and gives extra details such as recipe instructions, listed ingredient and measures and the urls for the image and youtube video. There are four buttons under the image that bring you to the youtube video, delete the recipe, bring you back to the list of recipes, and the fourth button allows you to edit. This is facilitated via a posgresql databasen and another view. You can only edit recipes from the detail view, you can't edit them from the list view. You can only edit a recipe from Your Receipes.

## Your Recipes: Edit
All aspects of the recipe can be edited, ingredients can be added and removed, images can be uploade (stored on AWS S3). uploaded images will overwrite any previously used image. The youtube link provided is verified via tge google cloud youtube api. Underneath the reipes we can cancel the edit or save the recipe via buttons. The user will then be take back to Your Recipes.

## Your Recipes: Create Recipe
The [Create Recipe Page](https://frameworksassignment.onrender.com/recipes/recipes-create/) is essentially similar in format to the Edit Recipe Page except there is no initial image to display. Users must add the recipe name, category, region, instructions and at least one ingredient and measure pair. A youtube link does not need to be provided but if one is it will be verified via the youtube api. If an imag is not uploaded the recipe will appear with the default recipe image when the user saves the recipe.
