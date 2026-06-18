import os
from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    job_type = request.form.get("job_type")
    paper_size = request.form.get("paper_size", "")
    paper_type = request.form.get("paper_type", "")
    quantity = request.form.get("quantity", "")
    instructions = request.form.get("instructions", "")
    custom_job = request.form.get("custom_job", "")
    uploaded_file = request.files.get("file")
    msg = EmailMessage()
    msg["Subject"] = "New Print Order"
    msg["From"] = "achudigital.web@gmail.com"
    msg["To"] = "achudigital.web@gmail.com"
    msg.set_content(f"""
New Print Order Received:

Name: {name}
Phone: {phone}
Email: {email}
Job Type: {job_type}
Paper Size: {paper_size}
Paper Type: {paper_type}
Quantity: {quantity}
Instructions: {instructions}
Custom Job: {custom_job}
""")
    if uploaded_file and uploaded_file.filename != "":

        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        file_data = uploaded_file.read()
        with open(filepath, "wb") as f:
            f.write(file_data)
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=filename
        )
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(
        "achudigital.web@gmail.com",
        "fmhy gtfp ihgu fcjb"  
    )
    server.send_message(msg)
    server.quit()
    return "Order submitted successfully ✅"
if __name__ == "__main__":
    app.run(debug=True)