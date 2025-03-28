<?php
$error = false;

$emojis = [
    "😊",
    "😎",
    "😂",
    "😍",
    "🤔",
    "😁",
    "😇",
    "😜",
    "🤩",
    "🥳",
    "🎉",
    "🎶",
    "🚀",
    "🌟",
    "🔥",
    "⚡",
    "🌈",
    "💖",
    "🍕",
    "🏆"
];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $emoji = $_POST["emoji"];
    $background = $_POST["background"];

    if (empty($username)) {
        $error = true;
    } elseif (preg_match('/[!@#%&*()+=\[\]{};:\'\"<>?,\/]/', $username)) {
        $error = true;
    } else {
        $user_data = [
            "username" => $username,
            "emoji" => $emoji,
            "background" => $background,
        ];

        // Store user data in a cookie that expires in 7 days
        setcookie("user", json_encode($user_data), time() + (7 * 24 * 60 * 60), "/");

        header("Location: index.php");
        exit;
    }
}
?>

<?php include 'includes/header.php'; ?>

<div class="text-light">
    <h1 class="display-1">Registration</h1>
    <hr class="my-4">

    <form class="needs-validation" method="POST" action="" novalidate style="width: 25%;">
        <div class="mb-3">
            <label for="usernameInput" class="form-label">Username</label>
            <input type="text" class="form-control <?php echo $error ? 'is-invalid' : ''; ?>" id="usernameInput"
                name="username" placeholder="Enter Username" required>
            <div class="invalid-feedback">
                <?php echo $error ? 'Username is required and cannot contain special characters like &quot; ! @ # % &amp; * ( ) + = { } [ ] &mdash; ; : &ldquo; &rsquo; &lt; &gt; ? /' : '' ?>
            </div>
        </div>

        <div class="mb-3">
            <label for="emojiSelect" class="form-label">Choose an Emoji</label>
            <select class="form-control" id="emojiSelect" name="emoji">
                <?php foreach ($emojis as $e) { ?>
                    <option value="<?php echo $e; ?>"><?php echo $e; ?></option>
                <?php } ?>
            </select>
        </div>

        <div class="mb-3">
            <label for="backgroundColor" class="form-label">Choose Background Color</label>
            <input type="color" class="form-control form-control-color" id="backgroundColor" name="background"
                value="#0D6EFD">
        </div>

        <button type="submit" class="btn btn-primary mt-2">Register</button>
    </form>
</div>

<?php include 'includes/footer.php'; ?>
