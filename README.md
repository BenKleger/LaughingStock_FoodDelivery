# LaughingStock_FoodDelivery

## Project Description and Goal
The goal of this project is to design and build a scalable full-stack dockerized multiuser food delivery application system. With the real-world online dataset, the system will implement backend functionality utilizing modern software engineering practices to mimic a deployed version of the app. The platform will provide secure login and authorization and will allow users of all types to modify details and interact with app assets. The system will be built on RESTful API which will aid in enabling the implementation of countless features such as filtering orders/menu items, and more. The platform will be built to operate reliably and will act as a full, albeit undeployed, food delivery application system.

## Maintenance Requirements
Account credentials:
  ### REDACTED
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



## Features and Requirements
Feature 1 (FEAT1): The system will allow users and restaurant owners/managers to create accounts and log in. It will handle user authentication (login), authorization (what each user is allowed to do), and basic user identity management. Different roles such as regular users and restaurant owners/managers will be supported.
FEAT1-FR1: The system shall allow creation of multiple types of accounts (manager [restaurant owners / managers], drivers and users), with different permission levels.
FEAT1-US1: As a system user (user, driver, or manager), I want to be able to create an account so that I can access the service.
Accounts are granted extra permissions for restaurant management or customer management features according to the account type.
The user's account data is saved and stored in the system.
The account creation screen has selectable options for customer(default), delivery, or manager.
FEAT1-FR2: The system shall allow access to created accounts.
FEAT1-US2: As a system user, I want to be able to login to my account so that I can access the service repeatedly.
If the login attempt is invalid, prompt retry after displaying text “invalid login”.
To login the user must enter valid credentials for email and password.
FEAT1-FR3: The system shall support user identity management, ensuring passwords are stored hashed.
FEAT1-US3: As a system user, I want to have a password so that I can be sure that no one else can access my account.
To login the user must enter valid credentials for email and password.
The system stores sensitive data with (salted) hashes.


Feature 2 (FEAT2): The system will store information about restaurants and their menus. It will ensure that data is valid, properly connected (for example, menu items must belong to a restaurant), and that basic constraints are enforced, such as preventing invalid or missing values.
FEAT2-FR1: The system shall store restaurant name, location, menu, and contact information for each restaurant that wants to deliver through the system. 
FEAT2-US1: As a user, I want to be able to filter restaurants by the style of cuisine they offer.
Selecting style filters will only display restaurants of matching style tags.	
FEAT2-US2: As a user, I want to be able to see the menu for any given restaurant so I can decide on which restaurant to order from and what to order.
Searching by restaurant allows the user to view the entire menu for a given restaurant.
FEAT2-US3: As a user, I want to be able to see the location and distance/ETA for any given restaurant so that I can decide whether the wait or payment is worth it.
System updates user location approximately every minute and the ETA reflects that (ETA will be displayed at order checkout in the order list screen)
FEAT2-FR2: The system shall validate entries in input fields by checking to make sure each field is filled with no errors.
FEAT2-US4: As a user, I want to be able to search without having errors, so that I can avoid breaking the system and get my results.
Errors are found.
Users are notified of errors, where and what.
FEAT2-FR3: The system shall allow adding businesses and menu items.
FEAT2-US5: As a manager, I want to be able to add my business and related information to the system so customers can make purchases at my business.
Accounts having manager level can choose to input restaurant details including: open hours, policies, fun description, phone, and website link. 
FEAT2-US6: As a manager, I want to be able to add my menu items and price them accordingly so customers can purchase them.
Accounts with manager level can submit a menu list with images and descriptions for each item which is stored and linked to their owned restaurant.
Menu information is checked that a description is written, an image is present, and no special characters are submitted.
Invalid menu item inputs from manager account prompts re-entry.


