from numpy.random import normal, randint, rand
import pandas as pd
from random import shuffle
import pickle
import os

class player:
    """
    A class to model any sports player/team.
    
    Parameters
    ----------
    skill : int
            The underlying 'true' skill of a player
    variance : int
               How much the player varies in their performance. The lower this is the more consistent they are in their performance
    name : str
           The players name/id that will be used as a reference later on
    pointLimit : int, default=10
                 The max number of points a player is allowed to keep in the pointRec.
    
    Attributes
    ----------
    pointRec : list of int
               A record of the points the this player has earnt from a tournament in the order that they earnt them.
    totalPoints : int
                  The total of all the points in pointRec.
    """
    def __init__(self,skill,variance,name,pointLimit=10):
        """
        The init method of the class.
        """
        self.skill = skill
        self.variance = variance
        self.name = name
        self.pointRec=[]
        self.totalPoints=0
        self.pointLimit=pointLimit
        
    def perform(self):
        """
        A method getting the player to perform.
        
        A numerical value is returned representing the players performance 'on the day'. 
        This is generate from a normal dist. with mean equal to the player skill and var equal to the player variance, 
        which is then rounded to the nearest integer.
        
        Returns
        -------
        performance : int
                      The value representing the player performance on the day.
        """
        return round(normal(self.skill,self.variance))
    
    def selfsummary(self):
        """
        A method to print out the characteristics of the player.
        """
        outstr = "Name: {}\nSkill: {}\nVar: {}"
        print(outstr.format(self.name,self.skill,self.variance))
        
    def gainPoints(self,points):
        """
        A method to update the current points of the player.
        
        The points provided are added to the players point record. If the number of entries in the pointRec is greater than pointLimit, 
        then the oldest entry is removed. After this the totalPoint arrtibute is updated with the new total of pointRec.
        
        Parameters
        ----------
        points : int
                 Points to be added to the players pointRec.
        """
        self.pointRec.append(points)
        if len(self.pointRec)>self.pointLimit:
            self.pointRec.pop(0)
        self.totalPoints = sum(self.pointRec)
    
class match:
    """
    A class to handle the match between two players.
    
    Parameters
    ----------
    player1 : player
              The first player that is participating in the match.
    player2 : player
              The second player that is participating in the match.
    """
    def __init__(self,player1,player2):
        """
        The init function of the class.
        """
        self.player1 = player1
        self.player2 = player2
    
    def playMatch(self):
        """
        A method to excute the match between players.
        
        Both the perform methods of the players are activated and the player with the higher performance score is the winner. 
        If the two values are equal, then a winner is randomly chosen.
        
        Returns
        -------
        winner : player
                 The player who won the match
        loser : player
                The player who lost the match
        matchReport : list
                      A list containing the information from the match it has just played out. 
                      Containing for both players: their name, their total points, their performance value for that match. 
                      Then finally the name of the player who won.
        """
        p1 = self.player1.perform()
        p2 = self.player2.perform()
        if p1==p2:
            t=(rand()-0.5)
        else:
            t=0
        if (p1+t)>p2:
            return self.player1,self.player2,[self.player1.name,self.player1.totalPoints,p1,self.player2.name,self.player2.totalPoints,p2,self.player1.name]
        else:
            return self.player2,self.player1,[self.player1.name,self.player1.totalPoints,p1,self.player2.name,self.player2.totalPoints,p2,self.player2.name]
        
