package main;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Logs Deck actions to a file named "deck<n>.txt".
 */
public class FileDeckLogger implements IDeckLogger {
    private final String fileName;

    /**
     * Constructor that initializes the logger and creates the file.
     *
     * @param deckNumber The number of the deck being logged.
     */
    public FileDeckLogger(int deckNumber) {
        this.fileName = String.format("logs/deck%d.txt", deckNumber);

        File file = new File(fileName);

        try {
            File logDir = new File("logs");
            if (!logDir.exists() && !logDir.mkdirs()) {
                throw new IOException("Could not create logs directory");
            }

            boolean deleted = file.delete();
            boolean created = file.createNewFile();

            if (deleted) {
                System.out.println("Old log file deleted: " + fileName);
            }

            if (!created) {
                throw new IOException("Could not create file " + fileName);
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void logCards(Deck deck) {
        StringBuilder cards = new StringBuilder();

        for (Card c : deck.getCards()) {
            cards.append(c.getDenomination()).append(" ");
        }

        writeToFile(String.format("deck %d contains: %s\n", deck.number(), cards));
    }

    /**
     * Writes a log message to the file associated with the deck.
     *
     * @param message The log message to write.
     */
    private void writeToFile(String message) {
        try (FileWriter writer = new FileWriter(fileName, true)) {
            writer.write(message);
        } catch (IOException e) {
            System.err.printf("Failed to write to %s: %s\n", fileName, e.getMessage());
        }
    }
}