Feature 3 (FEAT3): The system will allow users to browse restaurant menus and search for items or restaurants. Backend logic will handle filtering, searching, and returning paginated results.
FEAT3-FR1: The system shall be dynamically filterable to produce results relevant to the user.
FEAT3-US1: As a user, I want to be able to filter any given restaurant’s offerings (appetizers, main, dessert, drinks, etc.) based on common criteria (e.g. type, price, popularity) to decide on what to order.
When a filter option(s) are selected only matching menu offerings are shown. If no item matches display message “no matches”
FEAT3-US2: As a user, I want to be able to search for restaurants and menu items to decide on what to order.
The search feature is in the food menu that does text matching which updates results for each character typed.
The search feature is clearly present on restaurants list and does text matching which updates results for each character typed.
FEAT3-FR2: The system shall allow managers to add and edit menu items and applicable tags.
FEAT3-US3: As a manager, I want to be able to add tags to my menu items and business so users can effectively search/filter for them.
Account of manager status can add and remove up to 4 tags for their restaurant and individual food items


Feature 4 (FEAT4): The system will allow users to create and manage food orders. It will ensure that orders are consistent, correctly stored, and follow business logic for the domain (for example, an order cannot be modified after it is completed).
FEAT4-FR1: The system shall allow creation and management of food orders, ensuring correctness.
FEAT4-US1: As a user, I want to be able to place an order for items from a restaurant.
Selected menu items are displayed in an order list for complete viewing.
Once the user places an order using the “order now” button, the payment method screen will be displayed.
FEAT4-US2: As a user, I want to be able to cancel an order before it is complete if I change my mind.
In the order list, the user can remove individual items or scrap the entire order list.
FEAT4-FR2: The system shall allow additional information to be added to orders for custom instructions.
FEAT4-US3: As a user, I want to be able to add custom delivery instructions so suit my needs.
Next to the order button, the customer can write “special instructions” which are sent to the delivery driver along with the list. These details are sent and received in ~2 minutes.


Feature 5 (FEAT5): The system will manage delivery-related information. It will support assigning deliveries and tracking basic delivery status as part of the backend logic.
FEAT5-FR1: The system shall support delivery time and routing information.	
FEAT5-US1: As a driver, I want to see where I am supposed to deliver to, and custom delivery instructions so I can make a delivery as specified by the customer.
In the delivery details page there is a button labelled “navigation” that will show the driver a map and automatically route the driver to the restaurant(s) for pickup.
After accepting a listing the delivery driver has a delivery details page where can view the “special instructions” the customer has sent as well as their list, restaurant name, and customer address. (details received within 2-5 seconds).
The driver can confirm pickup by pressing the same navigation button again which will re-route to the customer's address.
FEAT5-US2: As a driver, I want to see an ETA for the restaurant, and destination so I can effectively manage my time.
Delivery drivers can navigate to a screen where there are listings for nearby orders. The listing will display restaurant name, ETA for drivers current location + restaurant to customer location, and payout.
FEAT5-FR2: The system shall communicate the delivery information to the user that made the order.
FEAT5-US3: As a user, I want to be able to view delivery information, so that I know when my food is coming.
Once the navigation button has been pressed a second time, a status update is displayed for the customer which displays an ETA based on how far the driver is from their location.
The customer delivery information screen automatically displays once an order is placed containing ETA, amount paid, and items ordered. Only one order may happen per customer at a time.


Feature 6 (FEAT6): The system will calculate the total cost of an order, including item prices, delivery fees, and taxes. These calculations will follow predefined business rules implemented in the backend.
FEAT6-FR1: The system shall calculate the total amount of money for the user to pay.
FEAT6-US1: As a user, I want to be able to know the total cost of the food before purchase, so that I know if I’m willing to buy it.
Order list contains summary details including pricing of each individual item, total cost, tax, discount, delivery free, tip%, fees. Updates to the order list are reflected in summary details within ~2 seconds.
Once an order is placed and confirmed the price remains fixed.
FEAT6-FR2: The system shall calculate the amount of delivery money for the driver to receive.
FEAT6-US2: As a driver, I want to be able to know the amount of pay I will receive for delivering an order.
On a drivers account, when viewing the available delivery options, text next to the “accept delivery” button will display the calculated cut of the payment the driver will receive which includes the customer's tip %.
Once an order is accepted by the delivery driver their earnings are fixed.


