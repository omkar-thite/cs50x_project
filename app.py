
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, rupee

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# Session and database confugiration settings are copied from pset9
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["rupee"] = rupee

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///store.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache" 
    return response


@app.route("/")
@login_required
def index():
    store = db.execute("SELECT store_name FROM users WHERE id = ?", session["user_id"])
    return render_template("home.html", store=store)


# Login and Logout are copied from pset9 distribution code
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # POST request
    if request.method == "POST":

        # get username and password from user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate username
        if not username or username == " ":
            flash("must provide valid username")
            return redirect("/register")

         # Ensure password was submitted
        elif not password:
            flash("must provide password")
            return redirect("/register")
        elif password != confirmation:
            flash("Password do not match!")
            return redirect("/register")
        elif len(password) < 8:
            flash("Password must have at least 8 characters")
            return redirect("/register")

        # check if username already exists
        users = db.execute("SELECT * FROM users WHERE username = ?", username)
        if users:
            flash("username already exists!")
            return redirect("/register")


        # Insert user's details into database
        else:
             # get store details
            store_name = request.form.get("store_name")
            contact = request.form.get("contact")
            store_address = request.form.get("store_address")
            name = request.form.get("name")
            email = request.form.get("email")
            
            # validate info
            if not name or name == " ":
                flash("must provide valid name")
                return redirect("/register")

            elif not store_name or not store_address or not email:
                flash("Enter required fields")
                return redirect("/register")

            elif store_name =="" or store_address == "" or name=="":
                flash("Enter valid store name/address And/or your name")
                return redirect("/register")

            elif "@" not in email or email=="":
                flash("Invalid e-mail")
                return redirect("/register")
            
            elif contact:
                if not contact.isnumeric():
                    flash("Enter valid mobile number")
                    return redirect("/register")
            
            # Enter user's detailes into database
            
            hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length = 8)

            insert_user = db.execute(
                "INSERT INTO users (username, hash, store_name, contact, store_address, name, email) VALUES(?)", 
                [username, hash, store_name, contact, store_address, name, email])
            
            if not insert_user:
                return apology("Operation Failed!")
                
            else:
                flash("Registration Successdull")
                return redirect("/login")

    # GET request
    else:
        return render_template("register.html")


@app.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():

    # POST request
    if request.method == "POST":
        particulars = request.form.get("particulars")
        try:
            purchase_rate = float(request.form.get("purchase_rate"))
            quantity = int(request.form.get("quantity"))
            amount = purchase_rate * quantity
        except ValueError or KeyError:
            return apology("Please Enter valid details")

        if not particulars or particulars.isnumeric():
            return apology("Enter valid particulars")
        
        # get vendor details
        vendor_name = request.form.get("name")
        vendor_email= request.form.get("email")
        vendor_contact= request.form.get("contact")
    
        if not vendor_name or not vendor_email:
            return apology ("Enter vendor details")

        # get username
        user_id = session["user_id"]
        user = db.execute("SELECT username AS user FROM users WHERE id = ?", user_id)
        username = user[0]["user"]

        # Enter vendor details if does not exists already 
        vendor = db.execute("SELECT * FROM person WHERE name = ? AND user_id = ?", vendor_name, user_id)
        if not vendor:
            test = db.execute("INSERT INTO person(user_id, name, email, contact) VALUES (?)",[user_id, vendor_name, vendor_email, vendor_contact])
            if not test:
                return apology("person Error!")

        # get vendor id 
        get_id = db.execute("SELECT id FROM person WHERE name = ? AND user_id = ?", vendor_name, user_id)
        person_id = get_id[0]["id"]

        # Record trasnsaction
        insert = db.execute(
                "INSERT INTO transactions (user_id, person_id, particulars, purchase_quantity, purchase_rate, amount) VALUES(?)",
                [user_id, person_id, particulars, quantity, purchase_rate, amount])
        if not insert:
            return apology("transaction Error")

        # Update inventory
        select = db.execute("SELECT * FROM inventory WHERE particulars = ? AND user_id = ?", particulars, user_id)
        if select:
            update = db.execute("UPDATE inventory SET quantity = quantity + ? WHERE particulars = ? AND user_id = ?", quantity, particulars, user_id)            
            flash("success", 'success')
            return redirect("/purchase")
        else:
            # Add item to inventory
            insert_ = db.execute("INSERT INTO inventory(user_id, particulars, quantity) VALUES (?,?,?)",user_id, particulars, quantity)
            if not insert_:
                return apology("Opearation failed!")

            flash("success", 'success')
            return redirect("/purchase")
    # GET request
    else :
        return render_template("purchase.html")


