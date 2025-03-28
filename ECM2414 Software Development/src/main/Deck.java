package main;

import java.util.concurrent.locks.ReentrantLock;

/**
 * Represents a Deck of cards in the game. The Deck holds and manages a collection
 * of {@link Card} objects, allowing cards to be drawn or discarded by players.
 * This class supports thread-safe operations using a {@link ReentrantLock}.
 */
public class Deck extends CardHolder {
    private final IDeckLogger logger;

    /**
     * Constructs a {@code Deck} for use in the game.
     *
     * @param logger the {@link IDeckLogger} to use
     * @param n the identifier for this Deck, typically representing the player's number
     */
    public Deck(IDeckLogger logger, int n) {
        super(n);
        this.logger = logger;
    }

    /**
     * Logs the current state of this Deck's cards.
     */
    public void logCards() {
        logger.logCards(this);
    }
}
