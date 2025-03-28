package main;

/**
 * Interface for logging deck actions.
 */
public interface IDeckLogger {

    /**
     * Logs the cards contained in the specified deck.
     *
     * @param deck the {@link Deck} whose cards are being logged.
     */
    void logCards(Deck deck);
}
