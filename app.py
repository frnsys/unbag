import config
import random
import sentry_sdk
from taozi import create_app
from taozi.models import Issue
from unbag.routes import bp
from flask_konbini import Konbini
from sentry_sdk.integrations.flask import FlaskIntegration

app = create_app(config, name='unbag', blueprints=[bp])
Konbini(app)

if not app.debug:
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration()]
    )

@app.context_processor
def inject_issues():
    """Inject issues into all templates"""
    issues = Issue.query.filter(Issue.name!='Programs', Issue.published).order_by(Issue.id.desc()).all()
    return dict(issues=issues,
                get_products=app.get_products,
                get_plans=app.get_plans)

@app.template_filter('shuffle')
def filter_shuffle(seq):
    result = list(seq)
    random.shuffle(result)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
