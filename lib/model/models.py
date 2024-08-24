from lib.config import db


class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), nullable=False)
    length = db.Column(db.Float, nullable=False)
    diameter = db.Column(db.Float, nullable=False)
    non_local_param = db.Column(db.Float, nullable=False)
    linear_foundation = db.Column(db.Float, nullable=False)
    non_linear_foundation = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    velocity = db.Column(db.Float, nullable=False)
    initial_disp = db.Column(db.Float, nullable=False)
    data_3d = db.Column(db.JSON, nullable=False)
    data_2d = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<Prediction {self.user_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "length": self.length,
            "diameter": self.diameter,
            "non_local_param": self.non_local_param,
            "linear_foundation": self.linear_foundation,
            "non_linear_foundation": self.non_linear_foundation,
            "temperature": self.temperature,
            "velocity": self.velocity,
            "initial_disp": self.initial_disp,
            "data_3d": self.data_3d,
            "data_2d": self.data_2d
        }
