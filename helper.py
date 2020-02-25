
import pandas as pd




def filterPoints(player, points, sORrCol=None, result=None, wORlCol=None, resultCol='result'):
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


def m_splitdata(match_dataframe, validation_year, test_year, date_column='date', gender_column='gender', gender=None):
	'''Splits data into validation and test data.
	Training data will be calculated later and applied to validation data.
	Returns validation dataframe, test dataframe in that order '''
 
	# Filter on gender
	if gender is not None:
		match_dataframe = match_dataframe.loc[match_dataframe[gender_column]==gender]

	# Filter by date range to create test
	data_test = match_dataframe.loc[match_dataframe[date_column].dt.year==test_year]
	data_test.reset_index(inplace=True)
	data_test.drop(columns=['index'], inplace=True)

	# Filter by date range to create validation data
	data_validation = match_dataframe.loc[match_dataframe[date_column].dt.year==validation_year]
	data_validation.reset_index(inplace=True)
	data_validation.drop(columns=['index'], inplace=True)

	return data_validation, data_test


def m_splitdata(match_dataframe, validation_year, test_year, date_column='date', gender_column='gender', gender=None):
	'''Splits data into validation and test data.
	Training data will be calculated later and applied to validation data.
	Returns validation dataframe, test dataframe in that order '''

	# Filter on gender
	if gender is not None:
		match_dataframe = match_dataframe.loc[match_dataframe[gender_column]==gender]

	# Filter by date range to create test
	data_test = match_dataframe.loc[match_dataframe[date_column].dt.year==test_year]
	data_test.reset_index(inplace=True)
	data_test.drop(columns=['index'], inplace=True)

	# Filter by date range to create validation data
	data_validation = match_dataframe.loc[match_dataframe[date_column].dt.year==validation_year]
	data_validation.reset_index(inplace=True)
	data_validation.drop(columns=['index'], inplace=True)

	return data_validation, data_test


def m_createdataframeformodel(match_row, match_dataframe, stats_dataframe, train_numyears, player1_column = 'player1', player2_column='player2', date_column='date'):
	'''Given a row (in validation data) and number of years,
	compute averages for each player then take differences
	and append to row. 
	Returns dictionary'''
	
	player1 = match_row[player1_column]
	player2 = match_row[player2_column]
	date = match_row[date_column]

	# Create a dictionary version of the row
	row_dict = dict(match_row)

	# Filter data to date range for validation data
	date_max = date - pd.Timedelta(1, unit='d')
	date_min = date_max - pd.Timedelta(train_numyears, unit='Y')
	data_train = match_dataframe.loc[(match_dataframe[date_column]>=date_min) & (match_dataframe[date_column]<=date_max)]


	playerstatsdict = {}

	# Initialize dictionary
	# Iterate through each player
	for player in [player1, player2]:
		# Filter to matches where player is involved
		data_train_player = data_train.loc[(data_train[player1_column]==player)|(data_train[player2_column]==player)]

		# Get player in a column
		data_train_player['player'] = player


		# Distinguish non-metric columns vs metric columns
		original_columns = data_train_player.columns
	
		# Merge stats on player
		data_train_player = pd.merge(data_train_player, stats_dataframe, left_on=['player', 'matchLink'], right_on = ['player',  'matchLink'], how='left')
		data_train_player.dropna(inplace=True)

		# Distinguish metric columns
		metric_columns = data_train_player.columns[len(original_columns):]

		# Get stats for each player
		stats_dict = dict(data_train_player[metric_columns].agg('mean'))
		
		# Append to dictionary
		playerstatsdict[player] = stats_dict

	# Combine the two players' stats to get difference
	playerstats_diff = {x: playerstatsdict[player1][x] - playerstatsdict[player2][x] for x in playerstatsdict[player1] if x in playerstatsdict[player2]}

	# Add the difference stats to the row
	row_dict.update(playerstats_diff)

	return row_dict
