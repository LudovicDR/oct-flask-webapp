from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import MyDb, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Utilisateur(UserMixin, MyDb.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    prenom: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<Utilisateur : {}>'.format(self.prenom)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return MyDb.session.get(Utilisateur, int(id))
