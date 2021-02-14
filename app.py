import dash
import dash_bootstrap_components as dbc
import dash_auth


USERNAME_PASSWORD_PAIRS = [['karli', 'boi']]

external_stylesheets =[dbc.themes.SIMPLEX]#, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']#,,dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = "GE Application"
