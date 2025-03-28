<?php
session_start();

// Handle POST request to add a new entry to the leaderboard
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get POST data
    $data = json_decode(file_get_contents('php://input'), true);

    // Check if user is authenticated
    if (!isset($_COOKIE['user'])) {
        http_response_code(403);
        echo json_encode(["error" => "User not authenticated"]);
        exit;
    }

    // Get user data from cookie
    $user = json_decode($_COOKIE['user'], true);
    $username = $user['username'];
    $emoji = $user['emoji'];
    $background = $user['background'];

    $score = $data['score'];
    $time = $data['time'];
    $attempts = $data['attempts'];
    $matched = $data['matched'];

    // Add new entry to the leaderboard
    $entry = "$username,$emoji,$background,$score,$time,$attempts,$matched\n";
    file_put_contents('leaderboard.txt', $entry, FILE_APPEND);

    // Send success response
    echo json_encode(["success" => true]);
    exit;
}
?>

<?php include 'includes/header.php'; ?>

<style>
    thead.thead-primary th {
        background-color: rgb(13, 110, 253);
        color: rgb(248, 249, 250);
    }
</style>

<div id="gameContainer" style="width: 100%; box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);"
    class="bg-dark p-5 m-0 text-light">
    <h1 class="display-1">Leaderboard</h1>
    <hr class="my-4">

    <!-- Leaderboard table -->
    <table class="table table-hover" style="border-spacing: 2px;">
        <thead class="thead-primary">
            <tr>
                <th scope="col"></th>
                <th scope="col">Username</th>
                <th scope="col">Score</th>
                <th scope="col">Time</th>
                <th scope="col">Attempts</th>
            </tr>
        </thead>
        <tbody>
            <!-- Display leaderboard entries -->
            <?php
            $leaderboard = file('leaderboard.txt');

            // Sort leaderboard entries by score in descending order
            usort($leaderboard, function ($a, $b) {
                $dataA = explode(',', $a);
                $dataB = explode(',', $b);
                return intval($dataB[3]) - intval($dataA[3]);
            });

            // Display leaderboard entries
            foreach ($leaderboard as $entry) {
                $data = explode(',', $entry); ?>
                <tr>
                    <td>
                        <div class="rounded-2 border border-secondary p-0"
                            style="background-color: <?php echo htmlspecialchars($data[2]); ?>; aspect-ratio: 1; align-content: center; width: 2em;">
                            <span class="p-1 m-0"><?php echo htmlspecialchars($data[1]); ?></span>
                        </div>
                    </td>
                    <td><?php echo htmlspecialchars($data[0]); ?></td>
                    <td><?php echo htmlspecialchars($data[3]); ?></td>
                    <td><?php echo htmlspecialchars($data[4]); ?></td>
                    <td><?php echo htmlspecialchars($data[5]); ?></td>
                </tr>
            <?php } ?>
        </tbody>
    </table>
</div>

<?php include 'includes/footer.php'; ?>
