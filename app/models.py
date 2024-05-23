from app import db

class Behaviour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    elo = db.Column(db.Integer, default=1000)
    wins = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Behaviour('{self.name}', ELO: {self.elo}, Wins: {self.wins})"

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    comments = db.relationship('Comment', backref='image', lazy=True)
    elo = db.Column(db.Integer, default=1000)
    wins = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"GalleryImage('{self.name}', Path: '{self.path}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('gallery_image.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}')"