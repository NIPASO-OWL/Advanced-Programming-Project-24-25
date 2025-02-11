from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
import pandas as pd
from process_file import process_file, motif_search, align_sequences

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

#define classes for user input
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

class MotifSearchForm(FlaskForm):
    motif = StringField("Motif", validators=[InputRequired()])
    submit = SubmitField("Search Motif")

class PairwiseAlignmentForm(FlaskForm):
    seq_id1 = StringField("Sequence ID 1", validators=[InputRequired()])
    seq_id2 = StringField("Sequence ID 2", validators=[InputRequired()])
    submit = SubmitField("Align Sequences")

#flask application
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_path)
        df = process_file(file_path)
        session['data'] = file_path
        return render_template('dataframe.html', data=df.to_html(classes='table table-striped'))
    return render_template('home.html', form=form)

@app.route('/motif_search', methods=['GET', 'POST'])
def motif_search_route():
    form = MotifSearchForm()

    if form.validate_on_submit():
        motif = form.motif.data
        df = process_file(session['data'])
        result = motif_search(motif, df)
        return render_template('result.html', result=result.to_html(classes='table table-striped'))
    return render_template('motif_search.html', form=form)

@app.route('/pairwise_alignment', methods=['GET', 'POST'])
def pairwise_alignment_route():
    form = PairwiseAlignmentForm()
    if form.validate_on_submit():
        seq_id1 = form.seq_id1.data
        seq_id2 = form.seq_id2.data
        df = process_file(session['data'])
        aln, aln_score = align_sequences(seq_id1, seq_id2, df)
        result = f"Alignment:<br>{aln}<br>Alignment Score: {aln_score}"
        return render_template('result.html', result=result.replace('\n', '<br>'))
    return render_template('pairwise_alignment.html', form=form)

@app.route('/back_to_dataframe', methods=['GET'])
def back_to_dataframe():
    df = process_file(session['data'])
    return render_template('dataframe.html', data=df.to_html(classes='table table-striped'))

if __name__ == "__main__":
    app.run(debug=True)