from flask import Flask, render_template, request
import string
from math import gcd
from sympy import mod_inverse

app = Flask(__name__)

def affine_cipher(text, a, b, mode):
    result = ""
    m = len(string.ascii_lowercase)

    if mode == 'decrypt':
        a_inv = mod_inverse(a, m)
    else:
        a_inv = a

    for char in text:
        if char.isalpha():
            alphabet = string.ascii_lowercase if char.islower() else string.ascii_uppercase
            index = alphabet.index(char)
            if mode == 'encrypt':
                encrypted_index = (a * index + b) % m
                result += alphabet[encrypted_index]
            else:
                decrypted_index = (a_inv * (index - b)) % m
                result += alphabet[decrypted_index]
        else:
            result += char

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    output_text = ''
    if request.method == 'POST':
        text = request.form['text']
        a = int(request.form['a'])
        b = int(request.form['b'])
        mode = request.form['mode']

        if text and a and b and gcd(a, len(string.ascii_lowercase)) == 1:
            output_text = affine_cipher(text, a, b, mode)

    return render_template('index.html', output_text=output_text)

if __name__ == '__main__':
    app.run(debug=True)
