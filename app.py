from flask import Flask, render_template, request, redirect, url_for
from itertools import permutations
import nltk

# Download NLTK words corpus if not already downloaded
nltk.download('words')
from nltk.corpus import words

app = Flask(__name__)

# Load the list of valid words
dictionary = set(word.lower() for word in words.words())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_letters = request.form.get("num_letters")
        if num_letters.isdigit() and int(num_letters) > 0:
            return redirect(url_for("letters_input", num_letters=int(num_letters)))
    return render_template("index.html")

@app.route("/letters_input/<int:num_letters>", methods=["GET", "POST"])
def letters_input(num_letters):
    if request.method == "POST":
        letters = request.form.getlist("letters")
        letters = ''.join(letters).lower()
        if len(letters) == num_letters:
            valid_words = find_words(letters)
            return render_template("index.html", words=valid_words, letters=letters)
        else:
            error = "Please fill all the letters correctly."
            return render_template("letters_input.html", num_letters=num_letters, error=error)
    return render_template("letters_input.html", num_letters=num_letters)

def find_words(letters):
    all_permutations = set()
    for i in range(1, len(letters) + 1):
        all_permutations.update([''.join(p) for p in permutations(letters, i)])
    valid_words = {word: len(word) for word in all_permutations if word in dictionary}
    
    # Sort words first by length and then alphabetically
    sorted_words = dict(sorted(valid_words.items(), key=lambda item: (item[1], item[0])))
    return sorted_words

if __name__ == "__main__":
    app.run(debug=True)
