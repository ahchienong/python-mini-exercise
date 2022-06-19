# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
from layouts import sidebar

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div(
    children=[
        html.Link(
            rel='stylesheet',
            href='/assets/custom.css'
        ),
        html.A(
            href='/' ,
            children=[html.Img(
                    src = app.get_asset_url('logo-slogan.png'),
                    height = '60 px',
                    width = 'auto')
            ],
            title='Back to Home Page'
        ),
        sidebar(),
        dash.page_container,
        # generate_kijang_emas()
    ], style = {'margin':'30px'})


@app.server.route('/assets/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(static_folder, path)

if __name__ == '__main__':
    app.run_server(debug=True)