Feature 7 (FEAT7) (simulated): The system will simulate payment processing. No real payment gateway will be used, but the system will follow the correct workflow for accepting or rejecting a payment and updating the order status.
FEAT7-FR1: The system shall check the payment information, accepting or rejecting the order based on if the order is accepted and update the order status. 
FEAT7-US1: As a user, I want to be able to pay for my order, so that the order can be completed.
The payment method screen contains types of offered payment methods, debt, credit, paypal, and apple pay. 
Once the user chooses a payment method a window will appear asking them to input valid information. Paypal and Apple require you to sign in to your email account and associated password. Credit and Debt requires a 16 digit entry, a cardholder name, a postal code, a billing address, and CVV.
Button labeled “complete payment” will be present in the 4th quartile of the screen and once pressed, all information that was inputted will be “checked against bank/company’s database for validity” ~15 seconds.
Upon payment completion a confirmation window saying “purchase complete” appears with an x button in the top right.
If payment declined, a window appeared stating “payment failed, please try again”. Two buttons show below the message one labelled “cancel” which cancels the order before it is placed and the other labelled “retry” which causes the payment method window to re-appear.
FEAT7-US2: As a driver, I want to be able to receive payment for my work.
Upon successful order, the driver’s share of it is paid ~2 minutes.
FEAT7-US3: As a manager, I want to be able to receive payment for my products.	
Upon successful order, the restaurant’s share of it is paid, within ~2 minutes.
Feature 8 (FEAT8): The system will generate notifications or events when important actions occur, such as order creation or status changes.
FEAT8-FR1: The system shall generate user notifications for order confirmation.
FEAT8-US1: As a user, I want to see confirmation for when I order food so I can be sure that an order is confirmed.
When an order is successfully placed an automatic message will display “order placed!” for ~3 seconds and then automatically display the customer delivery information screen.
FEAT8-FR2: The system shall generate user notifications for delivery nearing destination.
FEAT8-US2: As a user, I want to see a notification when the delivery is on its way or almost here so I can prepare for the driver.
As the driver approaches the customer location < 500m a drop down notification is sent to the customer saying “order is almost arriving”. 
When the navigation button is pressed by the driver a drop down notification is sent to the customer ~10 seconds.
FEAT8-FR3: The system shall generate user notifications for cancellations.
FEAT8-US3: As a user, I want to know when a driver or restaurant cancels an order so I can stop waiting and make another order.
When a driver cancels an order, the customer is immediately notified via drop down notification and payment is refunded ~30 seconds 
FEAT8-FR4: The system shall generate user notifications for driver messages.
FEAT8-US4: As a user, I want to see a notification when a driver messages me about the order so I can receive them on time and provide a quick response.
If the driver sends a message using in app messaging the user is notified in ~2 seconds. The drop down notification will contain the driver name, and preview of up to 20 characters of the message received. 
FEAT8-FR5: The system shall generate driver notifications for nearby restaurant orders.
FEAT8-US5: As a driver, I want to see a notification for orders for restaurants near me so that I can efficiently plan deliveries.
Drivers are notified via drop down for orders placed at restaurants within 5km of their current location which updates ~1min
FEAT8-FR6: The system shall generate driver notifications for order cancellations.
FEAT8-US6: As a driver, I want to see when a user or restaurant cancels an order so that I do not waste time completing the order.
Orders that are cancelled are taken off the order listings within ~2 seconds 





Non-Functional Requirements
Security: The system will have standard security measures such as 2FA and password lockouts. Passwords will be hashed and encrypted.
Reliability: The system must have 99% uptime, and the software should not lose excessive data in case of a crash, 
Usability: The software must be easy to use, have a user-friendly interface, and be intuitive to learn. New users should be able to use main features without a dedicated walkthrough or tutorial.
Maintainability: New features should be able to be added and tested without touching existing features. 
Performance: The system must support multiple users concurrently, without significant slowdowns.
Compatibility: The application will run on Android 15+ devices (Pixel 9A).

