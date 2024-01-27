import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import openai
from openai import OpenAI
import os
from flask import Flask, Response
from flask_basicauth import BasicAuth


# Initialize the OpenAI client
client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize Flask server
server = Flask(__name__)
# Configure BasicAuth
server.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME') # Replace with your desired username
server.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')  # Replace with your desired password
#server.config['BASIC_AUTH_FORCE'] = True  # This will force BasicAuth on all routes

basic_auth = BasicAuth(server)

# Initialize Dash app by passing the Flask server
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    html.Div([
        dcc.Textarea(
            id='input_system',
            placeholder="Input your system instructions here",
            style={'width': '100%', 'height': '150px', 'fontSize': 16}
        ),

        dcc.Textarea(
            id='input_user',
            placeholder="Input your user instructions here",
            style={
                'width': '100%',
                'height': '200px',
                'fontSize': 16
            },
        ),

        dcc.Textarea(  # Это уже Textarea, как и нужно
            id='input-text',
            style={'width': '100%', 'height': '200px', 'fontSize': 16}
        ),

        html.Button('Translate', id='translate-button', style={'fontSize': '24px', 'padding': '10px 20px', 'margin': '20px 0'}),

        dcc.Loading(
            id="loading",
            type="default",
            children=html.Div(id='output-translation', style={'width': '100%', 'margin': '20px 0', 'whiteSpace': 'pre-line'})
        )
    ], style={'text-align': 'left', 'margin': 'auto', 'width': '90%'})
])


@app.callback(
Output('output-translation', 'children'),
[Input('translate-button', 'n_clicks')],
[dash.dependencies.State('input_system', 'value'),
dash.dependencies.State('input-text', 'value'),
dash.dependencies.State('input_user', 'value')]
)
def update_output(n_clicks, input_system, input_text, input_user):
    if n_clicks is None:
        return ''
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",

    messages=[
            {"role": "system", "content": input_system},


            {"role": "user", "content": f"{input_text}"},  # Corrected this line
            {"role": "user", "content": input_user}
        ]
                                           )
    #translation = response['choices'][0]['message']['content']
    translation = response.choices[0].message.content


    return translation
if __name__ == '__main__':
    app.run_server(debug=False)
