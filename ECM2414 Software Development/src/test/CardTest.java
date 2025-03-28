package test;

import main.Card;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class CardTest {

    @Test
    public void getDenomination() {
        Card card = new Card(10);
        assertEquals(10, card.getDenomination());
    }
}