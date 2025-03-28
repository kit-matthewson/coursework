The website can be accessed from:
http://ml-lab-4d78f073-aa49-4f0e-bce2-31e5254052c7.ukwest.cloudapp.azure.com:64397/index.php

Features implemented:

- Consistent navbar across pages
  - Displays user's emoji with background colour if logged in
  - Shows leaderboard link if logged in, otherwise registration link
- Home page that shows either registration link or click to play button
- Pairs game initially shows start game button
- 10 randomly generated cards are displayed
- Cards are flipped when clicked
  - Cards are generated from a list of eyes, noses, and mouths with a random background colour
- Clicking on cards flips them
  - If the cards match they stay flipped
  - If the cards do not match they flip back after a short delay
- Game ends when all cards are matched
- The user is presented with a score based on their time and number of attempts
  - The user can choose to play again
  - The user can choose to submit their score to the leaderboard
- Leaderboard page shows all the scores submitted in descending order
