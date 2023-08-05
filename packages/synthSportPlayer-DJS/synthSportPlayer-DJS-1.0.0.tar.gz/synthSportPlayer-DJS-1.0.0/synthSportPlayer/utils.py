import pandas as pd
def getPlayerHist(pid,df):
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
    mu_df = df[((df["player1_id"]==pid1)&(df["player2_id"]==pid2)|(df["player1_id"]==pid2)&(df["player2_id"]==pid1))]
    mu_df.sort_values(by=["Tourn","Round","Match"],ascending=[False,False,True],inplace=True)
    return mu_df
