from numpy.random import normal, randint, rand
import pandas as pd
from random import shuffle
import pickle
import os

class player:
    """
    A class to model any sports player
    """
    def __init__(self,skill,variance,name):
        """
        The init function of the class
        
        [param skill]: int, the underlying 'true' skill of a player
        [param variance]: int, how much the player varies in their performance
        [param name]: str, and id to indtify a player prefferably a int converted to a string
        """
        self.skill = skill
        self.variance = variance
        self.name = name
        self.pointRec=[]
        self.totalPoints=0
        
    def perform(self):
        """
        A function asking the player to perform and returning a numerical value to represent the performance 'on the day'. 
        This is generate from a normal dist. with mean equal to the player skill and var equal to the player variance.
        
        out:
        [performance]: int, the value representing the player performance on the day
        """
        return round(normal(self.skill,self.variance))
    
    def selfsummary(self):
        """
        A function to print out the characteristics of the player.
        """
        outstr = "Name: {}\nSkill: {}\nVar: {}"
        print(outstr.format(self.name,self.skill,self.variance))
        
    def gainPoints(self,points):
        """
        A function to update the current points of the player, their total points is based only on the last 10 groups of points they have gained.
        
        [param points]: int, the points gained by the player
        """
        self.pointRec.append(points)
        if len(self.pointRec)>10:
            self.pointRec.pop(0)
        self.totalPoints = sum(self.pointRec)
    
class match:
    """
    A class to handle the match between two players
    """
    def __init__(self,player1,player2):
        """
        The init function of the class.
        
        [param player1]: player, player1 of the match
        [param player2]: player, player2 of the match
        """
        self.player1 = player1
        self.player2 = player2
    
    def playMatch(self):
        """
        A function to excute the match.
        
        out:
        [winner]: player, the player who won the match
        [loser]: player, the player who lost the match
        [matchSummary]: list, the match info for the records
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
    """
    def __init__(self, playerList,pointPerRound=5):
        """
        The init function of this class.
        
        [param playerList]: list of players: list of players who are participating in this tournament
        [param pointPerRound]: int, the points that a player will recieve at each stage
        """
        self.currentRound = playerList
        self.points=pointPerRound
        self.matchRec=[]
        self.round=1
        self.tournRes=None
    
    def playTourn(self):
        """
        A function to play the entire tournament.
        """
        while len(self.currentRound)>1:
            nextRound = self.playRound()
            self.currentRound = nextRound
            self.round+=1
        self.currentRound[0].gainPoints(self.round*self.points)
        self.tournRes = pd.DataFrame(self.matchRec,columns=["Round", "Match","player1_id","player1_rnkPoints","player1_perform","player2_id","player2_rnkPoints","player2_perform","winner_id"])
        
    def playRound(self):
        """
        A function to play all the matches in the current round.
        
        out:
        [nextRound]: list of players, a list of players who won their matches and proceed through to the next round
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
        A function to reset the tournamet to be able to be played again
        """
        self.matchRec=[]
        self.round=1
        self.tournRes=None
        
def generatePlayers(number):
    """
    A function to generate a numbers of players.
    
    out:
    [playerList]: list of players, a list containing the players created
    [playerInfo]: pandas table, a table with in information about the players created
    """
    playerList = []
    playerinfo = []
    for i in range(0,number):
        skill = randint(1,100)
        var=10
        playerList.append(player(skill,var, str(i)))
        playerinfo.append([str(i),skill,var])
    playerinfo = pd.DataFrame(playerinfo,columns=["name","skill","variance"])
    playerinfo.sort_values("skill",ascending=False,inplace=True)
    return playerList, playerinfo

class season:
    """
    A class to handle a season of tournaments being played.
    """
    def __init__(self,numPlayers=16,tournToPlay=20, players=None, playerSum=None):
        """
        The init function of this class.
        
        [param numPlayers]: int, number of players to have in the season
        [param tournToPlay]: int, number of tournament to play in the season
        [param players]: list of players*, optional - give a pre-existing list of players to use
        [param playerSum]: table*, optional - give a pre-existing table of player summary to use
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
        A function to play out the season of tournaments
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
        A function to reset the season. won't rest the players but resets the week count and the tournament results record. 
        """
        self.week=0
        self.tournRecs=[]
        
    def gatherPoints(self):
        """
        A function to gather the points players have earnt in the tournament and store it in the record
        """
        pointlist=[]
        for player in self.players:
            pointlist.append([player.name,player.totalPoints])
        pointlist=pd.DataFrame(pointlist,columns = ['name','week_'+str(self.week)] )
        self.playerSum = self.playerSum.merge(pointlist, on= 'name')
    
    def export(self,fldr='seasonData'):
        """
        A function to export the players, the tournament results tables, and the season points table as CSVs.
        
        [param path]: str, the name to call the folder.
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
    def __init__(self, playerList,pointPerRound=5):
        super().__init__(playerList,pointPerRound)
    
    def playTourn(self):
        """
        A function to play the entire tournament. When this one is called it will only play the next step
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
    def __init__(self,numPlayers=16,tournToPlay=20, players=None, playerSum=None):
        super().__init__(numPlayers=16,tournToPlay=20, players=None, playerSum=None)
        shuffle(self.players)
        self.currentTourn = liveTourn(self.players)
        self.currentTournComplete = False
        
    def playSeason(self):
        """
        A function to play out the season of tournaments. when it is called it just does one step of the tournament.
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
            