Domain Requirements
A user can only be either an manager, customer or a restaurant manager. 
Each customer has to be valid and registered before having the ability to place an order
Each customer must have valid and verified information entered (payment, name, address, etc.) before completing transaction
Each customer must have the ability to report or give reviews only once per order
Admin must have the ability to delete/suspend restaurants
Each restaurant manager must only manage restaurants under their oversight
Each restaurant manager can add/delete/edit menu and menu items
Each restaurant must have a menu with orderable items
Each menu item must include name, price, and availability status. 
Each order must have its own associated price reflecting any changes, substitutions, and modifications
Each order cannot be modified after its placed and/or processed
Each order must be associated with a single restaurant, user, and address
Each order must include at least one item
An order cannot be placed unless the system approves the transaction
The system must either accept or reject an order
The system must calculate taxes and relevant charges based on location
The system must keep track of the order and its step in the order workflow
The system must allow users create an account and to log in
The system must be able to identify users by their roles and their allowed actions
The system must be able to identify invalid or incomplete operations and warn the user
The system must allow users to browse different menus and items, and search/filter by preferences
The system must distribute funds between all users automatically upon completion of order
Delivery driver may only have one active assignment at a time
Delivery driver must be able to accept/reject orders

Architecture Overview
The system will be created with the client/service architecture. This model is ideal because the service we provide will be used by multiple clients at one time, each of which will be accessing multiple features. The modularity of this architecture allows us to separate feature components which makes development and testing smoother. Many benefits arise from having clients communicate with the server such as:
- Login feature benefits from the separate servers because it will store sensitive data away from other components. The password can be hashed and stored on the server side. All the client needs to sign in is valid matching credentials. Authentication logic is kept hidden on the client side.
- Manager level accounts will be able to create and upload a menu for their establishment to the server side. When customers want to view the menu, their device will communicate to the server to receive the latest uploaded menu. Menu's can only be uploaded by manager accounts so keeping authentication server sided restricts clients without access from changing anything. Invalid menu data will be rejected from being stored ensuring the menu doesn't update for clients until a manager submits a valid entry. 
- Customer searching logic can be handled on the backend and only the results will be displayed to the client. This keeps the client side running smoothly for a better user experience.
- Placed orders and calculation logic for orders are evenly distributed to each client because all of it will be stored in its own component server. Any updates to the calculation logic can be applied for all users at once since they all communicate with the same server. Orders are secured so that clients can't tamper with them by accident or maliciously. 
- Delivery information such as assignees, GPS tracking, and status will be done in real time for clients to see. Delivery information from the driver is pushed to the server where the user can view the most recent information like driver location, ETA calculation, and delivery status. 
- Transaction management is all handled away from the client. The server will process and validate client transaction info and update order status accordingly. The client only sees the transaction status to avoid any potential tampering. 

All of these benefits work towards the non-functional requirements by providing consistent functionality for all users, proper security from separating sensitive features from non-sensitive ones, easy across the board updates for maintainability, and server sided processing for system performance on the client end.








Low-Level Design

Component Identification
Account Manager
Desc: 
Supports account creation, secure login, cart items, and user details, and history. 
Classes: 
User, Customer, RestaurantManager, DeliveryDriver, Admin
Interacts with… 
	Order Manager to place/manage orders
	Restaurant Manager to browse restaurants and menu items
 
Restaurant Manager
Desc:
Manages restaurants profiles, and their respectable orderable items on their individual menus. Supports browsing items from different categories, and restaurants.
Classes: 
Restaurant, Menu, Item
Interacts with…
Account Manager to identify allowed actions of the user so they can place/modify/manage orders

Order Manager
Desc: 
Manages the creation of orders, order status and archival. Overseers all orders made by users along with their end-to-end completion statuses. Enforces immutability.
Classes: 
Order, OrderStatus
Interacts with… 
	Account Manager to process orders from select users
	Restaurant Manager to validate order details
	Payment System to process payment for the order
	


Payment System
Desc: 
Calculates and aggregates all fees, taxes, and order prices. Additionally simulates payment approval/denial, and provides receipt/invoice.
Classes: 
PaymentServices
Interacts with… 
	Order Manager to compute order cost, and simulated payment process.

GPS System
Desc:
Dynamically provides routing and directions support to delivery drivers for pick-up and drop off locations.
Classes:
	GPSService
Interacts with…
Payment System for order verification; is the order deliverable?
	Order Manager for customer location data for route generation.


