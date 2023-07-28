# scores_from_commentary
A tool that prepares a scoreboard from given commentary lines.

Problem Statement:

The regular expression code basically is to generate a cricket scorecard using the given commentary.
The commentary is taken from the Cricbuzz page for a India Pakistan match which was held
in the Asia Cup.
What we need to do is the parse the input text given and take the help of regular
expression in order to extract the scorecard. 
The scores are available on the crickbuzz link- https://www.cricbuzz.com/live-cricket-scorecard/51210/ind-vs-pak-2nd-match-group-a-asia-cup-2022

In the commentary you can see the following format
X.Y bowler to batsman, event followed by some text commentary
0.4 Bhuvneshwar to Babar Azam, FOUR, classic Babar Azam!Just a bit overpitched on off, Babar drives
with the full face on the bat. The timing is too pure as it gets past the rightward dive of mid-off
So, from above you can add 1 ball to Bhuvneshwar bowling tally, 4 runs to Babar Azam tally., and so on.
Teams.txt contains players names. You can map the players name as per the input in the text based
commentary. Like Chahal for Yuzvendra Chahal and so on.

Input files: india_innings2.txt , pakistan_innings1.txt , teams.txt

Output : scoreboard.xlsx (an excel file) and scoreboard.csv (a csv file)
