import sqlalchemy as sa
import sqlalchemy.orm as so
from app import MyApp, MyDb
from app.models import Utilisateur

@MyApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': MyDb, 'User': Utilisateur}

if __name__ == '__main__':
   MyApp.run(debug=True)
