package main;

/**
 * Logs Deck actions to console.
 */
public class ConsoleDeckLogger implements IDeckLogger {
    @Override
    public void logCards(Deck deck) {
        StringBuilder cards = new StringBuilder();

        for (Card c : deck.getCards()) {
            cards.append(c.getDenomination());
            cards.append(" ");
        }

        System.out.printf("deck %d contains: %s\n", deck.number(), cards);
    }
}
