import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Language configurations with their writing systems
LANGUAGES = {
    'chinese': {
        'name': 'Chinese',
        'flag': '🇨🇳',
        'chars': '汉字文本转换示例这是一个测试消息请输入您的问题我们会尽快回复您感谢使用本系统'
    },
    'japanese': {
        'name': 'Japanese',
        'flag': '🇯🇵',
        'chars': 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
    },
    'korean': {
        'name': 'Korean',
        'flag': '🇰🇷',
        'chars': '가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허고노도로모보소오조초코토포호'
    },
    'russian': {
        'name': 'Russian',
        'flag': '🇷🇺',
        'chars': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    },
    'greek': {
        'name': 'Greek',
        'flag': '🇬🇷',
        'chars': 'αβγδεζηθικλμνξοπρστυφχψω'
    },
    'georgian': {
        'name': 'Georgian',
        'flag': '🇬🇪',
        'chars': 'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
    },
    'arabic': {
        'name': 'Arabic',
        'flag': '🇸🇦',
        'chars': 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'
    },
    'thai': {
        'name': 'Thai',
        'flag': '🇹🇭',
        'chars': 'กขคฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ'
    },
    'hindi': {
        'name': 'Hindi',
        'flag': '🇮🇳',
        'chars': 'अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह'
    },
    'farsi': {
        'name': 'Farsi',
        'flag': '🇮🇷',
        'chars': 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    },
    'romance': {
        'name': 'Romance',
        'flag': '🇫🇷',
        'chars': 'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    }
}

def convert_to_random_script(text):
    """Convert text to a random script from the available languages"""
    language_key = random.choice(list(LANGUAGES.keys()))
    language = LANGUAGES[language_key]
    chars = language['chars']

    # Convert each character to a random character from the chosen script
    converted = ''
    for char in text:
        if char.isalnum() or char.isspace():
            if char.isspace():
                converted += ' '
            else:
                converted += random.choice(chars)
        else:
            converted += char

    return converted, language['name']

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1([
                "Multi-Language Assistant ",
                html.Span([
                    LANGUAGES['chinese']['flag'],
                    LANGUAGES['japanese']['flag'],
                    LANGUAGES['korean']['flag'],
                    LANGUAGES['russian']['flag'],
                    LANGUAGES['greek']['flag'],
                    LANGUAGES['georgian']['flag'],
                    LANGUAGES['arabic']['flag'],
                    LANGUAGES['thai']['flag'],
                    LANGUAGES['hindi']['flag'],
                    LANGUAGES['farsi']['flag'],
                    LANGUAGES['romance']['flag'],
                ])
            ], className="text-center mb-4 mt-4"),
            html.P("Type anything and watch it transform into random languages!",
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
                            placeholder='Type your message...',
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
        # Convert user message to random script
        converted_text, language_name = convert_to_random_script(user_message)

        # Add converted user message
        messages.append({
            'role': 'user',
            'content': converted_text,
            'original': user_message
        })

        # Generate bot response
        bot_response = f"Sorry, I don't understand {language_name}"
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
                    html.Span(msg['content'], style={'fontSize': '18px'}),
                    html.Br(),
                    html.Small(f"(Original: {msg.get('original', '')})",
                              style={'color': '#999'})
                ], style={'marginBottom': '15px', 'color': '#0066cc'})
            )
        else:
            chat_elements.append(
                html.Div([
                    html.Strong('Bot: '),
                    html.Span(msg['content'])
                ], style={'marginBottom': '15px', 'color': '#cc0000', 'fontWeight': 'bold'})
            )

    return chat_elements, messages, ''

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
