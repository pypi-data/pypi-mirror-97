import pandas as pd
def getPlayerHist(pid,df):
    """
    A function to get all the matches of a given player that reside in the provided dataframe.
    
    Parameters
    ----------
    pid : str
          The name of the player whose match results are to be searched for. This should be the players '.name' atrribute
    df : DataFrame
         The DataFrame that contains match results
    
    Returns
    -------
    pid_df : DataFrame
             A DataFrame that contains match results that the given player has participated in.
    """
    if type(pid)!=str:
        raise TypeError("pid must be a str")
    if type(df)!=pd.core.frame.DataFrame:
        raise TypeError("df must be a pandas dataframe")
        
    tk1='player1'
    tk2='player2'
    other = [x for x in list(df.columns) if not("_" in x)]
    ext = list(set([y.split('_')[1] for y in [x for x in list(df.columns) if ("_" in x)]]))
    
    pid_df = df[(df[tk1+'_'+ext[0]]==pid)]
    pid_df.winner_id=(pid_df["winner_id"]==pid)
    pid_df.rename(columns=dict(zip([tk1+"_"+x for x in ext]+[tk2+"_"+x for x in ext],
                                   ["player_"+x for x in ext]+["opponent_"+x for x in ext])),inplace=True)

    pid2_df = df[(df[tk2+'_'+ext[0]]==pid)]
    pid2_df.winner_id=(pid2_df["winner_id"]==pid)
    pid2_df.rename(columns=dict(zip([tk2+"_"+x for x in ext]+[tk1+"_"+x for x in ext],
                                    ["player_"+x for x in ext]+["opponent_"+x for x in ext])),inplace=True)

    pid_df = pd.concat([pid_df,pid2_df])
    pid_df.sort_values(by=["Tourn","Round","Match"],ascending=[False,False,True],inplace=True)

    return pid_df

def getMatchUpData(pid1,pid2,df):
    """
    A function to get all the matches between two players that reside in the provided dataframe.
    
    Parameters
    ----------
    pid1 : str
          The name of a player whose match results are to be searched for. This should be the players '.name' atrribute
    pid2 : str
          The name of the other player whose match results are to be searched for. This should be the players '.name' atrribute
    df : DataFrame
         The DataFrame that contains match results
    
    Returns
    -------
    mu_df : DataFrame
             A DataFrame that contains match results that the two player has participated in against each other.
    """
    if type(pid1)!=str:
        raise TypeError("pid1 must be a str")
    if type(pid2)!=str:
        raise TypeError("pid2 must be a str")
    if type(df)!=pd.core.frame.DataFrame:
        raise TypeError("df must be a pandas dataframe")
        
    mu_df = df[((df["player1_id"]==pid1)&(df["player2_id"]==pid2)|(df["player1_id"]==pid2)&(df["player2_id"]==pid1))]
    mu_df.sort_values(by=["Tourn","Round","Match"],ascending=[False,False,True],inplace=True)
    return mu_df
