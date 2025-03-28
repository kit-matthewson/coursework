package main;

import java.io.IOException;
import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * Represents the main driver class for the card game.
 *
 * <p>
 * This class handles the game setup, including reading inputs, creating players
 * and decks, dealing cards, and running the game loop. The game ends when one
 * player declares victory, and the final state of all decks and players is logged.
 * </p>
 */
public class CardGame {
    private final Player[] players;
    private final Deck[] decks;

    /**
     * Constructs a {@code CardGame} by setting up players, decks, and dealing cards.
     *
     * <p>
     * Prompts the user for the number of players and the location of the pack file,
     * then initialises the decks and players, and deals cards to each.
     * </p>
     */
    public CardGame() {
        int numPlayers = getNumPlayers();

        decks = new Deck[numPlayers];
        for (int i = 0; i < numPlayers; i++) {
            decks[i] = new Deck(new FileDeckLogger(i + 1), i + 1);
        }

        players = new Player[numPlayers];
        for (int i = 0; i < numPlayers; i++) {
            players[i] = new Player(new FilePlayerLogger(i + 1), i + 1, numPlayers, decks);
        }

        Pack pack = getPack(numPlayers);
        deal(pack);
    }

    /**
     * The entry point of the application. Initialises and runs the game.
     *
     * @param args command-line arguments (unused)
     */
    public static void main(String[] args) {
        CardGame game = new CardGame();
        System.out.println("Running game...");
        game.run();
        System.out.println("Game ended.");
    }

    /**
     * Deals the cards between players and decks, starting round-robin with the players and then the decks.
     *
     * @param pack the {@link Pack} to deal.
     */
    private void deal(Pack pack) {
        for (int j = 0; j < 4; j++) {
            for (Player player : players) {
                player.pushCard(pack.pop());
            }
        }

        for (int j = 0; j < 4; j++) {
            for (Deck deck : decks) {
                deck.pushCard(pack.pop());
            }
        }
    }

    /**
     * Starts the game and manages the main gameplay loop.
     *
     * <p>
     * The game runs concurrently, with all players taking turns until a winner is found.
     * The winner is declared, losing players are notified, and the final state of all
     * decks is logged.
     * </p>
     */
    public void run() {
        Player winner = null;

        for (Player player : players) {
            new Thread(player).start();
        }

        // Gameplay loop
        while (winner == null) {
            for (Player player : players) {
                if (player.allCardsSame()) {
                    winner = player;
                    break;
                }
            }

            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }

        // End-of-game logging
        winner.logWin();

        for (Player player : players) {
            if (player != winner) {
                player.flagLose(winner);
            }

            player.logHand();
        }

        for (Deck deck : decks) {
            deck.logCards();
        }
    }

    /**
     * Prompts the user for the number of players.
     *
     * <p>
     * Ensures the input is valid and greater than zero. If invalid, the user
     * is prompted again.
     * </p>
     *
     * @return the number of players
     */
    private int getNumPlayers() {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter number of players: ");

        int numPlayers;
        try {
            numPlayers = sc.nextInt();
        } catch (InputMismatchException e) {
            System.out.println("Invalid number of players: must be an integer.\n");
            return getNumPlayers();
        }

        if (numPlayers <= 0) {
            System.out.println("Invalid number of players: must be greater than 0.\n");
            return getNumPlayers();
        }

        return numPlayers;
    }

    /**
     * Prompts the user for the location of the pack file and loads the pack.
     *
     * <p>
     * Ensures the pack file is valid, containing exactly {@code 8 * numPlayers}
     * lines with valid integers. If invalid, the user is prompted again.
     * </p>
     *
     * @param numPlayers the number of players in the game
     * @return the {@link Pack} loaded from the specified file
     */
    private Pack getPack(int numPlayers) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter pack location: ");
        String fileName = sc.next();

        try {
            return new Pack(fileName, numPlayers);
        } catch (IOException e) {
            System.out.printf("Invalid pack file: %s.\n\n", e.getMessage());
            return getPack(numPlayers);
        }
    }
}
