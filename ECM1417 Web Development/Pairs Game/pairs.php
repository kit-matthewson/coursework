<?php include 'includes/header.php'; ?>

<style>
    .game-board {
        display: grid;
        width: 50%;
        margin: 0 auto;
        gap: 10px;
        grid-template-columns: repeat(5, 1fr);
        justify-content: center;
    }

    .card {
        width: 140px;
        height: 180px;
        background: gray;
        font-family: monospace;
        font-size: x-large;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        border-radius: 10px;
        border: 3px solid black;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    .hidden {
        background: gray !important;
        color: gray !important;
        user-select: none;
    }
</style>

<div id="preGameContainer" style="width: 100%; display: block; box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);"
    class="text-center bg-dark p-5">
    <button class="btn btn-primary btn-lg" id="startGame">Start Game</button>
</div>

<div id="gameContainer" style="display: none; width: 100%; box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);"
    class="bg-dark p-5 m-0">
    <div class="text-center m-0 pb-5 text-light bg-dark">
        <h1 class="display-1">Pairs Game</h1>
        <h3>Time: <span id="time">0</span></h3>
    </div>

    <div class="game-board" id="gameBoard"></div>

    <div class="text-center m-0 pt-5 text-light bg-dark">
        <h3>Attempts: <span id="attempts">0</span></h3>
        <h3>Matched: <span id="matched">0</span></h3>
    </div>
</div>

<div id="gameOverContainer" style="display: none; width: 100%; box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);"
    class="bg-dark">
    <div class="text-center m-0 p-5 text-light bg-dark">
        <h1 class="display-1">Game Over!</h1>
        <h2><span id="score">0</span> points</h2>
        <div class="d-flex justify-content-center m-5">
            <button class="btn btn-primary btn-lg mx-2" id="restartGame">Play Again</button>
            <button class="btn btn-secondary btn-lg mx-2" id="submit">Submit Score</button>
        </div>
        <p class="mb-0 pb-0">Time: <span id="gameOverTime">0</span></p>
        <p class="mb-0 pb-0">Attempts: <span id="gameOverAttempts">0</span></p>
        <p class="mb-0 pb-0">Matched: <span id="gameOverMatched">0</span></p>
    </div>
</div>

<script>
    const num_cards = 10;

    // Game variables
    let attempts = 0;
    let matched = 0;
    let startTime = null;
    let gameOver = false;

    const eyes = ["o o", "0 0", "o 0", "x x", "@ @", "^ ^", "- -", "* *", "> <", "= =", "- o", "o -", "O O"];
    const mouths = ["---", "__", "o", ">-<", ")-(", "^v^", "w", "U", "==", "~~", "O", "0"];
    const colours = ["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#A833FF", "#FFD700", "#40E0D0", "#FF8C00", "#8A2BE2", "#FF0000", "#0000FF", "#FFFF00", "#00FFFF", "#9400D3", "#32CD32", "#FF6347", "#1E90FF"];

    let firstCard = null;
    let secondCard = null;
    let canFlip = true;
    let cards = [];

    // Shuffle cards
    function shuffleCards() {
        const shuffledCards = [];
        while (shuffledCards.length < num_cards) {
            shuffle(eyes);
            shuffle(mouths);
            shuffle(colours);
            shuffledCards.push([eyes[0], mouths[0], colours[0]]);
            shuffledCards.push([eyes[0], mouths[0], colours[0]]);
        }
        shuffle(shuffledCards);
        return shuffledCards;
    }

    // Shuffle array
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    document.getElementById("startGame").addEventListener("click", function () {
        startGame();
    });

    document.getElementById("restartGame").addEventListener("click", function () {
        startGame();
    });

    document.getElementById("submit").addEventListener("click", function () {
        const score = document.getElementById("score").textContent;
        const time = document.getElementById("time").textContent;
        const attempts = document.getElementById("attempts").textContent;
        const matched = document.getElementById("matched").textContent;

        fetch('leaderboard.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                score: document.getElementById("score").textContent,
                time: document.getElementById("time").textContent,
                attempts: document.getElementById("attempts").textContent,
                matched: document.getElementById("matched").textContent
            }),
        })
            .then(response => response.json())
            .then(data => {
                this.disabled = true;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Start game
    function startGame() {
        document.getElementById("preGameContainer").style.display = "none";
        document.getElementById("gameContainer").style.display = "block";
        document.getElementById("gameOverContainer").style.display = "none";
        document.getElementById("submit").disabled = false;

        // Initialize game cards
        cards = shuffleCards();
        displayCards();

        // Start timer
        startTime = new Date().getTime();
        setInterval(() => {
            if (gameOver) return;
            document.getElementById("time").textContent = Math.floor((new Date().getTime() - startTime) / 1000);
        }, 1000);

        // Reset variables
        attempts = 0;
        matched = 0;
        firstCard = null;
        secondCard = null;
        canFlip = true;
        gameOver = false;

        document.getElementById("time").textContent = 0;
        document.getElementById("attempts").textContent = attempts;
        document.getElementById("matched").textContent = matched;
    }

    // Display cards
    function displayCards() {
        const gameBoard = document.getElementById("gameBoard");
        gameBoard.innerHTML = '';

        cards.forEach((card, index) => {
            const cardElement = document.createElement("div");
            cardElement.classList.add("card", "hidden");
            cardElement.setAttribute("data-index", index);
            cardElement.setAttribute("data-eyes", card[0]);
            cardElement.setAttribute("data-mouth", card[1]);
            cardElement.setAttribute("data-color", card[2]);

            const eyesText = document.createElement("p");
            eyesText.textContent = card[0];

            const mouthText = document.createElement("p");
            mouthText.textContent = card[1];

            cardElement.appendChild(eyesText);
            cardElement.appendChild(mouthText);

            cardElement.addEventListener("click", cardClick);
            gameBoard.appendChild(cardElement);
        });
    }

    // Handle card click
    function cardClick() {
        if (!canFlip || this === firstCard || !this.classList.contains("hidden")) return;

        this.classList.remove("hidden");
        this.style.backgroundColor = this.dataset.color;
        this.style.color = "black";

        if (!firstCard) {
            firstCard = this;
        } else {
            secondCard = this;
            canFlip = false;

            if (firstCard.dataset.eyes === secondCard.dataset.eyes && firstCard.dataset.mouth === secondCard.dataset.mouth && firstCard.dataset.color === secondCard.dataset.color) {
                firstCard = null;
                secondCard = null;
                canFlip = true;

                matched++;
            } else {
                setTimeout(() => {
                    firstCard.classList.add("hidden");
                    secondCard.classList.add("hidden");
                    firstCard.style.backgroundColor = "gray";
                    secondCard.style.backgroundColor = "gray";
                    firstCard.style.color = "gray";
                    secondCard.style.color = "gray";
                    firstCard = null;
                    secondCard = null;
                    canFlip = true;
                }, 500);
            }

            attempts++;
        }

        document.getElementById("attempts").textContent = attempts;
        document.getElementById("matched").textContent = matched;

        if (matched === (num_cards / 2)) {
            gameOver = true;

            setTimeout(() => {
                const time = Math.floor((new Date().getTime() - startTime) / 1000);
                const points = Math.floor(10000 / (attempts + time));

                document.getElementById("score").textContent = points;
                document.getElementById("gameOverTime").textContent = time;
                document.getElementById("gameOverAttempts").textContent = attempts;
                document.getElementById("gameOverMatched").textContent = matched;

                document.getElementById("preGameContainer").style.display = "none";
                document.getElementById("gameContainer").style.display = "none";
                document.getElementById("gameOverContainer").style.display = "block";
            }, 1000);
        }
    }
</script>

<?php include 'includes/footer.php'; ?>
