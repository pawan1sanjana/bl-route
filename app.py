from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
from static.database.databases import get_db

app = Flask("ItzSimplyJoe")
app.secret_key = 'superawesomesecretkey1010001'

CUSTOMERS_FILE = "customers.json"

# Utility functions for JSON customer management
def load_customers():
    """Load customer data from the JSON file."""
    try:
        with open(CUSTOMERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_customers(customers):
    """Save customer data to the JSON file."""
    with open(CUSTOMERS_FILE, "w") as file:
        json.dump(customers, file, indent=4)

# Routes for user account management
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login")
def signup():
    return render_template("login.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route("/createaccount", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    others = db.fetch(username)
    if others:
        flash("Username already exists", "error")
        return redirect(url_for("signup"))
    else:
        if len(password) < 8:
            flash("Password must be at least 8 characters long", "error")
            return redirect(url_for("signup"))
        else:
            try:
                db.insert(username, password)
                flash("Account created successfully, please login", "success")
                return redirect(url_for("login"))
            except:
                flash("An error occurred", "error")
                return redirect(url_for("signup"))

@app.route("/login_account", methods=["POST"])
def login_account():
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    user = db.login(username, password)
    if user:
        return redirect(url_for("success"))
    else:
        flash("Incorrect username or password", "error")
        return redirect(url_for("login"))

# Routes for customer management
@app.route("/customers")
def index():
    return render_template("index.html")

@app.route("/api/customers", methods=["GET", "POST", "PUT"])
def manage_customers():
    customers = load_customers()

    if request.method == "GET":
        return jsonify(customers)

    if request.method == "POST":
        new_customer = request.json
        new_customer["id"] = max(customer["id"] for customer in customers) + 1 if customers else 1
        customers.append(new_customer)
        save_customers(customers)
        return jsonify({"message": "Customer added successfully"}), 201

    if request.method == "PUT":
        updated_customer = request.json
        for customer in customers:
            if customer["id"] == updated_customer["id"]:
                customer.update(updated_customer)
                save_customers(customers)
                return jsonify({"message": "Customer updated successfully"}), 200
        return jsonify({"message": "Customer not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
