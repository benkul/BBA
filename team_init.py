from game_variables import budget
import sqlite3
import random


# database.execute('''CREATE TABLE team_db (Id, integer primary key, 
# 	league_id REFERENCES league_table(Id), 
# 	coach_id REFERENCES coach_db(Id), 
# 	PG_id REFERENCES player_db(Id), 
# 	SG_id REFERENCES player_db(Id), 
# 	SF_id REFERENCES player_db(Id), 
# 	PF_id REFERENCES player_db(Id),
# 	CR_id REFERENCES player_db(Id),
# 	bench_1_id REFERENCES player_db(Id),
# 	bench_2_id REFERENCES player_db(Id),
# 	bench_3_id REFERENCES player_db(Id),
# 	bench_4_id REFERENCES player_db(Id),
# 	bench_5_id REFERENCES player_db(Id),
# 	bench_6_id REFERENCES player_db(Id),
# 	bench_7_id REFERENCES player_db(Id),
# 	bench_8_id REFERENCES player_db(Id),
# 	bench_9_id REFERENCES player_db(Id),
# 	team_name, conference, home_court_advantage,
# 	possessions, percentage_close, percentage_midrange, percentage_three, percentage_layup)''')

class Team:
	def __init__(self, coach, team_name, league_id):
		self.league_id = league_id
		self.coach = coach
		self.id = 0 # default value, gets replaced with db primary key once there is one
		self.team_name = team_name
		# will eventually need to make these things dynamic instead of static and load them from db
		self.budget = 100
		self.home_court_advantage = random.randrange(50,100)
		self.possessions = 100
		self.percentage_close = .25
		self.percentage_midrange = .25
		self.percentage_three = .25
		self.percentage_layup =  .25
		self.conference = ''
		# the rest is static
		self.players = {
		"PG" : "", 
		"SG" : "", 
		"SF" : "",
		"PF" : "",
		"CR" : "",
		"bench_1" : "",
		"bench_2" : "",
		"bench_3" : "",
		"bench_4" : "",
		"bench_5" : "",
		"bench_6" : "",
		"bench_7" : "",
		"bench_8" : "",
		"bench_9" : ""
		}
		self.player_list = ["PG", "SG", "SF", "PF", "CR", "bench_1", "bench_2", 
		"bench_3", "bench_4", "bench_5", "bench_6", "bench_7", "bench_8", "bench_9"]

	def ft_percentage(self):
		total = 0
		for key in self.player_list:
			total += self.players[key].shot_ft
		total /= 14
		return total	

	def close_percentage(self):
		total = 0
		for key in self.player_list:
			total += self.players[key].shot_close
		total /= 14
		return total 

	def layup_percentage(self):
		total = 0
		for key in self.player_list:
			total += self.players[key].shot_layup
		total /= 14
		return total

	def three_percentage(self):
		total = 0
		for key in self.player_list:
			total += self.players[key].shot_three
		total /= 14
		return total

	def midrange_percentage(self):
		total = 0
		for key in self.player_list:
			total += self.players[key].shot_midrange
		total /= 14
		return total

	def update_team(self):
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		team_attributes = (self.league_id, self.coach, self.players['PG'], self.players['SG'], self.players['SF'], 
			self.players['PF'], self.players['CR'], self.players['bench_1'], self.players['bench_2'], self.players['bench_3'],
			self.players['bench_4'], self.players['bench_5'], self.players['bench_6'], self.players['bench_7'], self.players['bench_8'], 
			self.players['bench_9'], self.team_name, self.conference, self.home_court_advantage, self.possessions, self.percentage_close, 
			self.percentage_midrange, self.percentage_three, self.percentage_layup, self.league_id, self.id)
		database.execute('''UPDATE team_db
			SET league_id = ?,
			coach_id = ?,
			PG_id = ?,
			SG_id = ?,
			SF_id = ?,
			PF_id = ?,
			CR_id = ?,
			bench_1_id = ?,
			bench_2_id = ?,
			bench_3_id = ?,
			bench_4_id = ?,
			bench_5_id = ?,
			bench_6_id = ?,
			bench_7_id = ?,
			bench_8_id = ?,
			bench_9_id = ?,
			team_name = ?,
			conference = ?,
			home_court_advantage = ?,
			possessions = ?,
			percentage_close = ?,
			percentage_midrange = ?,
			percentage_three = ?,
			percentage_layup = ?
			WHERE 'league_id' = ? AND 'Id' = ?''', team_attributes)
		print self.team_name, " updated "
		connection.commit()
		connection.close()

	def insert_team(self):
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		team_attributes = (self.league_id, self.coach, self.players['PG'], self.players['SG'], self.players['SF'], 
			self.players['PF'], self.players['CR'], self.players['bench_1'], self.players['bench_2'], self.players['bench_3'],
			self.players['bench_4'], self.players['bench_5'], self.players['bench_6'], self.players['bench_7'], self.players['bench_8'], 
			self.players['bench_9'], self.team_name, self.conference, self.home_court_advantage, self.possessions, self.percentage_close, 
			self.percentage_midrange, self.percentage_three, self.percentage_layup)
		database.execute('''INSERT INTO team_db
			(league_id, coach_id, PG_id, SG_id, SF_id, PF_id, CR_id, bench_1_id, bench_2_id, bench_3_id, bench_4_id, 
			bench_5_id, bench_6_id, bench_7_id, bench_8_id, bench_9_id, team_name, conference, home_court_advantage,
			possessions, percentage_close, percentage_midrange, percentage_three, percentage_layup)
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', team_attributes)
		connection.commit()
		connection.close()

	def set_db_id(self): # updates a teams database id from default 0 to actual db primary key
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		team_attributed = (int(self.league_id), str(self.name))
		database.execute('''SELECT Id FROM team_db WHERE league_id = ? AND name = ?''', team_attributed)
		id_number = database.fetchone()
		self.id = id_number
		connection.commit()
		connection.close()

# database.execute('''CREATE TABLE team_db (Id, integer primary key, 
# 	league_id REFERENCES league_table(Id), 
# 	coach_id REFERENCES coach_db(Id), 
# 	PG_id REFERENCES player_db(Id), 
# 	SG_id REFERENCES player_db(Id), 
# 	SF_id REFERENCES player_db(Id), 
# 	PF_id REFERENCES player_db(Id),
# 	CR_id REFERENCES player_db(Id),
# 	bench_1_id REFERENCES player_db(Id),
# 	bench_2_id REFERENCES player_db(Id),
# 	bench_3_id REFERENCES player_db(Id),
# 	bench_4_id REFERENCES player_db(Id),
# 	bench_5_id REFERENCES player_db(Id),
# 	bench_6_id REFERENCES player_db(Id),
# 	bench_7_id REFERENCES player_db(Id),
# 	bench_8_id REFERENCES player_db(Id),
# 	bench_9_id REFERENCES player_db(Id),
# 	team_name, conference, home_court_advantage,
# 	possessions, percentage_close, percentage_midrange, percentage_three, percentage_layup)''')
def load_team(self, league_pk):
	pass

