from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

word_list = [
    'wares', 'soup', 'mount', 'extend', 'brown', 'expert', 'tired', 'humidity', 'backpack',
    'python', 'keyboard', 'monitor', 'mouse', 'laptop', 'charger', 'notebook', 'pencil', 'eraser',
    'umbrella', 'raincoat', 'thunder', 'lightning', 'hurricane', 'tornado', 'volcano', 'earthquake',
    'penguin', 'giraffe', 'elephant', 'kangaroo', 'dolphin', 'octopus', 'squirrel', 'crocodile',
    'mountain', 'valley', 'desert', 'ocean', 'island', 'forest', 'jungle', 'glacier',
    'velocity', 'friction', 'gravity', 'momentum', 'pressure', 'energy', 'magnet', 'electricity',
    'astronomy', 'galaxy', 'satellite', 'comet', 'telescope', 'asteroid', 'nebula', 'blackhole',
    'puzzle', 'mystery', 'adventure', 'journey', 'fortune', 'treasure', 'island', 'castle', 'village',
    'warrior', 'knight', 'sorcerer', 'wizard', 'alchemy', 'potion', 'magic', 'spell', 'crystal',
    'tiger', 'leopard', 'cheetah', 'panther', 'wolf', 'fox', 'bear', 'eagle', 'falcon',
    'sunrise', 'twilight', 'midnight', 'dawn', 'dusk', 'season', 'autumn', 'summer', 'winter',
    'fiction', 'novel', 'poetry', 'drama', 'author', 'library', 'manuscript', 'journal', 'encyclopedia'
]
def get_word():
    return random.choice(word_list).upper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-game', methods=['GET'])
def new_game():
    word = get_word()
    session['word'] = word
    session['tries'] = 6
    session['guessed_letters'] = []
    
    return jsonify({"word_length": len(word), "tries": 6, "hangman_image": f"/static/hangman6.png"})

@app.route('/guess', methods=['POST'])
def guess():
    if 'word' not in session:
        return jsonify({"message": "Start a new game first!", "game_over": True})

    data = request.get_json()
    letter = data.get("letter", "").upper()

    word = session['word']
    guessed_letters = session['guessed_letters']
    tries = session['tries']

    if letter in guessed_letters:
        return jsonify({"message": "You already guessed that letter!", "tries": tries, "hangman_image": f"/static/hangman{tries}.png"})

    guessed_letters.append(letter)
    session['guessed_letters'] = guessed_letters

    if letter not in word:
        session['tries'] -= 1

    tries = session['tries']
    word_completion = "".join([l if l in guessed_letters else "_" for l in word])

    if "_" not in word_completion:
        return jsonify({"message": "You won!", "word_completion": word, "tries": tries, "hangman_image": f"/static/hangman{tries}.png", "game_over": True})

    if tries <= 0:
        return jsonify({"message": f"You lost! The word was {word}.", "word_completion": word, "tries": 0, "hangman_image": f"/static/hangman0.png", "game_over": True})

    return jsonify({
        "word_completion": word_completion,
        "tries": tries,
        "hangman_image": f"/static/hangman{tries}.png"
    })

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
