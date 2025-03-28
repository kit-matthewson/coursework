package main;

/**
 * Logs Player actions to console.
 */
public class ConsolePlayerLogger implements IPlayerLogger {
    @Override
    public void logDraw(Player player, Card card, Deck deck) {
        System.out.printf("player %d draws a %d from deck %d\n", player.number(), card.getDenomination(), deck.number());
    }

    @Override
    public void logDiscard(Player player, Card card, Deck deck) {
        System.out.printf("player %d discards a %d to deck %d\n", player.number(), card.getDenomination(), deck.number());
    }

    @Override
    public void logHand(Player player) {
        StringBuilder cards = new StringBuilder();

        for (Card c : player.getCards()) {
            cards.append(c.getDenomination());
            cards.append(" ");
        }

        System.out.printf("player %d's current hand is: %s\n", player.number(), cards);
    }

    @Override
    public void logWin(Player player) {
        System.out.printf("player %d wins\n", player.number());
    }

    @Override
    public void logLose(Player player, Player winner) {
        System.out.printf("player %d has informed player %d that they have won\n", winner.number(), player.number());
    }
}
