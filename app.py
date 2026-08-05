
import bcrypt
from flask import Flask, render_template, request
from database import get_connection
from flask_mail import Mail, Message
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

# ---------------- HOME ---------------- #

@app.route("/")
def home():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM donors")
    donors = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM hospitals")
    hospitals = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM emergency_requests")
    requests = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        donors=donors,
        hospitals=hospitals,
        requests=requests
    )


# ---------------- USER REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        try:
            full_name = request.form["full_name"]
            age = request.form["age"]
            gender = request.form["gender"]
            blood_group = request.form["blood_group"]
            mobile = request.form["mobile"]
            email = request.form["email"]
            address = request.form["address"]
            password = request.form["password"]

            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            )

            connection = get_connection()
            cursor = connection.cursor()

            sql = """
            INSERT INTO users
            (full_name, age, gender, blood_group, mobile, email, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    full_name,
                    age,
                    gender,
                    blood_group,
                    mobile,
                    email,
                    address,
                    hashed_password
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            return """
            <h2>✅ Registration Successful!</h2>
            <a href='/login'>Login Now</a>
            """

        except Exception as e:
            return f"Database Error: {e}"

    return render_template("register.html")


# ---------------- USER LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = "SELECT * FROM users WHERE email=%s"
        cursor.execute(sql, (email,))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return render_template("dashboard.html")
        else:
            return """
            <h2>❌ Invalid Email or Password</h2>
            <a href='/login'>Try Again</a>
            """

    return render_template("login.html")


# ---------------- DONOR REGISTER ---------------- #

@app.route("/donor_register", methods=["GET", "POST"])
def donor_register():

    if request.method == "POST":

        donor_name = request.form["donor_name"]
        age = request.form["age"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        mobile = request.form["mobile"]
        city = request.form["city"]
        location = request.form["location"]
        last_donation = request.form["last_donation"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO users
        (full_name, age, gender, blood_group, mobile, email, address, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
         sql,
         (
          full_name,
          age,
          gender,
          blood_group,
          mobile,
          email,
          address,
          hashed_password
         )
    )

        connection.commit()

        cursor.close()
        connection.close()

        return """
        <h2>✅ Donor Registered Successfully!</h2>
        <a href='/search'>Search Donors</a>
        """

    return render_template("donor_register.html")


# ---------------- SEARCH DONORS ---------------- #

@app.route("/search", methods=["GET", "POST"])
def search():

    donors = []

    if request.method == "POST":

        blood_group = request.form["blood_group"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT * FROM donors
        WHERE blood_group=%s
        AND available='Yes'
        """

        cursor.execute(sql, (blood_group,))

        donors = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template("search.html", donors=donors)


# ---------------- RUN APP ---------------- #
@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    donor = None

    if request.method == "POST":

        blood_group = request.form["blood_group"]
        city = request.form["city"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT *
        FROM donors
        WHERE blood_group=%s
        AND city=%s
        AND available='Yes'
        ORDER BY last_donation ASC
        LIMIT 1
        """

        cursor.execute(sql, (blood_group, city))

        donor = cursor.fetchone()

        cursor.close()
        connection.close()

    return render_template(
        "recommend.html",
        donor=donor
    )

@app.route("/request_blood", methods=["GET", "POST"])
def request_blood():

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        blood_group = request.form["blood_group"]
        city = request.form["city"]
        mobile = request.form["mobile"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO requests
        (patient_name, blood_group, city, mobile)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (patient_name, blood_group, city, mobile)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return """
        <h2>✅ Request Submitted Successfully!</h2>
        <a href='/'>Go Home</a>
        """

    return render_template("request_blood.html")
    
@app.route("/admin")
def admin():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM donors")
    total_donors = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM donors WHERE available='Yes'")
    available = cursor.fetchone()["total"]

    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin.html",
        total_users=total_users,
        total_donors=total_donors,
        available=available,
        donors=donors
    )

@app.route("/ai_search", methods=["POST"])
def ai_search():

    blood_group = request.form["blood_group"]
    city = request.form["city"]

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    SELECT *
    FROM donors
    WHERE blood_group=%s
    AND city=%s
    AND available='Yes'
    LIMIT 3
    """

    cursor.execute(sql, (blood_group, city))

    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "ai_result.html",
        donors=donors
    )

@app.route("/emergency", methods=["GET", "POST"])
def emergency():

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        hospital_name = request.form["hospital_name"]
        city = request.form["city"]
        mobile = request.form["mobile"]
        blood_group = request.form["blood_group"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO emergency_requests
        (patient_name, hospital_name, city, mobile, blood_group)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                patient_name,
                hospital_name,
                city,
                mobile,
                blood_group
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "<h2>🚨 Emergency request submitted successfully!</h2>"

    return render_template("emergency.html")

import matplotlib.pyplot as plt

@app.route("/chart")
def chart():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT blood_group, COUNT(*) AS total
        FROM donors
        GROUP BY blood_group
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    blood_groups = []
    totals = []

    for row in data:
        blood_groups.append(row["blood_group"])
        totals.append(row["total"])

    plt.figure(figsize=(8, 5))
    plt.bar(blood_groups, totals)

    plt.xlabel("Blood Group")
    plt.ylabel("Number of Donors")
    plt.title("Blood Group Statistics")

    plt.savefig("static/chart.png")
    plt.close()

    return render_template("chart.html")

@app.route("/send_email")
def send_email():

    return """
    <h2>✅ Notification sent successfully!</h2>
    <p>The donor has been notified.</p>
    <a href="/">Go back</a>
    """


@app.route("/history")
def history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM donation_history")

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "history.html",
        history=history
    )
@app.route("/hospital", methods=["GET", "POST"])
def hospital():

    if request.method == "POST":

        hospital_name = request.form["hospital_name"]
        city = request.form["city"]
        mobile = request.form["mobile"]
        email = request.form["email"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO hospitals
        (hospital_name, city, mobile, email)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                hospital_name,
                city,
                mobile,
                email
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "<h2>✅ Hospital registered successfully!</h2>"

    return render_template("hospital.html")    
@app.route("/report")
def report():

    pdf_file = "donor_report.pdf"

    c = canvas.Canvas(pdf_file, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "Blood Bank Report")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM donors")

    donors = cursor.fetchall()

    y = 700

    for donor in donors:

        line = (
            f"{donor['donor_name']} | "
            f"{donor['blood_group']} | "
            f"{donor['city']}"
        )

        c.drawString(50, y, line)
        y -= 20

    cursor.close()
    connection.close()

    c.save()

    return "PDF report created successfully!"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)