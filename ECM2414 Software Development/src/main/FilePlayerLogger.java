package main;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Logs Player actions to a file named "player<n>.txt".
 */
public class FilePlayerLogger implements IPlayerLogger {
    private final String fileName;

    /**
     * Constructor that initializes the logger and creates the file.
     *
     * @param playerNumber The number of the player being logged.
     */
    public FilePlayerLogger(int playerNumber) {
        this.fileName = String.format("logs/player%d.txt", playerNumber);

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
    public void logDraw(Player player, Card card, Deck deck) {
        writeToFile(String.format("player %d draws a %d from deck %d\n",
                player.number(), card.getDenomination(), deck.number()));
    }

    @Override
    public void logDiscard(Player player, Card card, Deck deck) {
        writeToFile(String.format("player %d discards a %d to deck %d\n",
                player.number(), card.getDenomination(), deck.number()));
    }

    @Override
    public void logHand(Player player) {
        StringBuilder cards = new StringBuilder();

        for (Card c : player.getCards()) {
            cards.append(c.getDenomination()).append(" ");
        }

        writeToFile(String.format("player %d's current hand is: %s\n",
                player.number(), cards));
    }

    @Override
    public void logWin(Player player) {
        writeToFile(String.format("player %d wins\n", player.number()));
    }

    @Override
    public void logLose(Player player, Player winner) {
        writeToFile(String.format("player %d has informed player %d that they have won\n",
                winner.number(), player.number()));
    }

    /**
     * Writes a log message to the file associated with the player.
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
