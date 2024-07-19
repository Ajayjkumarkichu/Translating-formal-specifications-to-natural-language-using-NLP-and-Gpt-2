from flask import Flask, request, render_template, redirect, url_for, session
import re
from transformers import pipeline
from nltk.tokenize import word_tokenize

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Hardcoded users for simplicity
users = {
    'ajay': 'Amrita@123',
    'user2': 'password2'
}

relation_dict = {
    '==': 'is equal to',
    '!=': 'is not equal to',
    '>': 'is greater than',
    '<': 'is less than',
    '>=': 'is greater than or equal to',
    '<=': 'is less than or equal to',
    '*': 'multiplied by',
    '+': 'plus',
    '||': 'or',
    '&&': 'and',
    '&': 'and',
    '!': 'not',
    'forall': 'for all',
    'exists': 'there exists',
    'implies': 'implies',
    'true': 'true',
    'false': 'false',
    'in': 'in',
    'mod': 'modulus',
    '/': 'divided by',
    'Length': 'length of'
}

def extract_specifications(dafny_code):
    preconditions = re.findall(r'requires\s+(.+?);', dafny_code, re.DOTALL)
    postconditions = re.findall(r'ensures\s+(.+?);', dafny_code, re.DOTALL)
    invariants = re.findall(r'invariant\s+(.+?);', dafny_code, re.DOTALL)
    assertions = re.findall(r'assert\s+(.+?);', dafny_code, re.DOTALL)
    decreases = re.findall(r'decreases\s+(.+?);', dafny_code, re.DOTALL)
    modifies = re.findall(r'modifies\s+(.+?);', dafny_code, re.DOTALL)

    preconditions = [' '.join(spec.split()) for spec in preconditions]
    postconditions = [' '.join(spec.split()) for spec in postconditions]
    invariants = [' '.join(spec.split()) for spec in invariants]
    assertions = [' '.join(spec.split()) for spec in assertions]
    decreases = [' '.join(spec.split()) for spec in decreases]
    modifies = [' '.join(spec.split()) for spec in modifies]

    return preconditions, postconditions, invariants, assertions, decreases, modifies

def translate_specification(specification, relation_dict):
    def replace_token(match):
        token = match.group(1)
        return f'size of {token}'

    pattern = r'\|(\w+)\|'
    translated_text = re.sub(pattern, replace_token, specification)

    tokens = word_tokenize(translated_text)
    translated_tokens = []
    inside_parentheses = False

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            inside_parentheses = True
        elif token == ')':
            inside_parentheses = False

        if token in ['&&', '&', '& &']:
            if translated_tokens and translated_tokens[-1] != 'and':
                translated_tokens.append('and')
        elif token in relation_dict and not inside_parentheses:
            translated_tokens.append(relation_dict[token])
        else:
            translated_tokens.append(token)
        i += 1

    return ' '.join(translated_tokens)

# Initialize the text generation pipeline
generator = pipeline('text-generation', model='gpt2')

def get_gpt3_explanation(text):
    response = generator(f"Explain the following Dafny specification in detail: {text}.", max_length=150, num_return_sequences=1, truncation=True)
    explanation = response[0]['generated_text'].strip()
    return explanation

def translate_specifications(specifications, relation_dict):
    return [translate_specification(spec, relation_dict) for spec in specifications]

def add_comments_to_code(dafny_code, preconditions, postconditions, invariants, assertions, decreases, modifies):
    code_lines = dafny_code.split('\n')
    translated_code_lines = []

    for line in code_lines:
        stripped_line = line.strip()

        if stripped_line.startswith('requires') and preconditions:
            translated_code_lines.append(f'// {translate_specification(preconditions.pop(0), relation_dict)}')
            translated_code_lines.append(line)
        elif stripped_line.startswith('ensures') and postconditions:
            translated_code_lines.append(f'// {translate_specification(postconditions.pop(0), relation_dict)}')
            translated_code_lines.append(line)
        elif stripped_line.startswith('invariant') and invariants:
            translated_code_lines.append(f'// {translate_specification(invariants.pop(0), relation_dict)}')
            translated_code_lines.append(line)
        elif stripped_line.startswith('assert') and assertions:
            translated_code_lines.append(f'// {translate_specification(assertions.pop(0), relation_dict)}')
            translated_code_lines.append(line)
        elif stripped_line.startswith('decreases') and decreases:
            translated_code_lines.append(f'// {translate_specification(decreases.pop(0), relation_dict)}')
            translated_code_lines.append(line)
        elif stripped_line.startswith('modifies') and modifies:
            translated_code_lines.append(f'// {translate_specification(modifies.pop(0), relation_dict)}')
            translated_code_lines.append(line)
        else:
            translated_code_lines.append(line)

    return '\n'.join(translated_code_lines)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('translate'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('translate'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/translate', methods=['GET', 'POST'])


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        dafny_code = request.form['dafnyCode']
        preconditions, postconditions, invariants, assertions, decreases, modifies = extract_specifications(dafny_code)

        translated_preconditions = translate_specifications(preconditions, relation_dict)
        translated_postconditions = translate_specifications(postconditions, relation_dict)
        translated_invariants = translate_specifications(invariants, relation_dict)
        translated_assertions = translate_specifications(assertions, relation_dict)
        translated_decreases = translate_specifications(decreases, relation_dict)
        translated_modifies = translate_specifications(modifies, relation_dict)

        explanations = {
            "Preconditions": [get_gpt3_explanation(spec) for spec in translated_preconditions],
            "Postconditions": [get_gpt3_explanation(spec) for spec in translated_postconditions],
            "Invariants": [get_gpt3_explanation(spec) for spec in translated_invariants],
            "Assertions": [get_gpt3_explanation(spec) for spec in translated_assertions],
            "Decreases": [get_gpt3_explanation(spec) for spec in translated_decreases],
            "Modifies": [get_gpt3_explanation(spec) for spec in translated_modifies],
        }

        translated_dafny_code = add_comments_to_code(dafny_code, preconditions, postconditions, invariants, assertions,
                                                     decreases, modifies)

        return render_template('result2.html', translated_code=translated_dafny_code, explanations=explanations)

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
