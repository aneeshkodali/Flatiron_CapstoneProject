
import pandas as pd




def getServeOrReturnMetricDF(player, points, sORrCol=None, result=None, wORlCol=None, resultCol='result'):
    '''Calculates metric for given arguments
    Args
        - player = player name
        - points = points dataframe
        - sORrCol = 'server', 'receiver'
        - result = result of interest (ace, double fault, winner, ...)
        - wORlCol = 'winner', 'loser'
    Returns dataframe
    '''

    # Filter out any weird points
    points = points.loc[~(points['result'].isin(['None', 'challenge was incorrect']))]
    
    # Filter server or receiver column to player
    if sORrCol is not None:
        points = points.loc[points[sORrCol]==player]
    # Filter results column
    if result is not None:
        points = points.loc[points[resultCol]==result]
    # Filter winner or loser column to player
    if wORlCol is not None:
        points = points.loc[points[wORlCol]==player]
    return points