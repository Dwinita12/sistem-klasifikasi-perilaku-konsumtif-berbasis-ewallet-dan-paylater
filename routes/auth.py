from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from utils.db import get_db
from flask_mail import Message
from extensions import mail
from message import reset_password_message
import random

auth_bp = Blueprint("auth", __name__)

# ================= LOGIN =================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        db = get_db()
        cursor = db.cursor(dictionary=True)

        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = %s
            AND password = %s
            """,
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            flash("Login berhasil", "success")
            return redirect(url_for("dashboard.home"))

        else:
            flash("Username atau password salah", "danger")

    return render_template("login.html")


# ================= REGISTER =================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        db = get_db()
        cursor = db.cursor()

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            flash("Email sudah dipakai", "danger")

            cursor.close()
            db.close()

            return redirect(url_for("auth.register"))

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password, role)
            VALUES (%s, %s, %s, 'user')
            """,
            (username, email, password)
        )

        db.commit()

        cursor.close()
        db.close()

        flash("Registrasi berhasil", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ================= FORGOT PASSWORD =================
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            otp = random.randint(100000, 999999)

            session["otp"] = otp
            session["reset_email"] = email

            msg = Message(
                subject="Kode Reset Password",
                sender="system",
                recipients=[email]
            )

            msg.body = reset_password_message(otp)

            mail.send(msg)

            flash("OTP dikirim ke email", "success")

            return redirect(url_for("auth.verify"))

        else:
            flash("Email tidak ditemukan", "danger")

    return render_template("forgot_password.html")


# ================= VERIFY OTP =================
@auth_bp.route("/verify", methods=["GET", "POST"])
def verify():

    if request.method == "POST":

        otp = request.form.get("otp")

        if str(otp) == str(session.get("otp")):

            flash("OTP benar", "success")

            return redirect(
                url_for("auth.reset_password")
            )

        else:
            flash("OTP salah", "danger")

    return render_template("verify_code.html")


# ================= RESET PASSWORD =================
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if request.method == "POST":

        new_password = request.form.get("password")

        email = session.get("reset_email")

        if not email:

            flash(
                "Sesi reset password tidak ditemukan",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE users
            SET password=%s
            WHERE email=%s
            """,
            (new_password, email)
        )

        db.commit()

        cursor.close()
        db.close()

        session.pop("otp", None)
        session.pop("reset_email", None)

        flash(
            "Password berhasil direset",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("reset_password.html")


# ================= LOGOUT =================
@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Berhasil logout", "success")

    return redirect(url_for("auth.login"))