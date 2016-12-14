from API.app import db
#import API.app

class Metadata(db.Model):
    __tablename__='Metadata'

    id = db.Column(db.Integer, primary_key=True)
    mean = db.Column(db.Float)
    std = db.Column(db.Float)#nullable=Flase
    blarg = db.Column(db.Float)
    level = db.Column(db.String(1))
    #fpath = db.Column(db.String(80), nullable=False)???

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_dict(self):
        return dict(id=self.id, 
                    blarg=self.blarg, 
                    level=self.level, 
                    mean=self.mean, 
                    std=self.std)#, 
                    #fpath=self.fpath)

    # def __init__(self, meta):
    #     self.id = meta[0]
    #     self.mean = meta[1]
    #     self.std = meta[2]
    #     self.blarg = meta[3]
    #     self.level = meta[4]
