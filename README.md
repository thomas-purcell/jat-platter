# JAT - Platter MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
2. A Python Flask container to implement a REST API
3. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
2. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
3. Build the images with `docker compose build`
4. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

### Project Summary

    Platter is a recipe app that allows users to create, review, share, and bookmark their favorite recipes. A logged-in user can have one of three roles: Creator, Critic, and Admin. Critics review recipes that creators create. Admins are responsible for maintaining the database and have permission to delete all accounts and recipes.

### Current Functionality

    Platter currently has functionality for Creators and Critics. 

    Creators have a profile page where they can log in, update their name, and see their created recipes. They also have a create recipe page where they can create a new recipe, origin, or ingredient. They can also eidt their previous recipes by adding/changing its title, difficulty, ingredients and instructions.  

    Critics also have a profile page where they can log in, update their name, see the creators they are following and the recipes they have bookmarked, and follow and unfollow creators. They also have a search page where they can search for recipes based on the cuisine and category of the recipe and ingredients they have.

### Demo Link

    https://youtu.be/uK-_pyZvkIM

#### Built by Jiya Lakhani, Tom Purcell, and Allison Lisciandro







