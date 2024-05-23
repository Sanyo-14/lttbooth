from flask import Flask

from forms import CommentForm, AddBehaviourForm

'''
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
'''


#db = SQLAlchemy(app)
#Migrate(app, db)

import sqlite3
import os
from flask import render_template, url_for, flash, redirect, app

from utils import create_databases, add_comment, add_behaviour

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure databases are ready when the app starts
create_databases()

@app.route('/')
def index():
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PathToImage FROM Gallery")
    images = cursor.fetchall()
    conn.close()
    for image in images:
        print(images[0][0])
    return render_template('index.html', images=images)  # Tell


@app.route('/gallery/<image_id>', methods=['GET', 'POST'])
def gallery_description(image_id):
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Gallery WHERE id=?", (image_id,))
    image = cursor.fetchone()

    cursor.execute("SELECT * FROM Comments WHERE gallery_id=?", (image_id,))
    comments = cursor.fetchall()
    conn.close()

    if image is None:
        flash('Gallery image not found!', 'error')
        return redirect(url_for('index'))

    form = CommentForm()
    if form.validate_on_submit():
        add_comment(image[2], form.content.data)  # Pass image name
        flash('Your comment has been added!', 'success')
        return redirect(url_for('gallery_description', image_id=image_id))

    return render_template('gallery_description.html', image=image, comments=comments, form=form)


@app.route('/ab_testing_images')
def ab_testing_images():
    # (Logic for A/B testing images will go here)
    return render_template('ab_testing_images.html')


@app.route('/gallery_leaderboard')
def gallery_leaderboard():
    # (Logic for gallery leaderboard will go here)
    return render_template('gallery_leaderboard.html')


@app.route('/ab_testing_behaviours', methods=['GET', 'POST'])
def ab_testing_behaviours():
    form = AddBehaviourForm()
    if form.validate_on_submit():
        add_behaviour(form.name.data)
        flash('Behaviour added!', 'success')
        return redirect(url_for('ab_testing_behaviours'))
    return render_template('ab_testing_behaviours.html', form=form)


@app.route('/behaviour_leaderboard')
def behaviour_leaderboard():
    # (Logic for behaviour leaderboard will go here)
    return render_template('behaviour_leaderboard.html')

if __name__ == '__main__':
    app.run(debug=True)