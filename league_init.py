import random
import sqlite3
from team_init import Team
from coach_init import Coach, load_coaches
from player_init import Player, load_players
from player_init import cm_to_in, rating_to_letter_grade
from coach_first_names import coach_first_names
from player_last_names import player_last_names
from game_variables import team_name_options, salary_cap, number_of_teams, number_of_players
from schedule import return_schedule


class League:
	def __init__(self, name):
		self.id = 0
		self.name = name
		self.number_of_teams = number_of_teams
		self.team_name_pool = team_name_options
		self.salary_cap = salary_cap
	#########################
	#
	# funcions for new game league creation
	#
	#########################
	def insert_league(self):
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		league_attributes = [self.name]
		database.execute('''SELECT count(DISTINCT name) FROM league_table WHERE name = ?''', league_attributes)
		choice = database.fetchone()
		while choice[0] != 0: # we don't want saved games with the same name
			print "saved game already exists for league named ", self.name
			new_name = raw_input("please enter a new name: ")
			new_name = str(new_name)  ## this seeems a little in-elegant, but it works well enough
			setattr(self, 'name', new_name)
			league_attributes = [self.name]
			database.execute('''SELECT count(DISTINCT name) FROM league_table WHERE name = ?''', league_attributes)
			choice = database.fetchone()
				

		database.execute('''INSERT INTO league_table
			(name) VALUES(?)''', league_attributes)
		database.execute('''SELECT Id FROM league_table WHERE name = ?''', league_attributes)
		new_id = database.fetchone()
		setattr(self, 'id', new_id[0])
		print self.id, new_id[0]
		connection.commit()
		connection.close()
		#########################
		# database table creation for reference
		#
		# database.execute('''CREATE TABLE league_table (Id integer primary key, name)''') 
		#########################

	def get_coaches(self):
		league_id = self.id
		coaches = []
		number_of_coaches = (self.number_of_teams + 6) # make more coaches than needed
		for item in range(number_of_coaches):
			coaches.append(Coach())
			coaches[item].create_coach(league_id)
			coaches[item].update_coach()
		return coaches


	def get_new_player_pool(self):
		all_players = {}
		for item in range(number_of_players):
			new_player = Player(self.id) # id is the league pk
			new_player.player_set_position()
			new_player.insert_player()
			all_players[new_player.db_id] = new_player
		return all_players

	def make_teams(self, coach_pool, team_name_pool):
		#print team_name_pool
		league_teams = {}
		# initialize team db here
		league_id = self.id
		for item in range(self.number_of_teams):
			coach = coach_pool.pop()
			choice = random.randrange(0, len(team_name_pool))
			team_name = team_name_pool.pop(choice)
			setattr(coach, 'team', team_name)
			print coach.team
			coach.update_coach()
			print coach, team_name, league_id
			league_teams[team_name] = Team(coach, team_name, league_id) # create the team class objects
		return league_teams

	def assign_to_conference(self, team_pool, number_of_teams):
		team_list = []
		for item in team_pool:
			team_list.append(team_pool[item].team_name)

		#print team_list
		eastern_conference = []
		western_conference = []
		conferences = {}
		for key in range(number_of_teams / 2):
			eastern_conference.append(team_list.pop())
			western_conference.append(team_list.pop())  
		conferences["eastern"] = eastern_conference
		conferences["western"] = western_conference
		# update team dicts here to reference conferences
		return conferences

	def draft_players(self, player_pk_pool, team_pool):
		# TO DO: sort player pool by quality of player
		temp_pool = []

		for item in player_pk_pool:
			temp_pool.append(item)

		players_to_draft = [
		"PG", 
		"SG", 
		"SF",
		"PF",
		"C",
		"bench_1",
		"bench_2",
		"bench_3",
		"bench_4",
		"bench_5",
		"bench_6",
		"bench_7",
		"bench_8",
		"bench_9"
		]
		for round in players_to_draft: # for each round in the draft
			for team in team_pool: # go team by team
				for player_pk in temp_pool: # check the player pool
					if self.player_pool[player_pk].position == round or round[0] == 'b': # if they match the round, or the round starts with "bench"
						# assign to team player dict
						# remove from draft pool
						team_pool[team].players[round] = temp_pool.pop(temp_pool.index(player_pk))
						self.player_pool[player_pk].change_role(round) # update the players role for the team
						print team_pool[team].team_name, " drafted ", self.player_pool[player_pk].name, " for position ", round
						break
		for team in team_pool:
			#####
			# need to be using the db id for each player, coach, etc if they're being referenced as pk in team db
			# grab the id for each player and coach
			####
			pass







	##############################
	# The following should only be run when creating a brand new league, 
	# otherwise these should be built from the database class object extractions
	##############################
	def create_league(self):
		try: 
			if self.team_pool: 
				pass
		except AttributeError:
			print "league teams do not exist, creating now"
			self.insert_league()
			self.coach_pool = self.get_coaches()
			self.player_pool = self.get_new_player_pool()

			self.team_pool = self.make_teams(self.coach_pool, self.team_name_pool)

			self.conferences = self.assign_to_conference(self.team_pool, self.number_of_teams)

			self.draft_players(self.player_pool, self.team_pool)

			self.league_schedule = return_schedule(self.conferences['eastern'], self.conferences['western'])

			#self.insert_league()
			print "league creation success"
			pass

	#########################
	#
	# funcions for loading a saved game
	#
	#########################
	def load_league(self, league_pk):
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		print league_pk
		database.execute('''SELECT COUNT(name) FROM coach_db WHERE league_id = ?''', league_pk)
		coaches = database.fetchall()
		self.coach_pool = load_coaches(league_pk) # get a list with the coach objects in it
		self.player_pool = load_players(league_pk)



new_or_old = str(raw_input('start a new game or load one? \ntype new or load: '))


if new_or_old == 'new':
	league_namer = str(raw_input('enter a name for the league: ')) 

	test_league = League(league_namer)

	test_league.create_league()

else:
	connection = sqlite3.connect('league.db')
	database = connection.cursor()
	league_name = raw_input("Enter the name of the league you'd like to load: ")
	league_name = [league_name]

	database.execute('''SELECT count(DISTINCT name) FROM league_table WHERE name = ?''', league_name)
	choice = database.fetchone()
	while choice[0] != 1: # we expect to find only one database object with the name passed by user
		print "saved game named ", league_name, " not found."
		league_name = ''
		league_name = raw_input("please enter the name of the league you'd like to load, \nenter 'ZZZZ' to see a list of saved game names: ")
		league_name = [str(league_name)]  
		if league_name[0] == 'ZZZZ':
			database.execute('''SELECT name FROM league_table''')
			show_all = database.fetchall()
			print show_all
		database.execute('''SELECT count(DISTINCT name) FROM league_table WHERE name = ?''', league_name)
		choice = database.fetchone()
	
	database.execute('''SELECT Id FROM league_table WHERE name = ?''', league_name)
	league_pk = database.fetchone()
	print "league key ", league_pk
	test_league = League(league_name[0])
	test_league.load_league(league_pk)

# for item in self.team_pool:
# 	print item, "team schedule"
# 	for line in self.league_schedule:
# 		if item == line[0]:
# 			print "vs", line[1] 
# 		elif item == line[1]:
# 			print "@", line[0]
# 		else: 
# 			pass
# 	print "xxxxxxxxxxxxxxxx"
