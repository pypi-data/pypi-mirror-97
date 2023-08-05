# synthSportPlayer Package

Last updated - 3/3/2021

This is a package designed to simulate sports players/teams that compete against each other in a head-to-head elemination tournaments. This was created in support of another project for more information/documentation please see [the github repo.](https://github.com/DrJStrudwick/Synthetic-Sport-Player)

Official fully written documentation shall be coming.

There are 3 primary classes contained within this package:
1. `player` These are the teams/players that do the competeing. They are simply defined by a 'skill' level and a variance and whenever they have to 'compete' that is created from a normal distribution defined by these two properties.
2. `tournament` This is an event that a collection of players enter and compete pair-wise with the winners moving forward to the next round, and is complete when there is one player remaining.
3. `season` This is a collection of tournaments that are played in order. at the end of the rounament the players recieve point based on how far they got in tha tournament.

There are two extra child classes that were written to extra both `tournament` and `season` to be able to have 'real-time' functionality for dashboarding purposes. They are:
1. `liveTourn`
2. `liveSeason`
The main difference is their respective `playTourn` and `playSeason` function. In the parent classes the functions would run to completition of the tournament/season. In these child classes they move forward one step in the current tournament.