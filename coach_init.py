import random
import sqlite3
from game_variables import motivation, coach_off_iq, coach_def_iq, training, offense_playbook, defense_playbook, leadership, major_bonus
from coach_first_names import coach_first_names
from player_last_names import player_last_names


def create_stat(stat): # assumes a min/max tuple as input 
	min = stat[0]	   # helper function that aids in class object creation
	max = stat[1]
	selection = random.randrange(min, max)	
	return selection



# Coach database structure for future reference
# database.execute('''CREATE TABLE coach_db (Id integer primary key, 
# 	league_id REFERENCES league_table(Id), 
# 	team_id REFERENCES team_db(Id), 
# 	name, motivation, coach_off_iq, coach_def_iq, training, 
# 	leadership, offense_playbook, defense_playbook, coach_rating)''')




class Coach:
	def __init__(self):
		self.league_id = 0 # invalid pk value as default, needs to be overridden before being stuffed into db
		self.team = 0 # invalid pk value as default, needs to be overridden before being stuffed into db

	def update_coach(self): # updates every coach field except for name
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		coach_attributes = (self.league_id, self.team, self.motivation, self.coach_off_iq, self.coach_def_iq, self.training, self.leadership, self.offense_playbook, self.defense_playbook, self.coach_rating, self.name)
		database.execute('''UPDATE coach_db 
			SET league_id = ?,
			team_id = ?, 
			motivation = ?,
			coach_off_iq = ?,
			coach_def_iq = ?,
			training = ?,
			leadership = ?,
			offense_playbook = ?,
			defense_playbook = ?,
			coach_rating = ?
			WHERE 'name' = ?''', coach_attributes)
		print "coach", self.name,  "updated"
		connection.commit()
		connection.close()

	def create_coach(self, league_id):
		self.league_id = league_id
		self.name = random.choice(coach_first_names) + " " + random.choice(player_last_names)
		self.motivation = create_stat(motivation)
		self.coach_off_iq = create_stat(coach_off_iq)
		self.coach_def_iq = create_stat(coach_def_iq)
		self.training = create_stat(training)
		self.leadership = create_stat(leadership)
		self.offense_playbook = offense_playbook[str(random.randint(1,3))]
		self.defense_playbook = defense_playbook[str(random.randint(1,3))]
		
		def rating_boost(): # because every coach should be good at 1 thing in the very least
			to_boost = random.randint(1,5)
			if to_boost == 1:
				major_bonus(self.motivation)
				return self.motivation
			elif to_boost == 2:
				major_bonus(self.coach_off_iq)
				return self.coach_off_iq
			elif to_boost == 3:
				major_bonus(self.coach_def_iq)
				return self.coach_def_iq				
			elif to_boost == 4:
				major_bonus(self.training)
				return self.training
			elif to_boost == 5:
				major_bonus(self.leadership)

		def coach_rating():
			total = self.motivation + self.coach_off_iq + self.coach_def_iq + self.training + self.leadership
			rating = int(total / 4.5)
			return rating

		def insert_coach(self): # puts the coach class object into the coach database table
			connection = sqlite3.connect('league.db')
			database = connection.cursor()
			coach_attributes = (self.league_id, self.team, self.name, self.motivation, self.coach_off_iq, self.coach_def_iq, self.training, self.leadership, self.offense_playbook, self.defense_playbook, self.coach_rating)
			database.execute('''INSERT INTO coach_db
				(league_id, team_id, name, motivation, coach_off_iq, coach_def_iq, training,leadership, offense_playbook, defense_playbook, coach_rating) 
				VALUES(?,?,?,?,?,?,?,?,?,?,?)''', coach_attributes)
			connection.commit()
			connection.close()

		rating_boost()
		self.coach_rating = coach_rating()
		insert_coach(self)

		
def load_coaches(league_pk, number_of_coaches):
	connection = sqlite3.connect('league.db')
	database = connection.cursor()
	league_id = league_pk
	coach_pool = []
	database.execute('''SELECT league_id, team_id, name, motivation, coach_off_iq, coach_def_iq, training,leadership, offense_playbook, defense_playbook, coach_rating FROM coach_db WHERE league_id = ?''', league_id)
	for coach in range(number_of_coaches):		
		coach_attributes = database.fetchone()
		coach_pool.append(Coach())
		print "attempting coach resurrection"
		coach_pool[coach].league_id = coach_attributes[0]
		coach_pool[coach].team = coach_attributes[1]
		coach_pool[coach].name = coach_attributes[2]
		coach_pool[coach].motivation = coach_attributes[3]
		coach_pool[coach].coach_off_iq = coach_attributes[4]
		coach_pool[coach].coach_def_iq = coach_attributes[5]
		coach_pool[coach].training = coach_attributes[6]
		coach_pool[coach].leadership = coach_attributes[7]
		coach_pool[coach].offense_playbook = coach_attributes[8]
		coach_pool[coach].defense_playbook = coach_attributes[9]
		coach_pool[coach].coach_rating = coach_attributes[10]
		print coach_pool[coach].name, " resurrected"
	return coach_pool
