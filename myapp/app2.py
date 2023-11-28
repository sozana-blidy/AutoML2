from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired
import pandas as pd
from supervised.automl import AutoML
import os
import shutil
import BeautifulSoup
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = './uploads'


class DataUploadForm(FlaskForm):
    file = FileField('Upload CSV with training data', validators=[DataRequired()])
    submit = SubmitField('Upload and Proceed')


class ModelTrainingForm(FlaskForm):
    x_columns = StringField('Input features (comma-separated)', validators=[DataRequired()])
    y_column = StringField('Target column', validators=[DataRequired()])
    mode = SelectField('AutoML Mode', choices=[('Explain', 'Explain'), ('Perform', 'Perform'), ('Compete', 'Compete')])
    algorithms = StringField('Algorithms (comma-separated)', validators=[DataRequired()])
    time_limit = SelectField('Time limit (seconds)',
                            choices=[('60', '60'), ('120', '120'), ('240', '240'), ('300', '300')])
    submit = SubmitField('Start Training')

allowed_usernames = ['hassan', 'obai', 'sozana','laith','madeleine']
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    
    if username in allowed_usernames and password == '1234':

        return redirect('/home')
    else:
        error_message = 'error'
        if request.method == 'POST':
                if 'reset' in request.form:
                        return redirect('/home')
        error_message = 'The user name or password is incorrect'
        flash(error_message)

        return render_template('login.html', error_message=error_message)
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = DataUploadForm()
    if form.validate_on_submit():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], form.file.data.filename)
        form.file.data.save(filepath)
        
    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect('/home')
        return redirect(url_for('train_model', filepath= filepath))
    return render_template('home.html', form=form)




@app.route('/train', methods=['GET', 'POST'])
def train_model():

    filepath = request.args.get('filepath')
    form = ModelTrainingForm()
    
    if form.validate_on_submit():
        df = pd.read_csv(filepath)
        algorithms = form.algorithms.data.split(',')
        x_columns = form.x_columns.data.split(',')
        y_column = form.y_column.data
        automl = AutoML(mode=form.mode.data, algorithms=algorithms,
                            total_time_limit=int(form.time_limit.data))
        automl.fit(df[x_columns], df[y_column])

        html_content_data = automl.report().data
        soup = BeautifulSoup(html_content_data, 'html.parser')
        image_src_to_remove = "https://raw.githubusercontent.com/mljar/visual-identity/main/media/mljar_AutomatedML.png"
        image_tags_to_remove = soup.find_all('img', src=image_src_to_remove)
        for img_tag in image_tags_to_remove:
            img_tag.extract() 
        # Get the edited HTML  
        edited_html_content = str(soup)

        return render_template('results.html', automl=automl, edited_html_content=edited_html_content)
    return render_template('train.html', form=form)
 

 
if __name__ == "__main__":
    app.run(debug=True) 
