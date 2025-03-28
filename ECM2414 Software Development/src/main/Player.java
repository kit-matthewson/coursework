package main;

import java.util.Random;

/**
 * Represents a Player in a card game. This Player extends the `Thread` class
 * and runs concurrently with other Players.
 */
public class Player extends CardHolder implements Runnable {
    private final IPlayerLogger logger;

    private final Deck leftDeck;
    private final Deck rightDeck;

    private boolean gameOver = false;

    private final Random rand = new Random();

    /**
     * Constructs a Player object.
     *
     * @param logger     the {@link IPlayerLogger} to use
     * @param n          this player's number (1-indexed)
     * @param numPlayers the number of players in the game
     * @param decks      an ordered array of {@link Deck Decks} being used
     * @throws IllegalArgumentException if the provided number of players is less than 2
     */
    public Player(IPlayerLogger logger, int n, int numPlayers, Deck[] decks) {
        super(n);

        this.logger = logger;
        this.leftDeck = decks[(n - 1) % numPlayers];
        this.rightDeck = decks[n % numPlayers];
    }

    /**
     * The main execution loop for this Player thread. This method continues
     * to run until the Player wins or loses the game.
     */
    @Override
    public synchronized void run() {
        while (!gameOver) {
            if (allCardsSame()) {
                gameOver = true;
            } else {
                if (leftDeck.size() >= 4 && rightDeck.size() <= 4) {
                    doTurn();
                }

                try {
                    wait(rand.nextLong(5, 10));
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }
    }

    /**
     * Performs a single turn for this Player. This involves drawing a card from the left deck and discarding a non-matching card to the right deck.
     */
    private void doTurn() {
        if (allCardsSame()) {
            return;
        }

        draw();

        shuffle();

        for (Card card : cards) {
            if (card.getDenomination() != n) {
                discard(card);
                break;
            }
        }
    }

    /**
     * Draws a {@link Card} from the left {@link Deck} and adds it to {@code cards}.
     */
    private void draw() {
        Card draw = leftDeck.pop();
        pushCard(draw);

        logger.logDraw(this, draw, leftDeck);
    }

    /**
     * Discards a {@link Card} to the right {@link Deck} and removes it from {@code cards}.
     *
     * @param card the {@link Card} to discard
     */
    private void discard(Card card) {
        transferCard(card, rightDeck);

        logger.logDiscard(this, card, rightDeck);
    }

    /**
     * Sets the {@code hasLost} flag for this Player and logs the winner.
     *
     * @param winner the Player who won the game
     */
    public void flagLose(Player winner) {
        gameOver = true;
        logger.logLose(this, winner);
    }

    /**
     * Logs this Player's hand.
     */
    public void logHand() {
        logger.logHand(this);
    }

    /**
     * Logs that this Player has won the game.
     */
    public void logWin() {
        logger.logWin(this);
    }

    /**
     * Returns this Player's number.
     *
     * @return the Player's number
     */
    public int number() {
        return n;
    }
}