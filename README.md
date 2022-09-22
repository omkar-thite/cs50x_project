# THE STORE MANAGER
### Video Demo : https://youtu.be/0lZmnkd5JaE

#### DESCRIPTION : 

THE STORE MANAGER is a simple minimal web app that allows users to record their everyday business transactions and access that information whenever needed.  The app provides minimal forms to record transactions as well as features that give easy access to systematically stored information. App also keeps track of customers and vendors along with transactions. It also provides auto generated invoices, in a form of web-page. (of course, user can print them.) 

The app is written using Flask framework of python in backend , HTML CSS and Javascript for frontend designs.
Detail Description as follows: 
Project Folder includes following:
1.	app.py 
2.	helpers.py
3.	requirements.txt
4.	store.db
5.	static
	- styles.css
6.	templates
	- apology.html
	- home.html
	- inventory.html
	- invoice.html
	- layout.html
	- login.html
	- purchase.html
	- register.html
	- reset.html
	- sale.html
	- transactions.html

- app.py
  - A python file that named as required by flask. Code contains configurations of seesions and sqlite database file. Custom rupee filter for jija has been added.
  - isFloat(num) is defined which tests whether input is float. Furthure routes for different paths have been defined.

Routes :
- "/login"
    - user visits this page first. For GET request *login.html* page is rendered. 
    - For POST request i.e. when user submits login form, user input is validated and checked for      credentials stored in database. 
    - if credentials found and matched, user is taken to default path "/".
- "/"
    - default path which redirects to home.html with necessary information.
- "/register"
    - When GET request i.e. when user has clicked on a **Register** button, user is redirected to *registration.html*
    - When POST request i.e. when user has submitted registration form, user's credentials gets stored in database *store.db* and user gets redirected to */login* route for login.
- "/purchase"
    - **Purchase** button on homepage or in navigation bar send user to this route.
    - GET request: *purchase.html* is rendered.
    - POST request: user input from *purchase.html* is validated and stored in database. User is redirected to */purchase* route via GET.
- "/sale"
    - **Sale** button on homepage or in navigation bar send user to */sale* via GET.
    - GET request: *sale.html* page is rendered.
    - POST request: user input from sale.html page is validated and stored into database. User is redirected to *invoice.html* page.
- "/inventory"
    - **Inventory** button on navbar or on homepage via GET. 
    - GET request: *inventory.html* is rendered.
    - NO POST request to this route.
- "/invoice"
    - only POST request: renders *invoice.html* with necessary informtion
    - request is made through **invoice** button available on *transaction.html* for every sale transaction.
- "/transactions"
    - POST request: Through **Details** button on *inventory.html* page. User is redirected to *transactions.html* page with necessary information where inventory specific transactions are displayed.
    - GET request: Arrived through **transactions** button on homepage or on navigation bar. *transactions.html* is rendered with necessary information to display all transactions.
- "/logout"
    - via GET only. 
    - Logs user out of session.
    - Can be arrived at by **Logout** button on navigation bar.
- "/reset"
    - via GET only. 
    - at *login.html* page, **forgot password** button is provided if user forgets his/her password.
    - Resets the password of user.

helpers.py is python file that is included in app.py. the file has been taken from distribution code of pset9 of cs50x and suitably modified for the needs of project.
It provides:
- apology() function which renders *apology.html* to user with error code 400.
- loginRequired decorator
- Jinja filter for rupee symbol

requirements.txt file includes all required modules from python.

*store.db* is the premade database file that is used to store all the information. sqlite3 module is used to process database.

templates foler contains all webpages in html format. They are as follows:
- apology.html
  - Displays apology to the user with code 400 and error message. Taken from cs50x distribution code.
- home.html
  - Displayed after login and is the home page of the project. 
  - Has Navbar with **log out** button 
  - Has four buttons **Purchase**, **Sales**, **Transactions** and **Inventory**.
- inventory.html
  - Displayes table of available inventory.
  - Quantities of items are adjusted according to sale and purchase quantities of those items.
  - **Details** button sends request to */transactions* via POST.
- invoice.html
  - Displays automatically generated sale invoice with store's name and sales details in it.
  - Currently only one particulars is allowed.
- layout.html
  - layout file that is extended in all other html pages.
  - Taken from cs50x distribution code.
  - Has code for navbar, flash messages.
- login.html
  - Displays login form
  - Coped from cs50x distribution code with some modifications.
  - Form is submitted to */login* via POST request.
  - let the user log in with username and password
- purchase.html
  - Displays purchase form. 
  - Form is sent to */purchase* via POST
- register.html
  - Displays registration form.
  - Form is submitted to */register* via POST request.
  - All fields are mandotary to fill. 
  - ***Password must be greater than 8 characters long.***
- reset.html
  - Arrived at when **forgot password** is clicked.
  - Displays form that allows users to reset their password.
- sale.html
  - Displays sale form
  - Input is sent to */sale* via POST
  - Can be accessed through **Sale** button on home page or on navbar.
  - User has to enter transaction as well as customer's details. (mandotary)
- transactions.html
  - This page serves two requests from two different routes.
  - This page is rendered when user clicks **Details** button on inventory page for specific item, and ***shows item specific transactions*** only. This request is sent from */transacions* route via POST method with necessary information. 
  - Page is also rendered when user clicks on **Transactions** button, on navbar or on homepage, accessed through */transactions* route via GET request with necessary information.

Modules used:
1. cs50
   - SQL is used to configure CS50 Library to use
   SQLite database
2. flask
   - flask, flash, redirect, render_template, session 
3. flask_session
   - Sessions to configure app foe sessions.
4. werkzeug.security
   - generate_password_hash(), check_password_hash()
   - Used to generate a hash for a password and then to ckeck it for login respectively.

Javascript is used on purchase and sales page to calculate total amount.

Summary :
- A web app that can record transactions, store information about customers and vendors, gives information about available inventory and shows all past transactions of user.
- supports multiple user.

That's it.

Thank you for visiting my project.