class tournament:
    """
    A class to model a tournament
    
    The tournament is the classic 1v1 elimination tournament where the winner of a match proceeds through to the next round.
    
    Parameters
    ----------
    playerList : list of players
                 A list containg the players who are competing in this tournament.
    pointPerRound : int, default=5
                    The number of points that a player earns at each stage that they get to.
                    
    Attributes
    ----------
    matchRec :  list of list
                A list where the match results are stored when they are completed.
    round : int
            An integer used to track what current round the tournament is in.
    tournRes : DataFrame
               A pandas dataframe that is created and assigned once the tournament is complete containing all the match results, made from the matchRec attribute.
    
    """
    def __init__(self, playerList,pointPerRound=5):
        """
        The init function of this class.
        """
        self.currentRound = playerList
        self.points=pointPerRound
        self.matchRec=[]
        self.round=1
        self.tournRes=None
    
    def playTourn(self):
        """
        A method to play the entire tournament.
        
        Activating this method will play out the tournament until there is one player remaining as the winner. 
        At which point the final tournament results are created.
        """
        while len(self.currentRound)>1:
            nextRound = self.playRound()
            self.currentRound = nextRound
            self.round+=1
        self.currentRound[0].gainPoints(self.round*self.points)
        self.tournRes = pd.DataFrame(self.matchRec,columns=["Round", "Match","player1_id","player1_rnkPoints","player1_perform","player2_id","player2_rnkPoints","player2_perform","winner_id"])
        
    def playRound(self):
        """
        A method to play all the matches in the current round.
        
        This plays out the round with the players that have made it through to the current stage. Each match result is added to the match record, 
        and the loser gains points equal to the round where they got to.
        
        Returns
        -------
        nextRound : list of players
                    A list of players who won their matches and proceed through to the next round
        """
        nextRound=[]
        for i in range(0,len(self.currentRound)//2):
            currentMatch=match(self.currentRound[2*i],self.currentRound[(2*i)+1])
            winner,loser,res = currentMatch.playMatch()
            loser.gainPoints(self.round*self.points)
            nextRound.append(winner)
            self.matchRec.append([self.round,i+1]+res)
        return nextRound
    
    def reset(self):
        """
        A method to reset the tournamet to be able to be played again
        """
        self.matchRec=[]
        self.round=1
        self.tournRes=None
        
def generatePlayers(number,maxSkill=100,var=10):
    """
    A function to generate a numbers of players.
    
    This will generate the given number of players whose skill is uniformly random between 1 and maxSkill, and whose variance is equal to var.
    
    Parameters
    ----------
    number : int
             The number of players that are to be created.
    maxSkill : int, default=100
               The max skill that a player can have.
    var : int, default=10
          The variance to give to each player.
             
    Returns
    -------
    playerList : list of players
                 A list containing the players created.
    playerInfo : DataFrame
                 A table with information about the players created.
    """
    playerList = []
    playerinfo = []
    for i in range(0,number):
        skill = randint(1,maxSkill)
        playerList.append(player(skill,var, str(i)))
        playerinfo.append([str(i),skill,var])
    playerinfo = pd.DataFrame(playerinfo,columns=["name","skill","variance"])
    playerinfo.sort_values("skill",ascending=False,inplace=True)
    return playerList, playerinfo

class season:
    """
    A class to handle a season of tournaments being played.
    
    A season is a squence of tournaments that are played by a group of players one after another and collect points as they go based 
    on performance in each tournament.
    
    Parameters
    ----------
    numPlayers : int, default=16
                 The number of players that will be generated to play in this season. This will be overridden if players are provided
    tournToPlay : int, default=20
                  The number of tournaments that this season will have,
    players : list of players, default=None
              Optional. If there are pre-existing players that the user wishes to enter into this season. The number of players in the list will override numPlayers. 
    playerSum : DataFrame, default=None
                Optional. If the player are being provided externally then their summary data table can be provided for their total point record to be appended to.
    
    Attributes
    ----------
    week : int
           An integer to keep track of what week (tournament) is being played out.
    tournRecs : list of DataFrames
                A list that stores the results from each tournament.
    """
    def __init__(self,numPlayers=16,tournToPlay=20, players=None, playerSum=None):
        """
        The init method of this class.
        """
        self.tournsToPlay = tournToPlay
        self.week=0
        self.tournRecs=[]
        if players == None:
            self.numPlayers = numPlayers
            self.players, self.playerSum = generatePlayers(self.numPlayers)
        else:
            self.numPlayers = len(players)
            self.players = players
            self.playerSum = playerSum
    
    def playSeason(self):
        """
        A method to play out the season of tournaments.
        
        This method will play all of the tournaments in order, storing tournament results, recording players total points and shuffling the order of players
        inbetween each tournament.
        """
        if self.week == self.tournsToPlay:
            print("This season has already been played. Please reset, use: .rest()")
        while self.week<self.tournsToPlay:
            shuffle(self.players)
            tourn = tournament(self.players)
            tourn.playTourn()
            self.gatherPoints()
            self.tournRecs.append(tourn.tournRes)
            self.week+=1
    
    def reset(self):
        """
        A method to reset the season. 
        
        It won't reset the players but resets the week count and the tournament results record. 
        """
        self.week=0
        self.tournRecs=[]
        
    def gatherPoints(self):
        """
        A method to gather the total points of players aftern a tournament has been completed. These are store it in the playerSum.
        """
        pointlist=[]
        for player in self.players:
            pointlist.append([player.name,player.totalPoints])
        pointlist=pd.DataFrame(pointlist,columns = ['name','week_'+str(self.week)] )
        self.playerSum = self.playerSum.merge(pointlist, on= 'name')
    
    def export(self,fldr='seasonData'):
        """
        A function to export the players, the tournament results tables, and the season points table as CSVs.
        
        Parameters
        ----------
        fldr : str, default='seasonData'
               The name to call the folder the results shall be stored in.
        """
        if fldr in [x for x in os.listdir() if os.path.isdir(x)]:
            pass
        else:
            os.mkdir(fldr)
        file_to_store = open(fldr+"/players.pickle", "wb")
        pickle.dump(self.players, file_to_store)
        file_to_store.close()
        
        for i in range(0,len(self.tournRecs)):
            self.tournRecs[i].to_csv(fldr+"/tournament_"+str(i)+".csv",index=False)
        
        self.playerSum.to_csv(fldr+"/seasonPoints.csv",index=False)
        
        

class liveTourn(tournament):
    """
    A class to facilitate live dashboarding of a season/tournament being played
    
    For further info see the parent class tournament.
    """
    def __init__(self, playerList,pointPerRound=5):
        super().__init__(playerList,pointPerRound)
    
    def playTourn(self):
        """
        A method to play the tournament. 
        
        Unlike it's parent class, when this method is called it will only play the next round of the tournament.
        
        Returns
        -------
        complete : bool
                   A boolean to indicate if the tournament is now complete.
        """
        if len(self.currentRound)>1:
            nextRound = self.playRound()
            self.currentRound = nextRound
            self.round+=1
            if len(self.currentRound)==1:
                self.currentRound[0].gainPoints(self.round*self.points)
                self.tournRes = pd.DataFrame(self.matchRec,columns=["Round", "Match",
                                                                    "player1_id","player1_rnkPoints","player1_perform",
                                                                    "player2_id","player2_rnkPoints","player2_perform","winner_id"])
                return True
            else:
                return False
        else:
            return True
        
class liveSeason(season):
    """
    A class to facilitate live dashboarding of a season/tournament being played
    
    For further info see the parent class season.
    
    Attributes
    ----------
    currentTourn : liveTourn
                   The current tournament that is in progress
    currentTournComplete : bool
                           A boolean indicating if the current tournament is completed or not.
    """
    def __init__(self,numPlayers=16,tournToPlay=20, players=None, playerSum=None):
        super().__init__(numPlayers=16,tournToPlay=20, players=None, playerSum=None)
        shuffle(self.players)
        self.currentTourn = liveTourn(self.players)
        self.currentTournComplete = False
        
    def playSeason(self):
        """
        A method to play the season.
        
        Unlike it's parent class, when this method is called it will only play the next round of the tournament. But if the tournament is complete 
        it will update the records and move onto make the next tournament and play the first round.
        
        Returns
        -------
        complete : bool
                   A boolean indicating if the season is completed or not.
        """
        if self.week == self.tournsToPlay:
            return True
        else:
            if self.currentTournComplete:
                shuffle(self.players)
                self.currentTourn = liveTourn(self.players)

            self.currentTournComplete = self.currentTourn.playTourn()
            if self.currentTournComplete:
                self.gatherPoints()
                self.tournRecs.append(self.currentTourn.tournRes)
                self.week+=1
            return False
            
