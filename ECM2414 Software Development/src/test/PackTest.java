package test;

import main.Card;
import main.Pack;
import org.junit.Test;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.Assert.assertEquals;

public class PackTest {

    @Test
    public void testPackCreation_ValidFile() throws IOException {
        int numPlayers = 2;
        String fileName = createTemporaryPackFile("1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n");

        Pack pack = new Pack(fileName, numPlayers);

        assertEquals("Pack should contain exactly 16 cards", 16, pack.getCards().size());
    }

    @Test(expected = IOException.class)
    public void testPackCreation_InvalidFile_NotEnoughLines() throws IOException {
        // Arrange
        int numPlayers = 2;
        String fileName = createTemporaryPackFile("1\n2\n3\n");

        // Act
        new Pack(fileName, numPlayers);
    }

    @Test(expected = IOException.class)
    public void testPackCreation_InvalidFile_NonIntegerValue() throws IOException {
        // Arrange
        int numPlayers = 2;
        String fileName = createTemporaryPackFile("1\n2\nthree\n4\n");

        // Act
        new Pack(fileName, numPlayers);
    }

    @Test
    public void testPop_ValidCase() throws IOException {
        // Arrange
        int numPlayers = 2;
        String fileName = createTemporaryPackFile("1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n");
        Pack pack = new Pack(fileName, numPlayers);

        // Act
        Card firstCard = pack.pop();

        // Assert
        assertEquals("The first card should have denomination 1", 1, firstCard.getDenomination());
        assertEquals("Pack should contain 15 cards after one pop", 15, pack.getCards().size());
    }

    @Test
    public void testPackCreation_EmptyFile() throws IOException {
        int numPlayers = 0;
        String fileName = createTemporaryPackFile("");

        try {
            new Pack(fileName, numPlayers);
        } catch (IOException e) {
            assertEquals("must contain 8n lines", e.getMessage());
        }
    }

    // Helper Method to Create Temporary Pack File
    private String createTemporaryPackFile(String content) throws IOException {
        Path tempFile = Files.createTempFile("pack", ".txt");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(tempFile.toFile()))) {
            writer.write(content);
        }
        return tempFile.toString();
    }
}
