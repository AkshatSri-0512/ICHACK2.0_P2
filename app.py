from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import json
import hashlib
import openai

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a strong, random key.



@app.route('/')
def home():
   return render_template("home.html")


@app.route('/bot')
def bot():
    return render_template("bot.html")

@app.route('/commentpatient')
def commentpatient():
   return render_template("commentpatient.html")

@app.route('/doctor')
def doctor():
   return render_template("doctor.html")

@app.route('/doctorUpload')
def doctorUpload():
   return render_template("doctorUpload.html")

@app.route('/loginDoctor')
def loginDoctor():
   return render_template("loginDoctor.html")

@app.route('/loginPatient')
def loginPatient():
   return render_template("loginPatient.html")

@app.route('/loginRepresent')
def loginRepresent():
   return render_template("loginRepresent.html")

@app.route('/patient')
def patient():
   return render_template("patient.html")



@app.route('/patientSearch')
def patientSearch():
   return render_template("patientSearch.html")

@app.route('/qr')
def qr():
   return render_template("qr.html")


@app.route('/sign')
def sign():
   return render_template("sign.html")




with open("login.json", "r") as file:
    login_data = json.load(file)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


    


@app.route("/loginDoctor", methods=["GET", "POST"])
def doctorlogin():
    if request.method == "POST":
        username = request.form["username"]
        uid = request.form["uid"]
        password = request.form["password"]

        if username in login_data and login_data[username]["uid"] == uid:
            # Hash the provided password for comparison
            hashed_password = hash_password(password)

            if login_data[username]["password"] == hashed_password:
                session["logged_in"] = True
                session["username"] = username
                flash("Login successful", "success")
                return redirect(url_for("welcomedct"))
        flash("Invalid username, uid, or password", "error")

    return render_template("loginDoctor.html")


@app.route("/welcomedct")
def welcomedct():
    if session.get("logged_in"):
        return render_template('doctor.html')
    else:
        return redirect(url_for("loginDoctor"))


@app.route("/doctorsign", methods=["GET", "POST"])
def doctorsign():
    if request.method == "POST":
        username = request.form["username"]
        uid = request.form["uid"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username in login_data:
            flash("Username already exists. Please choose another.", "error")
        else:
            # Hash the password before storing it
            hashed_password = hash_password(password)

            login_data[username] = {
                "uid": uid,
                "email": email,
                "password": hashed_password,
                "confirm_password": confirm_password
            }
            with open("login.json", "w") as file:
                json.dump(login_data, file)
            flash("Signup successful. You can now log in.", "success")
            return redirect(url_for("loginDoctor"))

    return render_template("doctorsign.html")





@app.route("/loginPatient", methods=["GET", "POST"])
def patientlogin():
    if request.method == "POST":
        username = request.form["username"]
        uid = request.form["uid"]
        password = request.form["password"]

        if username in login_data and login_data[username]["uid"] == uid:
            # Hash the provided password for comparison
            hashed_password = hash_password(password)

            if login_data[username]["password"] == hashed_password:
                session["logged_in"] = True
                session["username"] = username
                flash("Login successful", "success")
                return redirect(url_for("welcomepatient"))
        flash("Invalid username, uid, or password", "error")

    return render_template("loginPatient.html")



@app.route("/welcomepatient")
def welcomepatient():
    if session.get("logged_in"):
        return render_template('patient.html')
    else:
        return redirect(url_for("loginPatient"))

@app.route("/patientsign", methods=["GET", "POST"])
def patientsign():
    if request.method == "POST":
        username = request.form["username"]
        uid = request.form["uid"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username in login_data:
            flash("Username already exists. Please choose another.", "error")
        else:
            # Hash the password before storing it
            hashed_password = hash_password(password)

            login_data[username] = {
                "uid": uid,
                "email": email,
                "password": hashed_password,
                "confirm_password": confirm_password
            }
            with open("login.json", "w") as file:
                json.dump(login_data, file)
            flash("Signup successful. You can now log in.", "success")
            return redirect(url_for("loginPatient"))

    return render_template("patientsign.html")



@app.route("/loginRepresent", methods=["GET", "POST"])
def representlogin():
    if request.method == "POST":
        username = request.form["username"]
        uid = request.form["uid"]
        password = request.form["password"]

        if username in login_data and login_data[username]["uid"] == uid and login_data[username]["password"] == password:
            session["logged_in"] = True
            session["username"] = username
            flash("Login successful", "success")
            return redirect(url_for("welcomerep"))
        else:
            flash("Invalid username, uid, or password", "error")

    return render_template("loginRepresent.html")


@app.route("/welcomerep")
def welcomerep():
    if session.get("logged_in"):
        return render_template('represent.html')
    else:
        return redirect(url_for("loginRepresent"))


@app.route("/representsign", methods=["GET", "POST"])
def representsign():
    if request.method == "POST":
        username = request.form["username"]
        uid = request.form["uid"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username in login_data:
            flash("Username already exists. Please choose another.", "error")
        else:
            login_data[username] = {
                "uid": uid,
                "email": email,
                "password": password,
                "confirm_password": confirm_password
            }
            with open("login.json", "w") as file:
                json.dump(login_data, file)
            flash("Signup successful. You can now log in.", "success")
            return redirect(url_for("loginRepresent"))

    return render_template("representsign.html")






@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_type = request.args.get("type")  

    if logout_type == "doctor":
        session.pop("logged_in", None)
        session.pop("username", None)
        return redirect(url_for("loginDoctor"))
    elif logout_type == "patient":
        session.pop("logged_in", None)
        session.pop("username", None)
        return redirect(url_for("loginPatient"))
    elif logout_type == "represent":
        session.pop("logged_in", None)
        session.pop("username", None)
        return redirect(url_for("loginRepresent"))



    return "Invalid user type for logout"



@app.route("/logoutRepresent")
def logoutRepresent():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("loginRepresent"))

# OpenAI API Key 
openai.api_key = "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"

def get_completion(prompt): 
	print(prompt) 
	query = openai.Completion.create( 
		engine="text-davinci-003", 
		prompt=prompt, 
		max_tokens=1024, 
		n=1, 
		stop=None, 
		temperature=0.5, 
	) 

	response = query.choices[0].text 
	return response 

@app.route("/bot", methods=['POST', 'GET'])
def query_view():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')  # Use request.form.get to safely retrieve the prompt.

        try:
            response = get_completion(prompt)
            return jsonify({'response': response})
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': 'An error occurred while processing the request.'}, 500)  # Return a 500 Internal Server Error response.

    return render_template('bot.html')



if __name__ == '__main__':
   app.run()