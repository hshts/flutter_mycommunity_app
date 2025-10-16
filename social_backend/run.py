import os
from api import create_app, db
from api.models import Activity

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Activity': Activity}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)