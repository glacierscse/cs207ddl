from API.app import db

class Metadata(db.Model):
    """This is the metadata class implemented using Python.
    The metadata class store the index, mean, std, level and blarg
    of a timeseries.

    Implements: 
        db.Model

    Attributes:
        id: the index of the timeseries
        blarg: a random generated values on [0,1] drawn from a Uniform distribution
        level: a random generated level on [A, B, C, D, E, F].
        mean: mean of the timeseries
        std: standard deviation of the timeseries

    Methods:
        __repr__: The function to return formal string representation of metadata.
        to_dict: The funcction to transform a set of fields into a dictionary.
    """

    __tablename__='Metadata'

    id = db.Column(db.Integer, primary_key=True)
    mean = db.Column(db.Float)
    std = db.Column(db.Float)
    blarg = db.Column(db.Float)
    level = db.Column(db.String(1))

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_dict(self):
        return dict(id=self.id, 
                    blarg=self.blarg, 
                    level=self.level, 
                    mean=self.mean, 
                    std=self.std)


