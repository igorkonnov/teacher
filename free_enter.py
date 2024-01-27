import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import openai
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])







app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Textarea(
            id='input_system',
            placeholder="Input your system instructions here",
            style={'width': '100%', 'height': '150px', 'fontSize': 16}
        ),

        dcc.Textarea(  # Изменено на Textarea для многострочного ввода
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
            # Uncomment the following line if you need to use it
            # {"role": "user", "content": f"use this text to find all relevant information requested by user : {werk}"},
            {"role": "user", "content": f"{input_text}"},  # Corrected this line
            {"role": "user", "content": input_user}
        ]
                                           )
    #translation = response['choices'][0]['message']['content']
    translation = response.choices[0].message.content
    #with open(r"C:\Users\igork\OneDrive\SG\Leube\record_13_11_2023_summary.txt", 'w') as file:
        #file.write(translation + '\n')

    return translation
if __name__ == '__main__':
    app.run_server(debug=True, port=8083)