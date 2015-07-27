import sqlite3
from league_init import League

	
##########################################################
# The following fucntions create all the database tables.
# They should be run only once at the beginning of a new game and need to happen before 
# any class initilization as class creations reference the db tables created by these functions
##########################################################

def create_player_db_table(): # one time only player table initialization
	database.execute('''CREATE TABLE player_db (team_id, league_id, salary, name, age, potential, def_iq, off_iq, 
		decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, height, wingspan, vertical, 
		speed, passing, dribbling, shot_layup, shot_close, shot_midrange, shot_three, shot_ft, steal, rebounding, 
		block, birthday, position)''')


def create_team_db_table():  # one time only team table initialization
	database.execute('''CREATE TABLE team_db (coach_id, league_id, team_name, conference, home_court_advantage,
		possessions, percentage_close, percentage_midrange, percentage_three, percentage_layup, PG_id, SG_id, 
		SF_id, PF_id, CR_id, bench_1_id, bench_2_id, bench_3_id, bench_4_id, bench_5_id, bench_6_id, bench_7_id, 
		bench_8_id, bench_9_id)''')


def create_coach_db_table(): # one time only coach table initilization
	database.execute('''CREATE TABLE coach_db (team_id, name, motivation, coach_off_iq, coach_def_iq, training, 
		leadership, offense_playbook, defense_playbook, coach_rating)''')

def create_league_db_table(): # mostly only using this to load things back from save
	database.execute('''CREATE TABLE league_table (name, number_of_teams, season, how to handle teams)''') ## teams????

def create_season_db_table():
	database.execute('''CREATE TABLE season_table (season_year, league_id, )''') ## questions here, do we include games?


def create_game_db_table():
	database.execute('''CREATE TABLE game_table (home_team_id, away_team_id, home_team_score, away_team_score, league_id, season_id)''') 
	# eventually this should be expanded to include whole boxscore data


def create_budget_db_table():
	database.execute('''CREATE TABLE budget_table(team_id, season_id, season_year, PG_id, SG_id, SF_id, 
		PF_id, CR_id, bench_1_id, bench_2_id, bench_3_id, bench_4_id, bench_5_id, bench_6_id, bench_7_id, 
		bench_8_id, bench_9_id)''') # eventually this should be expanded to include whole boxscore data


def create_blank_db(): # just calls table creation functions
	# opening one connection to the database
	connection = sqlite3.connect('league.db')
	database = connection.cursor()
	print "opening database connection"
	create_league_db_table()
	create_coach_db_table()
	create_season_db_table()
	create_game_db_table()
	create_budget_db_table()
	print "database tables created"
	database.commit()
	print "database tables committed"
	connection.close()
	print "database connection closed"


#####
# need set of functions to take created databases and build classes using the data from the tables
# make sure to account for portions of player classes that should not be run multiple times, probably 
# build some sort of mechanism for determining initial or load creation as that seems like a top-level concern. 
#####


def restore_from_save(league_name):
	



