from app import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Disease(db.Model):
    __tablename__ = 'disease'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', foreign_keys=category_id)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class PeopleCategory(db.Model):
    __tablename__ = 'people_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)



class DiseaseCategory(db.Model):
    __tablename__ = 'disease_category'

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('people_category.id'))

    def __repr__(self):
        return '<id {}>'.format(self.id)


class DiseaseStage(db.Model):
    __tablename__ = 'disease_stage'

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Stage(db.Model):
    __tablename__ = 'stage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)



class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    form = db.Column(db.String)
    disease_stage_id = db.Column(db.Integer, db.ForeignKey('disease_stage.id'))
    disease_stage = db.relationship('DiseaseStage', foreign_keys=disease_stage_id)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
