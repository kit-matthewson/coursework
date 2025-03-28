package main;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Represents the Pack of cards used in the game.
 */
public class Pack extends CardHolder {
    /**
     * Creates a {@code Pack} by reading cards from a file.
     *
     * <p>
     * This method throws an {@link IOException} if:
     * <ul>
     *     <li>The file is invalid.</li>
     *     <li>The file does not contain exactly {@code 8 * numPlayers} lines.</li>
     *     <li>The file contains anything other than valid integer values representing card numbers.</li>
     * </ul>
     * </p>
     *
     * @param fileName   the name of the file containing card data
     * @param numPlayers the number of players in the game (used to validate file content)
     * @throws IOException if the pack file is invalid
     */
    public Pack(String fileName, int numPlayers) throws IOException {
        super(0);

        BufferedReader br = new BufferedReader(new FileReader(fileName));
        ArrayList<Card> card_input = readCards(br);

        if (card_input.size() != 8 * numPlayers) {
            throw new IOException("must contain 8n lines");
        }

        cards.addAll(card_input);
    }

    private ArrayList<Card> readCards(BufferedReader reader) throws IOException {
        ArrayList<Card> cards = new ArrayList<>();

        String line;
        while ((line = reader.readLine()) != null) {
            try {
                int number = Integer.parseInt(line);
                cards.add(new Card(number));
            } catch (NumberFormatException e) {
                throw new IOException("must only contain integers");
            }
        }

        return cards;
    }
}