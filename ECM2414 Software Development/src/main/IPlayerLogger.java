package main;

/**
 * Interface for logging player actions.
 */
public interface IPlayerLogger {

    /**
     * Logs when a player draws a card from a deck.
     *
     * @param player the {@link Player} who performed the draw
     * @param card   the {@link Card} drawn by the player
     * @param deck   the {@link Deck} from which the card was drawn
     */
    void logDraw(Player player, Card card, Deck deck);

    /**
     * Logs when a player discards a card to a deck.
     *
     * @param player the {@link Player} who performed the discard
     * @param card   the {@link Card} discarded by the player
     * @param deck   the {@link Deck} to which the card was discarded
     */
    void logDiscard(Player player, Card card, Deck deck);

    /**
     * Logs the current hand of a player.
     *
     * @param player the {@link Player} whose hand is being logged
     */
    void logHand(Player player);

    /**
     * Logs when a player wins the game.
     *
     * @param player the {@link Player} who won the game
     */
    void logWin(Player player);

    /**
     * Logs when a player loses the game due to another player's win.
     *
     * @param player the {@link Player} who lost the game
     * @param winner the {@link Player} who won the game
     */
    void logLose(Player player, Player winner);
}
