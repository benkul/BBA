import sqlite3
#from league_init import League

	
##########################################################
# The following fucntions create all the database tables.
# They should be run only once at the beginning of a new game and need to happen before 
# any class initilization as class creations reference the db tables created by these functions
##########################################################




def create_blank_db(): # just calls table creation functions
	# opening one connection to the database
	connection = sqlite3.connect('league.db')
	database = connection.cursor()
	print "opening database connection"
	database.execute('''CREATE TABLE league_table (Id integer primary key, name)''') 
	# the name here is supplied by the user and required to load a saved game

	
	database.execute('''CREATE TABLE player_db (Id integer primary key,
		league_id REFERENCES league_table(Id), 
		team_id REFERENCES team_db(Id), 
		salary, name, age, potential, def_iq, off_iq, decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, 
		height, wingspan, vertical, speed, passing, dribbling, shot_layup, shot_close, shot_midrange, shot_three, shot_ft, steal, rebounding, 
		block, birthday, position, role)''')

	database.execute('''CREATE TABLE coach_db (Id integer primary key, 
		league_id REFERENCES league_table(Id), 
		team_id REFERENCES team_db(Id), 
		name, motivation, coach_off_iq, coach_def_iq, training, 
		leadership, offense_playbook, defense_playbook, coach_rating)''')
	

	database.execute('''CREATE TABLE team_db (Id, integer primary key, 
		league_id REFERENCES league_table(Id), 
		coach_id REFERENCES coach_db(Id), 
		PG_id REFERENCES player_db(Id), 
		SG_id REFERENCES player_db(Id), 
		SF_id REFERENCES player_db(Id), 
		PF_id REFERENCES player_db(Id),
		CR_id REFERENCES player_db(Id),
		bench_1_id REFERENCES player_db(Id),
		bench_2_id REFERENCES player_db(Id),
		bench_3_id REFERENCES player_db(Id),
		bench_4_id REFERENCES player_db(Id),
		bench_5_id REFERENCES player_db(Id),
		bench_6_id REFERENCES player_db(Id),
		bench_7_id REFERENCES player_db(Id),
		bench_8_id REFERENCES player_db(Id),
		bench_9_id REFERENCES player_db(Id),
		team_name, conference, home_court_advantage,
		possessions, percentage_close, percentage_midrange, percentage_three, percentage_layup)''')
	# one time only coach table initilization

	database.execute('''CREATE TABLE season_table (Id integer primary key, 
		league_id REFERENCES league_table(Id), 
		season_year)''')

	database.execute('''CREATE TABLE game_table (Id integer primary key, 
		league_id REFERENCES league_table(Id), 
		season_id REFERENCES season_table(Id),
		home_team_id REFERENCES team_db(Id),
		away_team_id REFERENCES team_db(Id),
		home_team_score, away_team_score)''') 
	# eventually this should be expanded to include whole boxscore data, references to player PK etc. 

	database.execute('''CREATE TABLE budget_table(Id integer primary key, 
		league_id REFERENCES league_table(Id),
		team_id REFERENCES team_db(Id), 
		season_id REFERENCES season_table(Id))''') ## big questions about how to handle player costs, etc
	
	print "database tables created"
	connection.commit()
	print "database tables committed"
	connection.close()
	print "database connection closed"


#create_blank_db()


def dump_database():
	connection = sqlite3.connect('league.db')
	database = connection.cursor()
	database.execute('PRAGMA writable_schema = 1')
	database.execute('''delete from sqlite_master where type in ("table", "index", "trigger")''')
	database.execute('PRAGMA writable_schema = 0')
	print "database tables, indexes and triggers dropped"
	print "creating blank tables"
	create_blank_db()
	print "blank tables created, commiting and closing connection"
	connection.commit()
	connection.close()
	
dump_database()

#####
# need set of functions to take created databases and build classes using the data from the tables
# make sure to account for portions of player classes that should not be run multiple times, probably 
# build some sort of mechanism for determining initial or load creation as that seems like a top-level concern. 
#####


def restore_from_save(league_name):
	pass




