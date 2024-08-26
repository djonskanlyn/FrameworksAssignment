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
The [about page](https://frameworksassignment.onrender.com/about/) gives details about the 