@app.route("/sale", methods=["GET", "POST"])
@login_required
def sale():
    # POST request
    if request.method == "POST":
        try:
            particulars = request.form.get("particulars")
            price = float(request.form.get("price"))
            quantity = int(request.form.get("quantity"))            
        except ValueError:
            flash("Enter valid details", 'danger')
            return redirect("/sale")
        
        try:
            discount = float(request.form.get("discount"))
        except ValueError:
            flash("Enter valid details", 'danger')
            return redirect("/sale")

        # Validate user input
        if not particulars or particulars == "" or particulars.isnumeric():
            return apology("Enter valid details")
        
        if not price or not quantity:
            return apology("Please enter required details")
        
        # check if required quantity is available
        quantity_check = db.execute("SELECT * FROM inventory WHERE particulars = ? AND user_id = ?", particulars, session["user_id"])

        if not quantity_check:
            return apology("Item not available")

        quantity_available = quantity_check[0]["quantity"]

        if quantity_available < quantity:
            return apology("Not enough quantity available")

        # net amount = total amount - discount 
        net_amount =  (price * quantity) - (((price * quantity) * discount) / 100)

        # Get customer details
        name = request.form.get("name")
        email = request.form.get("email")
        contact = request.form.get("contact")
        if not name or not email:
            return apology("Please Enter Customer Details")

        # get customer id
        get_id = db.execute("SELECT id FROM person WHERE name=? AND email=?", name, email)
        
        # Add customer to person table 
        # insert customer if doesn't exists 
        if not get_id:
            insert_customer = db.execute("INSERT INTO person(user_id, name, email, contact) VALUES(?)", [session["user_id"], name, email, contact])
            if not insert_customer:
                return ("Customer could not be registered!")
            else:
                # if susscefully inserted then get person id
                ID = db.execute("SELECT id FROM person WHERE name = ? AND email = ?", name, email)
                id = ID[0]["id"]
        else:
        # if person exists in tble already
            id = get_id[0]["id"]

        # Insert sale into transaction table
        sale = db.execute("INSERT INTO transactions(user_id, person_id, particulars, sale_quantity, sale_price, discount, amount) VALUES (?)",
                    [session["user_id"], id, particulars, quantity, price, discount, net_amount])
        if not sale:
            flash("transaction fail", 'danger')
            return redirect("/sale")
        
        # update quantity in inventory
        net_quantity = quantity_available - quantity
        update = db.execute("UPDATE inventory SET quantity = quantity - ? WHERE particulars = ?", quantity, particulars)
        
        # Delete item if quantity is 0
        quantity_ = db.execute("SELECT quantity FROM inventory WHERE particulars = ?", particulars)
        if quantity_[0]["quantity"] == 0:
            delete = db.execute("DELETE FROM inventory WHERE particulars = ?", particulars)
            if not delete:
                return apology("Operation Error")

        store = db.execute("SELECT store_name, store_address FROM users WHERE id = ?", session["user_id"])
        if not store:
            return apology("Store Not Found!")

        sales = {
            "particulars": particulars,
            "quantity": quantity,
            "rate": price,
            "discount": discount, 
            "amount": net_amount,
        }

        flash("success", category='success')
        return render_template("invoice.html", sales=sales,store=store)
    
    # GET request
    else:
        return render_template("sale.html")


@app.route("/inventory")
@login_required
def inventory():
    # get user id
    user_id = session["user_id"]
    inventories = db.execute("SELECT * FROM inventory WHERE user_id = ? ORDER BY particulars ASC", user_id)
    if not inventory:
        return apology("No items yet")
    return render_template("inventory.html", inventories = inventories)


@app.route("/reset", methods = ["GET", "POST"])
def ChangePassword():
    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Invalid username or password")

        users = db.execute("SELECT username FROM users")

        for user in users:
            if user["username"] == username:
                hash = generate_password_hash("password")
                i = db.execute("UPDATE users SET hash=? WHERE username=?", hash, username)
                if i:
                    return redirect("/login")
                else:
                    return apology("operation failed")
        return apology("no username found")
    # GET
    else:
        return render_template("reset.html")


@app.route("/transactions", methods = ["GET", "POST"])
@login_required
def transactions():

    user_id = session["user_id"]
    # POST
    if request.method == "POST":
        particulars = request.form.get("particulars")
        if not particulars:
            return apology("Error")
        
        # Select transactions of particulars
        transactions = db.execute("SELECT * FROM transactions WHERE particulars = ? AND user_id = ?", particulars, user_id)
        people = db.execute("SELECT id, name FROM person WHERE user_id = ?", session["user_id"])

        dates = db.execute("SELECT id, DATE(time) FROM transactions WHERE particulars = ? AND user_id = ?",particulars, user_id)

        return render_template("transactions.html", people=people, particulars=particulars, dates=dates, transactions = transactions)
    # GET
    else:
        dates = db.execute("SELECT id, DATE(time) FROM transactions WHERE user_id = ?", user_id)
        people = db.execute("SELECT id, name FROM person WHERE user_id = ?", user_id)
        transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
        
        return render_template("transactions.html", dates=dates, people=people, transactions=transactions)


@app.route("/invoice", methods=["GET", "POST"])
@login_required
def invoice():
    # POST (through transactions)
    if request.method == "POST":

        store = db.execute("SELECT store_name, store_address FROM users WHERE id = ?", session["user_id"])
        if not store:
            return apology("Store Not Found!")
        
        particulars = request.form.get("particulars")
        quantity = request.form.get("quantity")
        rate = request.form.get("rate")
        discount = request.form.get("discount")
        amount = request.form.get("amount")
        
        sales = {
            "particulars": particulars,
            "quantity": quantity,
            "rate": rate,
            "discount": discount,
            "amount": amount,
        }
        return render_template("invoice.html", sales=sales,store=store)
    else:
        return apology("Something Went Wrong")