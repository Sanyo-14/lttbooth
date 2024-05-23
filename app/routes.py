from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import GalleryImage, Behaviour, Comment
from app.forms import CommentForm, AddBehaviourForm

@app.route('/')
def index():
    images = GalleryImage.query.all()
    return render_template('index.html', images=images)

@app.route('/gallery/<image_name>', methods=['GET', 'POST'])
def gallery_description(image_name):
    image = GalleryImage.query.filter_by(name=image_name).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, image=image)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('gallery_description', image_name=image_name))
    return render_template('gallery_description.html', image=image, form=form)

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
        behaviour = Behaviour(name=form.name.data)
        db.session.add(behaviour)
        db.session.commit()
        flash('Behaviour added!', 'success')
        return redirect(url_for('ab_testing_behaviours'))
    return render_template('ab_testing_behaviours.html', form=form)

@app.route('/behaviour_leaderboard')
def behaviour_leaderboard():
    # (Logic for behaviour leaderboard will go here)
    return render_template('behaviour_leaderboard.html')