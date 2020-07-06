from . import app
from .view import PaymentView

app.add_url_rule('/', view_func=PaymentView.as_view('payment_view'))
