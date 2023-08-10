from flask import Flask, render_template, request, jsonify, redirect

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 
from wtforms.validators import InputRequired
import firebase_admin
from firebase_admin import credentials, storage, firestore, initialize_app


# FIREBASE 
cred = credentials.Certificate("key.json") 

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
# objects to perform CRUD operations on resumes collection
default_app = initialize_app(cred, {'storageBucket': 'skillscan-4d57e.appspot.com'})
db = firestore.client() # allows you to read and write data 
resumes_ref = db.collection('resumes') # creating a ref to resume collection in the Firestore database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/resumes'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File") # Submit Button 

 # SUBMIT TO FIREBASE 
@app.route('/add', methods=['POST'])
def create():
    """  
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try: 
        id = request.json['id']
        resumes_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e: 
        return f"An Error Ocurred: {e}"

# Input field and submit field 
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")        

# LINKS
@app.route('/',methods=['GET', 'POST']) # the root URL can handle GET and POST

# returns HTML file for webpage 
@app.route('/home',methods=['GET', 'POST'])
def home(): 
    form = UploadFileForm()
    if form.validate_on_submit(): # once you submit 
        file = form.file.data # get the file or the resume uploades 
        uploadResume(file) # upload to firebase
            # could save file locally here
        
        return redirect("/submitted")
    return render_template('index.html', form=form)
       
# Upload function to firebase 
def uploadResume(file): 
    path = '/resumes/'+str(secure_filename(file.filename))
    if file:
        try:
            bucket = storage.bucket()
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
        except Exception as e: 
            print('error uploadinf user photo: ' % e)

# Submitted  Redirect 
@app.route('/submitted', methods=['GET', 'POST'])
def submitted():
    return render_template('submitted.html')

@app.errorhandler(404)
def invalid_route(e):
    return "Invalid Route"
    
if __name__ == '__main__':
        app.run(debug=True)
