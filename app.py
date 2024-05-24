from flask import Flask, jsonify

from forms import CommentForm, AddBehaviourForm
import sqlite3
import os
from flask import render_template, url_for, flash, redirect, app, request

from utils import create_databases, add_comment, add_behaviour, update_gallery_elo_wins, update_behaviour_elo_wins, \
    get_gallery_elo_wins, get_behaviour_elo_wins, get_gallery_leaderboard, get_behaviour_leaderboard, get_random_items, \
    calculate_elo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Ensure databases are ready when the app starts
create_databases()


@app.route('/')
def index():
    conn = sqlite3.connect('treehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PathToImage FROM Gallery") # Select both id and PathToImage
    images = cursor.fetchall()
    conn.close()
    return render_template('index.html', images=images) 


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
    item1, item2 = get_random_items('Gallery')
    return render_template('ab_testing_images.html', item1=item1, item2=item2)

@app.route('/ab_testing_images_choose/<choice>')
def ab_testing_images_choose(choice):
    item1_name = request.args.get('item1_name')
    item2_name = request.args.get('item2_name')

    # Retrieve data using functions from utils.py
    item1_elo, item1_wins = get_gallery_elo_wins(item1_name)
    item2_elo, item2_wins = get_gallery_elo_wins(item2_name)

    # Determine winner and update wins
    if choice == 'item1':
        item1_wins += 1
        result = 1
    else:
        item2_wins += 1
        result = 0

    # Calculate new ELO scores
    item1_new_elo, item2_new_elo = calculate_elo(item1_elo, item2_elo, result)

    # Update database using functions from utils.py
    update_gallery_elo_wins(item1_name, item1_new_elo, item1_wins)
    update_gallery_elo_wins(item2_name, item2_new_elo, item2_wins)

    return redirect(url_for('ab_testing_images'))


@app.route('/gallery_leaderboard')
def gallery_leaderboard():
    leaderboard = get_gallery_leaderboard()
    return render_template('gallery_leaderboard.html', leaderboard=leaderboard)


@app.route('/ab_testing_behaviours', methods=['GET', 'POST'])
def ab_testing_behaviours():
    form = AddBehaviourForm()
    behaviour1, behaviour2 = get_random_items('Behaviour')

    if request.method == 'POST':
        if 'choice' in request.form:
            # Handle A/B testing choice
            choice = request.form['choice']

            # Get ELO and Wins from the database for both behaviours
            behaviour1_elo, behaviour1_wins = get_behaviour_elo_wins(behaviour1)
            behaviour2_elo, behaviour2_wins = get_behaviour_elo_wins(behaviour2)

            if choice == 'behaviour1':
                behaviour1_wins += 1
                result = 1  # Behaviour 1 won
            else:
                behaviour2_wins += 1
                result = 0  # Behaviour 2 won

            # Calculate the new ELO scores
            behaviour1_new_elo, behaviour2_new_elo = calculate_elo(behaviour1_elo, behaviour2_elo, result)

            # Update the database with the new ELO scores and win counts
            update_behaviour_elo_wins(behaviour1, behaviour1_new_elo, behaviour1_wins)
            update_behaviour_elo_wins(behaviour2, behaviour2_new_elo, behaviour2_wins)

            flash('ELO ratings updated!', 'success')
            return redirect(url_for('ab_testing_behaviours'))

        elif 'action' in request.form and request.form['action'] == 'add_behavior':
            # Handle new behavior form submission
            if form.validate_on_submit():
                add_behaviour(form.name.data)
                flash('Behaviour added!', 'success')
                return redirect(url_for('ab_testing_behaviours'))

    return render_template('ab_testing_behaviours.html',
                           behaviour1=behaviour1,
                           behaviour2=behaviour2,
                           form=form)


@app.route('/behaviour_leaderboard')
def behaviour_leaderboard():
    leaderboard = get_behaviour_leaderboard()
    return render_template('behaviour_leaderboard.html', leaderboard=leaderboard)


if __name__ == '__main__':
    app.run(debug=True)