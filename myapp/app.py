from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired
import pandas as pd
from supervised.automl import AutoML
import os
import shutil

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


@app.route('/', methods=['GET', 'POST'])
def home():
    form = DataUploadForm()
    if form.validate_on_submit():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], form.file.data.filename)
        form.file.data.save(filepath)

        return redirect(url_for('train_model', filepath=filepath))
    return render_template('home.html', form=form)


@app.route('/train', methods=['GET', 'POST'])
def train_model():
    filepath = request.args.get('filepath')
    form = ModelTrainingForm()
    if form.validate_on_submit():
        df = pd.read_csv(filepath)
        automl = AutoML(mode=form.mode.data, algorithms=form.algorithms.data.split(','),
                        total_time_limit=int(form.time_limit.data))
        automl.fit(df[form.x_columns.data.split(',')], df[form.y_column.data])

        # Store results for downloading (if needed)
        # ... (similar to your previous code)

        return render_template('results.html', automl=automl)
    return render_template('train.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
