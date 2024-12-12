# Recipe Suggestion

## Overview
The Fridge Inventory Management project is a web application that allows users to manage their fridge contents and get recipe suggestions based on the available ingredients. The application uses a PostgreSQL database to store user inventory data and a Flask backend to handle the server-side logic.

## Features
- **Existing User Management**: Users can view and manage the contents of their existing fridge inventories.
- **New Fridge Setup**: Users can create a new fridge inventory by adding ingredients and their quantities.
- **Recipe Suggestions**: The application provides recipe suggestions based on the user's available ingredients, including both complete recipes and partial recipes that can be made with the current inventory.

## Installation and Setup
Prerequisites:

- Ensure you have PostgreSQL installed on your local machine
- Install Python and pip
- Have Git installed (optional, but recommended)

Database Setup:

- Run the init.sql script to create the database

Database Connection:

- Open the Python files main.py and input.py
- Update the connection details to match your local PostgreSQL setup:

Installation:

- Install required Python dependencies - mentioned in the requirements.txt file

Running the Application:

Open two terminal windows
In the first terminal, run main.py
In the second terminal, run input.py
The frontend should now pop up


## Usage
- When the application loads, you'll see an option to choose between different User Fridges.
- Once you select "Select Existing User", you can browse through the existing user inventories and view their contents.
- After you choose your desired Fridge, the recipes that can be made from the available ingredients are displayed.
- The recipe suggestions are displayed in two sections: "Complete Recipes" and "Partial Recipes".
