#### first_dash

# Paris Tree Visualization Dash App
Welcome to the repository for the Paris Tree Visualization Dash application. This interactive web application leverages Python's Dash framework and Plotly to provide a visual exploration of tree data in Paris.

## Application Overview
The Dash application is designed to allow users to filter and visualize different attributes of trees across Paris. Users can select criteria such as the 'Domain' (DOMANIALITE) and the 'Development Stage' (STADE DE DEVELOPPEMENT) of trees through dropdown menus to customize the displayed data.

## Features
- Domain Selection: A dropdown to filter trees by their domain in Paris, such as 'Alignement', 'Jardin', etc.
- Development Stage Selection: A dropdown to filter trees by their development stage, such as 'Young', 'Adult', 'Old', etc.
- Height Distribution Graph: A histogram that updates to show the distribution of tree heights based on the filters selected.
- Circumference Distribution Graph: A histogram to visualize the distribution of tree circumferences.
- Paris Map Visualization: An interactive map displaying the location of trees with markers scaled by circumference and colored by height.
The application is responsive and updates the visualizations in real-time as users change their selections.

## Installation and Usage
Before running the application, please ensure you have Python installed on your machine and install the necessary libraries listed in requirements.txt. To start the application:
- Clone the repository.
- Navigate to the app's directory in your terminal.
- Run '''pip install -r requirements.txt''' to install the required packages.
- Execute python app.py to launch the Dash server.
- Open your web browser and go to http://127.0.0.1:8050/.

## Data
The dataset, sourced from Paris's open data portal, contains detailed information about trees within the city, including their size, species, and geographical coordinates.

## Customization
If you want to adjust the dataset or add more features to the application, you can modify the load_and_clean_data() function and callbacks to accommodate your changes. Thank you for visiting, and enjoy exploring the greenery of Paris through this application !
