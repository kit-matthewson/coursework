<?php include 'includes/header.php'; ?>

<div class="text-light">
    <h1 class="display-1">Welcome to Pairs</h1>
    <p class="lead">Test your memory and speed as you progress through increasingly challenging levels!</p>

    <hr class="my-4">

    <?php if ($logged_in): ?>
        <a class="btn btn-primary btn-lg" href="pairs.php" role="button">Click here to play</a>
    <?php else: ?>
        <p>You are not logged in: <a class="bg-primary text-light px-2 py-1 small rounded text-decoration-none" href="registration.php">Register Now</a></p>
    <?php endif; ?>
</div>

<?php include 'includes/footer.php'; ?>
