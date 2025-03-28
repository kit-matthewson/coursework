package test;

import main.Card;
import main.CardHolder;
import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class CardHolderTest {

    private CardHolder cardHolderA;
    private CardHolder cardHolderB;

    @Before
    public void setUp() {
        cardHolderA = new CardHolder(1) {
        };
        cardHolderB = new CardHolder(2) {
        };
    }

    @Test
    public void pushCard() {
        Card card = new Card(1);
        cardHolderA.pushCard(card);

        List<Card> cards = cardHolderA.getCards();
        assertEquals("CardHolder should contain exactly 1 card after push", 1, cards.size());
        assertEquals("The pushed card should be the first in the CardHolder", card, cards.getFirst());
    }

    @Test
    public void popCard() {
        Card card = new Card(1);
        cardHolderA.pushCard(card);

        Card poppedCard = cardHolderA.pop();
        assertEquals("The popped card should match the one that was pushed", card, poppedCard);
        assertTrue("CardHolder should be empty after popping the only card", cardHolderA.getCards().isEmpty());
    }

    @Test(expected = IllegalStateException.class)
    public void popCard_empty() {
        cardHolderA.pop();
    }

    @Test
    public void removeCard() {
        Card card = new Card(1);
        cardHolderA.pushCard(card);

        boolean removed = cardHolderA.removeCard(card);
        assertTrue("removeCard should return true for a card present in the CardHolder", removed);
        assertTrue("CardHolder should be empty after removing the only card", cardHolderA.getCards().isEmpty());
    }

    @Test
    public void removeCard_nonExistent() {
        Card card = new Card(1);
        boolean removed = cardHolderA.removeCard(card);

        assertFalse("removeCard should return false for a card not present in the CardHolder", removed);
    }

    @Test
    public void transferCard() {
        Card card = new Card(1);
        cardHolderA.pushCard(card);

        cardHolderA.transferCard(card, cardHolderB);

        assertTrue("CardHolderA should be empty after transferring its only card", cardHolderA.getCards().isEmpty());
        assertEquals("CardHolderB should contain exactly 1 card after transfer", 1, cardHolderB.getCards().size());
        assertEquals("The transferred card should be present in CardHolderB", card, cardHolderB.getCards().getFirst());
    }

    @Test(expected = IllegalStateException.class)
    public void transferCard_nonExistent() {
        Card card = new Card(1);
        cardHolderA.transferCard(card, cardHolderB);
    }

    @Test
    public void allCardsSame() {
        cardHolderA.pushCard(new Card(1));
        cardHolderA.pushCard(new Card(1));

        assertTrue("allCardsSame should return true when all cards have the same denomination", cardHolderA.allCardsSame());

        cardHolderA.pushCard(new Card(2));
        assertFalse("allCardsSame should return false when cards have different denominations", cardHolderA.allCardsSame());
    }

    @Test
    public void allCardsSame_empty() {
        assertTrue("allCardsSame should return true for an empty CardHolder", cardHolderA.allCardsSame());
    }

    @Test
    public void getCards() {
        Card card1 = new Card(1);
        Card card2 = new Card(2);

        cardHolderA.pushCard(card1);
        cardHolderA.pushCard(card2);

        List<Card> cards = cardHolderA.getCards();
        assertEquals("CardHolder should contain 2 cards", 2, cards.size());
        assertTrue("CardHolder should contain card1", cards.contains(card1));
        assertTrue("CardHolder should contain card2", cards.contains(card2));
    }

    @Test
    public void size() {
        assertEquals("size should return 0 for an empty CardHolder", 0, cardHolderA.size());

        cardHolderA.pushCard(new Card(1));
        cardHolderA.pushCard(new Card(2));

        assertEquals("size should return the correct count of cards in the CardHolder", 2, cardHolderA.size());
    }
}
