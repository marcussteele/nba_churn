# Predicting when an NBA Player will leave his team

## Table of Contents
1. [Introduction](#intro)
2. [Process](#process)

<a name="intro"></a>
### Introduction 
In recent years there have been more big name players that are leaving their teams and going to play with other teams. They are going to play with friends, going to play where they are paid more, or leaving to go to teams to win a championship. A few recent examples, LeBron James, Kevin Durant, and Kyrie Irving.

This means that teams do not have as much power as they did before. It is sometimes out of their hands when a player wants to leave. MY goal is to accurately predict when a player is going to leave when he is in the last year of his contract. This way teams can adjust and be prepared when their star player leaves.

<a name="process"></a>
PROCESS:   
First I webscraped data from a couple different websites. I gathered stats data from 2009 to the present, salary data from 2011 to the present, and team data from 2011 to the present. I have more data on the players stats so I can look at how their previous stats affected if they would leave or not.  
After scraping all this data, I combined it all together so I could run it through a model to test it.  
The next step was to explore the data. After looking at the data I noticed that players salaries seemed to go up every year. That makes sense because the salary cap in the NBA was going up every year. (Mostly because they were making more money from TV deals)  
I read about players salaries a little bit and learned that most salaries are calculated but taking a percentage of the salary cap. A max player is someone who makes 35% of the total salary cap. The average across the whole league is 5.7%. I decided to add this into the model to see if it has an effect on players leaving or not.  
Some other things i noticed was that surprisingly 75.5% of players leave at the end of their contracts. On the other side there are players like Dirk Nowitzki who have been on the same team for 20 years. I added a feature of years with the same team to see if that has an effect on a player leaving.  
Other added features: Whether the team made the playoffs that year or not, difference in minutes played this year from last 3 years, difference in points scored this year from last 3 years, whether they were traded that year or not.  
After exploring the data and adding features
- Cluster similar players into groups
![](clusters_pca.png)
- Ran a boosting model on each group to predict who is going to churn

HOW TO RUN:
- In scraping.py there is code that will scrape the players statistics, salary, and team data.
- It then combines and saves this data onto your computer


RESULTS:  

- Clusters are split mostly by games played, games started, and minutes played.
- Group 0 are players that play most games and start most games
- Group 1 are players that play very little games to some games
- Group 2 are players that play most games and either dont start or start some games


# Group 0

# Group 1

# Group 2
 


Data sources:
https://www.spotrac.com/nba/  
https://www.basketball-reference.com/  
https://hoopshype.com/  