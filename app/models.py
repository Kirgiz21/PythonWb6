from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

from app import db, login_manager

procedure_procedure_type = db.Table('procedure_procedure_type',
                                    db.Column('procedure_id', db.Integer(), db.ForeignKey('procedure.pk')),
                                    db.Column('procedure_type_id', db.Integer(), db.ForeignKey('procedure_type.pk'))
                                    )


class ProcedureType(db.Model):
    __tablename__ = 'procedure_type'
    pk = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    details = db.Column(db.Text(), nullable=False)
    procedures = db.relationship('Procedure', secondary=procedure_procedure_type, back_populates='procedure_types')
    created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return self.name


class Procedure(db.Model):
    __tablename__ = 'procedure'
    pk = db.Column(db.Integer(), primary_key=True)
    date_time = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.pk'))
    doctor_id = db.Column(db.Integer(), db.ForeignKey('doctor.pk'))
    procedure_types = db.relationship('ProcedureType', secondary=procedure_procedure_type, back_populates='procedures')
    status = db.Column(db.String(20), default='Заплановано')
    details = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return ('Процедура: {}, {}, Дата та час: {}'
                .format(self.user, self.doctor, self.date_time))


class Doctor(db.Model):
    __tablename__ = 'doctor'
    pk = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    procedures = db.relationship('Procedure', backref='doctor')
    created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return ('{} {} {}'
                .format(self.last_name, self.first_name, self.middle_name))


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    pk = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    procedures = db.relationship('Procedure', backref='user')
    role_id = db.Column(db.Integer(), db.ForeignKey('role.pk'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def get_id(self):
        return str(self.pk)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return ('{} {} {}'
                .format(self.last_name, self.first_name, self.middle_name))


class Role(db.Model):
    __tablename__ = 'role'
    pk = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return self.name
