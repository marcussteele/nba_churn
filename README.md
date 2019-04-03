# nba_churn


GOAL: 
In recent years there have been more big name players that are leaving their teams and going to play with other teams. They are going to play with friends, going to play where they are paid more, or leaving to go to teams to win a championship. A few recent examples, LeBron James, Kevin Durant, and Kyrie Irving.

This means that teams do not have as much power as they did before. It is sometimes out of their hands when a player wants to leave. MY goal is to accurately predict when a player is going to leave when he is in the last year of his contract. This way teams can adjust and be prepared when their star player leaves.

PROCESS:
- Import data
- Combine data from different years and websites
- Deal with missing data and data that is not uniform across websites
- Explore data
- PCA
- Cluster similar players into groups
- Ran a boosting model on each group to predict who is going to churn

HOW TO RUN:
- In scraping.py there is code that will scrape the players statistics, salary, and team data.
- It then combines and saves this data into a pickle file

RESULTS:

IDEAS:
- 

Data sources:
https://www.spotrac.com/nba/
https://www.basketball-reference.com/leagues/
https://hoopshype.com/salaries/players/