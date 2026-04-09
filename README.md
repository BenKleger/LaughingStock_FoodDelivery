# LaughingStock_FoodDelivery

## Project Description and Goal
The goal of this project is to design and build a scalable full-stack dockerized multiuser food delivery application system. With the real-world online dataset, the system will implement backend functionality utilizing modern software engineering practices to mimic a deployed version of the app. The platform will provide secure login and authorization and will allow users of all types to modify details and interact with app assets. The system will be built on RESTful API which will aid in enabling the implementation of countless features such as filtering orders/menu items, and more. The platform will be built to operate reliably and will act as a full, albeit undeployed, food delivery application system.

## Maintenance Requirements
Data management procedures
Data is stored in .json files in the Backend directory:
items.json
menus.json
orders.json
reviews.json
users.json
To edit data, manually go into the files and change values accordingly.
To reset data, you can manually go into the files and delete specific users / orders / items, or use the corresponding reset_<xyz>_DB() function found in the corresponding Backend/FastAPI_DB/services/<xyz>s_service.py, where  <xyz> can be either ‘order’, ‘user’ or ‘item’.
To access API endpoints and documentation, visit http://localhost:8080/docs# once the server is running.
Configuration of external APIs or service
We used FastAPI, and Docker.

## Installation Instructions: Step-by-step setup procedures for running the system using Docker.
GOTO: https://github.com/BenKleger/LaughingStock_FoodDelivery (You made it!)
clone the repository into your choice location
In the terminal of your choice location, in the LaughingStock_FoodDelivery directory:  docker compose up --build
GOTO: http://localhost:3000 this brings you to the login page, where the rest of the service can be accessed.
