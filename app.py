import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Polish curse words and insults (keeping it somewhat tame)
POLISH_CURSES = [
    "Cholera jasna!",
    "Do diabła z tym!",
    "Kurczę blade!",
    "Psiakrew!",
    "Niech to szlag!",
    "Do licha!",
    "Kuźwa!",
    "Jejku!",
    "O kurcze!",
    "Jezu!",
]

POLISH_INSULTS = [
    "Ty baranie!",
    "Głupi jesteś?!",
    "Co ty chrzanisz?!",
    "Przestań gadać bzdury!",
    "Daj spokój z tym!",
    "Idioto!",
    "Ty cieniasie!",
    "Kretynie!",
    "Co ty pleciesz?!",
    "Oszalałeś?!",
]

def generate_cursed_response(user_message):
    """Generate a response that curses in Polish"""
    curse = random.choice(POLISH_CURSES)
    insult = random.choice(POLISH_INSULTS)

    responses = [
        f"{curse} {insult} {user_message}? Serio?!",
        f"{insult} {curse} Znowu z tym przychodzisz!",
        f"{curse} {user_message}?! {insult}",
        f"{insult} {curse} Nie mam czasu na takie pytania!",
        f"{curse} Co za głupie pytanie! {insult}",
        f"{insult} {user_message}?! {curse} Daj mi spokój!",
    ]

    return random.choice(responses)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Polish Cursing Chatbot", className="text-center mb-4 mt-4"),
            html.P("Ask me anything and I'll curse at you in Polish! 🇵🇱",
                   className="text-center text-muted mb-4"),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='chat-history', style={
                        'height': '400px',
                        'overflowY': 'auto',
                        'border': '1px solid #ddd',
                        'padding': '10px',
                        'marginBottom': '10px',
                        'backgroundColor': '#f8f9fa'
                    }),

                    dbc.InputGroup([
                        dbc.Input(
                            id='user-input',
                            type='text',
                            placeholder='Type something...',
                            style={'marginRight': '10px'}
                        ),
                        dbc.Button(
                            'Send',
                            id='send-button',
                            color='primary',
                            n_clicks=0
                        ),
                    ]),
                ])
            ])
        ], width=8)
    ], justify='center'),

    # Store for chat messages
    dcc.Store(id='messages-store', data=[]),

], fluid=True)

@app.callback(
    [Output('chat-history', 'children'),
     Output('messages-store', 'data'),
     Output('user-input', 'value')],
    [Input('send-button', 'n_clicks')],
    [State('user-input', 'value'),
     State('messages-store', 'data')]
)
def update_chat(n_clicks, user_message, messages):
    if n_clicks > 0 and user_message:
        # Add user message
        messages.append({
            'role': 'user',
            'content': user_message
        })

        # Generate cursed response
        bot_response = generate_cursed_response(user_message)
        messages.append({
            'role': 'bot',
            'content': bot_response
        })

    # Create chat display
    chat_elements = []
    for msg in messages:
        if msg['role'] == 'user':
            chat_elements.append(
                html.Div([
                    html.Strong('You: '),
                    html.Span(msg['content'])
                ], style={'marginBottom': '10px', 'color': '#0066cc'})
            )
        else:
            chat_elements.append(
                html.Div([
                    html.Strong('Bot: '),
                    html.Span(msg['content'])
                ], style={'marginBottom': '10px', 'color': '#cc0000', 'fontWeight': 'bold'})
            )

    return chat_elements, messages, ''

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
