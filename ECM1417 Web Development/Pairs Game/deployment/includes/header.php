<?php
if (isset($_GET["logout"])) {
    setcookie("user", "", time() - 1000, "/");
    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Pairs Game</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">

    <style>
        .navbar-nav .nav-link {
            font-family: Verdana, sans-serif;
            font-weight: bold;
            font-size: 12px;
        }
    </style>

    <?php
    $current_page = basename($_SERVER["SCRIPT_NAME"]);
    $logged_in = isset($_COOKIE["user"]);

    if ($logged_in) {
        $user_data = json_decode($_COOKIE["user"], true);

        $username = htmlspecialchars($user_data["username"]);
        $user_emoji = htmlspecialchars($user_data["emoji"]);
        $user_colour = htmlspecialchars($user_data["background"]);
    }
    ?>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-5">
        <a class="navbar-brand" href="../index.php">Pairs</a>

        <?php if ($logged_in): ?>
            <div class="rounded-2 border border-secondary p-0"
                style="background-color: <?php echo $user_colour ?>; aspect-ratio: 1; align-content: center;">
                <span class="navbar-brand p-1 m-0 h1"><?php echo $user_emoji ?></span>
            </div>
        <?php endif; ?>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse px-4" id="navbarSupportedContent" style="font-weight: bold;">

            <ul class="navbar-nav">
                <li class="nav-item">
                    <a href="../index.php"
                        class="nav-link <?php echo ($current_page == 'index.php') ? 'active' : ''; ?>">Home</a>
                </li>
            </ul>

            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a href="../pairs.php"
                        class="nav-link <?php echo ($current_page == 'pairs.php') ? 'active' : ''; ?>">Memory</a>
                </li>

                <?php if ($logged_in): ?>
                    <li class="nav-item">
                        <a href="../leaderboard.php"
                            class="nav-link <?php echo ($current_page == 'leaderboard.php') ? 'active' : ''; ?>">Leaderboard</a>
                    </li>

                    <!-- <li class="nav-item">
                        <a href="?logout=true" class="nav-link">Logout</a>
                    </li> -->
                <?php else: ?>
                    <li class="nav-item">
                        <a href="../registration.php"
                            class="nav-link <?php echo ($current_page == 'register.php') ? 'active' : ''; ?>">Register</a>
                    </li>
                <?php endif; ?>
            </ul>
        </div>
    </nav>

    <div id="main">
