from .database import db


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    email = db.Column(db.String(255))
    text = db.Column(db.Text)
    work = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<feedback %r>' % self.name


if __name__ == '__main__':
    db.create_all()
