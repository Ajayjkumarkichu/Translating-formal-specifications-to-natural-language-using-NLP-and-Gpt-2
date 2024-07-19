import re
from nltk.tokenize import word_tokenize
from transformers import pipeline

# Define a dictionary to translate common Dafny symbols and keywords to natural language
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

# Example usage with a Dafny code snippet
dafny_code = """
method Smallest(a: array<int>) returns (minIndex: nat)
    requires a.Length > 0;
    ensures 0 <= minIndex < a.Length;
    ensures forall i | 0 <= i < a.Length :: a[minIndex] <= a[i];
{
    minIndex := 0;
    var i := 1;
    while i < a.Length
        invariant 0 <= i <= a.Length;
        invariant 0 <= minIndex < a.Length;
        invariant forall j | 0 <= j < i :: a[minIndex] <= a[j];
    {
        if a[i] < a[minIndex] {
            minIndex := i;
        }
        i := i + 1;
    }
}
"""

preconditions, postconditions, invariants, assertions, decreases, modifies = extract_specifications(dafny_code)

# Translate all extracted specifications
translated_preconditions = translate_specifications(preconditions, relation_dict)
translated_postconditions = translate_specifications(postconditions, relation_dict)
translated_invariants = translate_specifications(invariants, relation_dict)
translated_assertions = translate_specifications(assertions, relation_dict)
translated_decreases = translate_specifications(decreases, relation_dict)
translated_modifies = translate_specifications(modifies, relation_dict)

generator = pipeline('text-generation', model='gpt2')
explanations = {
    "Preconditions": [get_gpt3_explanation(spec) for spec in translated_preconditions],
    "Postconditions": [get_gpt3_explanation(spec) for spec in translated_postconditions],
    "Invariants": [get_gpt3_explanation(spec) for spec in translated_invariants],
    "Assertions": [get_gpt3_explanation(spec) for spec in translated_assertions],
    "Decreases": [get_gpt3_explanation(spec) for spec in translated_decreases],
    "Modifies": [get_gpt3_explanation(spec) for spec in translated_modifies],
}

for key, value in explanations.items():
    print(f"{key} Explanations:")
    for explanation in value:
        print(f"- {explanation}")
    print()

# Add translated specifications as comments to the original Dafny code
translated_dafny_code = add_comments_to_code(
    dafny_code,
    translated_preconditions,
    translated_postconditions,
    translated_invariants,
    translated_assertions,
    translated_decreases,
    translated_modifies
)

print("Translated Dafny Code with Comments:")
print(translated_dafny_code)
