import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import random
import base64

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
    }
}

# Load and encode the background image
def encode_image(image_path):
    try:
        with open(image_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        return None

background_image = encode_image('image.png')

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

# Create background style with logo
background_style = {
    'minHeight': '100vh',
    'backgroundImage': f'url({background_image})' if background_image else 'none',
    'backgroundSize': 'cover',
    'backgroundPosition': 'center',
    'backgroundRepeat': 'no-repeat',
    'position': 'relative'
}

app.layout = html.Div(style=background_style, children=[
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1([
                    "Databricks Multi Language Agent ",
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
                    ])
                ], className="text-center mb-4 mt-4", style={'color': '#FF3621', 'fontWeight': 'bold'}),
                html.P("Type anything - 50% chance it transforms into a random language!",
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
                            'backgroundColor': 'rgba(248, 249, 250, 0.9)'
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
                                color='danger',
                                n_clicks=0
                            ),
                        ]),
                    ])
                ], style={'backgroundColor': 'rgba(255, 255, 255, 0.95)'})
            ], width=8)
        ], justify='center'),

        # Store for chat messages
        dcc.Store(id='messages-store', data=[]),

    ], fluid=True, style={'paddingBottom': '100px'}),

    # Databricks logo in bottom right
    html.Div([
        html.Img(src=background_image, style={
            'height': '60px',
            'opacity': '0.8'
        })
    ], style={
        'position': 'fixed',
        'bottom': '20px',
        'right': '20px',
        'zIndex': '1000'
    })
])

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
        # 50% chance to convert to random script
        should_convert = random.random() < 0.5

        if should_convert:
            # Convert user message to random script
            converted_text, language_name = convert_to_random_script(user_message)

            # Add converted user message
            messages.append({
                'role': 'user',
                'content': converted_text,
                'original': user_message,
                'converted': True
            })

            # Generate bot response
            bot_response = f"Sorry, I don't understand {language_name}"
            messages.append({
                'role': 'bot',
                'content': bot_response
            })
        else:
            # Keep original message
            messages.append({
                'role': 'user',
                'content': user_message,
                'converted': False
            })

            # Bot responds normally
            bot_response = "I understand you! How can I help?"
            messages.append({
                'role': 'bot',
                'content': bot_response
            })

    # Create chat display
    chat_elements = []
    for msg in messages:
        if msg['role'] == 'user':
            if msg.get('converted'):
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
                        html.Strong('You: '),
                        html.Span(msg['content'])
                    ], style={'marginBottom': '15px', 'color': '#0066cc'})
                )
        else:
            chat_elements.append(
                html.Div([
                    html.Strong('Bot: '),
                    html.Span(msg['content'])
                ], style={'marginBottom': '15px', 'color': '#FF3621', 'fontWeight': 'bold'})
            )

    return chat_elements, messages, ''

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
