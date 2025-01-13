from flask import Flask, render_template, request
import os

from datetime import datetime

app = Flask(__name__)


# Ensure the 'images' folder exists
os.makedirs('Details', exist_ok=True)

def check_duplicate(email, phone):
    """
    Check if the email or phone number already exists in any of the saved files.
    Returns True if a duplicate is found, otherwise False.
    """
    for filename in os.listdir('Details'):
        filepath = os.path.join('Details', filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()
            file_email = [line for line in lines if line.startswith("Email:")][0].strip().split(": ")[1]
            file_phone = [line for line in lines if line.startswith("Phone:")][0].strip().split(": ")[1]
            if file_email == email or file_phone == phone:
                return True
    return False

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message = request.form.get('message')
            
            # Validate data
            if not name or not email or not phone:
                return render_template('index.html', error="All fields are required!", success=None)
            
            # Check for duplicates
            if check_duplicate(email, phone):
                return render_template('index.html', error="This email or phone number is already in use.", success=None)
            
            # Generate a unique filename for each submission
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name.replace(' ', '_')}_{timestamp}.txt"
            filepath = os.path.join('Details', filename)
            
            # Save the details to the file
            with open(filepath, 'w') as file:
                file.write(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}\n")
            
            # Return success message
            return render_template('index.html', name=name, email=email, phone=phone, message=message, success="Details saved successfully!")
        
        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {str(e)}", success=None)
    
    return render_template('index.html', name=None, email=None, phone=None, message=None, success=None)

if __name__ == '__main__':
    app.debug = True
    app.run()
