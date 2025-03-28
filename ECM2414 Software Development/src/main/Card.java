package main;

/**
 * A playing card with a specific denomination.
 */
public class Card {
    private final int denomination;

    /**
     * Creates a {@code Card} with the specified denomination.
     *
     * @param denomination the denomination of the card
     */
    public Card(int denomination) {
        this.denomination = denomination;
    }

    /**
     * Returns the denomination of this card.
     *
     * @return the denomination of the card
     */
    public int getDenomination() {
        return denomination;
    }
}
