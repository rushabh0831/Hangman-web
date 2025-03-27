async function startNewGame() {
    const response = await fetch('/new-game');
    const data = await response.json();
    document.getElementById("word-display").textContent = "_".repeat(data.word_length);
    document.getElementById("tries").textContent = data.tries;
    document.getElementById("hangman-image").src = data.hangman_image;
    document.getElementById("message").textContent = "";
}

async function makeGuess() {
    const letterInput = document.getElementById("letter-input");
    const letter = letterInput.value.toUpperCase();
    letterInput.value = "";

    if (!letter) return;

    const response = await fetch('/guess', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ letter })
    });

    const data = await response.json();
    document.getElementById("word-display").textContent = data.word_completion;
    document.getElementById("tries").textContent = data.tries;
    document.getElementById("hangman-image").src = data.hangman_image;
    document.getElementById("message").textContent = data.message || "";

    if (data.game_over) {
        alert(data.message);
    }
}

window.onload = startNewGame;
