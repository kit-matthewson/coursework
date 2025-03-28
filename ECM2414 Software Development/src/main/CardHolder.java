package main;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Represents a CardHolder, a thread-safe collection of {@link Card Cards}.
 */
public abstract class CardHolder {
    protected final int n;
    protected final ArrayList<Card> cards = new ArrayList<>();
    private final Lock lock = new ReentrantLock();

    /**
     * Constructs a CardHolder object with the specified identification number.
     *
     * @param n the identification number (1-indexed)
     */
    public CardHolder(int n) {
        this.n = n;
    }

    /**
     * Adds a {@link Card} to this CardHolder.
     *
     * @param card the {@link Card} to be added
     */
    public void pushCard(Card card) {
        lock.lock();
        try {
            cards.add(card);
        } finally {
            lock.unlock();
        }
    }

    /**
     * Removes and returns the first {@link Card} from this CardHolder.
     *
     * @return the {@link Card} that was drawn from the Deck
     * @throws IllegalStateException if the CardHolder is empty
     */
    public Card pop() {
        lock.lock();
        try {
            if (cards.isEmpty()) {
                throw new IllegalStateException("Cannot pop from an empty CardHolder");
            }
            return cards.removeFirst();
        } finally {
            lock.unlock();
        }
    }

    /**
     * Removes a specified {@link Card} from this CardHolder.
     *
     * @param card the {@link Card} to remove
     * @return {@code true} if the card was successfully removed, {@code false} otherwise
     */
    public boolean removeCard(Card card) {
        lock.lock();
        try {
            return cards.remove(card);
        } finally {
            lock.unlock();
        }
    }

    /**
     * Removes a {@link Card} from this CardHolder and adds it to another CardHolder.
     *
     * @param card the {@link Card} to remove
     * @param to   the {@link CardHolder} to transfer the card to
     * @throws IllegalStateException if the card cannot be removed from this CardHolder
     */
    public void transferCard(Card card, CardHolder to) {
        lock.lock();
        try {
            if (!removeCard(card)) {
                throw new IllegalStateException("Invalid card");
            }
        } finally {
            lock.unlock();
        }

        to.pushCard(card);
    }

    /**
     * Checks if all the {@link Card Cards} in this CardHolder have the same denomination.
     *
     * @return {@code true} if all {@link Card Cards} have the same denomination, {@code false} otherwise
     */
    public boolean allCardsSame() {
        lock.lock();
        try {
            if (cards.isEmpty()) {
                return true;
            }

            int denomination = cards.getFirst().getDenomination();
            for (Card card : cards) {
                if (card.getDenomination() != denomination) {
                    return false;
                }
            }

            return true;
        } finally {
            lock.unlock();
        }
    }

    /**
     * Shuffles the {@link Card Cards} in this CardHolder.
     */
    public void shuffle() {
        lock.lock();
        try {
            Collections.shuffle(cards);
        } finally {
            lock.unlock();
        }
    }

    /**
     * Returns an immutable list of the {@link Card Cards} currently held by this CardHolder.
     *
     * @return an unmodifiable {@link List} of {@link Card Cards}
     */
    public List<Card> getCards() {
        lock.lock();
        try {
            return List.copyOf(cards);
        } finally {
            lock.unlock();
        }
    }

    /**
     * Returns the number of {@link Card Cards} in this CardHolder.
     *
     * @return the number of {@link Card Cards} in this CardHolder
     */
    public int size() {
        lock.lock();
        try {
            return cards.size();
        } finally {
            lock.unlock();
        }
    }

    /**
     * Returns the number of this CardHolder.
     *
     * @return the number of this CardHolder
     */
    public int number() {
        return n;
    }
}
