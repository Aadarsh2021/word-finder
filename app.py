from flask import Flask, render_template, request, redirect, url_for
from itertools import permutations
import nltk
from nltk.corpus import words
from urllib.parse import quote

app = Flask(__name__)

# Load the list of valid words
nltk.download('words')
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
        if len(letters) >= num_letters:  # Check if the input is at least the number of letters required
            valid_words = find_words(letters)
            return render_template("result.html", words=valid_words, letters=letters, num_letters=num_letters)
        else:
            error = "The number of letters provided is less than the number of letters required."
            return render_template("letters_input.html", num_letters=num_letters, error=error)
    return render_template("letters_input.html", num_letters=num_letters)

def find_words(letters):
    all_permutations = set()
    for i in range(1, len(letters) + 1):
        all_permutations.update([''.join(p) for p in permutations(letters, i)])
    valid_words = {word: len(word) for word in all_permutations if word in dictionary}
    # Sort the valid words by their length
    sorted_valid_words = dict(sorted(valid_words.items(), key=lambda item: item[1]))
    return sorted_valid_words

if __name__ == "__main__":
    app.run(debug=True)
