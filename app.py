from api import create_app, cli, db
from api.models import User, Product, Merchant

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Merchant': Merchant, 'Product': Product}
