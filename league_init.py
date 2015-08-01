import random
import sqlite3
from create_team import Team
from coach_init import Coach, load_coaches
from player_init import Player, Point_guard, Shooting_guard, Small_forward, Power_forward, Center
from player_init import cm_to_in, rating_to_letter_grade
from coach_first_names import coach_first_names
from player_last_names import player_last_names
from game_variables import team_name_options, salary_cap, number_of_teams
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
		# database table creation for reference
		# database.execute('''CREATE TABLE league_table (Id integer primary key, name)''') 


	def get_coaches(self):
		league_id = self.id
		coaches = []
		draft_order = []
		number_of_coaches = (self.number_of_teams + 6) # make more coaches than needed
		for item in range(number_of_coaches):
			coaches.append(Coach())
			coaches[item].create_coach(league_id)
			coaches[item].update_coach()

		return coaches
	

	def get_pg_pool(self):
		pg_pool = []
		all_players = {}
		number_of_players = (self.number_of_teams * 5)
		for item in range(number_of_players):
			all_players[item] = Point_guard()
			all_players[item].insert_player()
			pg_pool.append((all_players[item].overall_rating, all_players[item]))
		return pg_pool

	def get_sg_pool(self):
		sg_pool = []
		all_players = {}
		number_of_players = (self.number_of_teams * 5)
		for item in range(number_of_players):
			all_players[item] = Shooting_guard()
			sg_pool.append((all_players[item].overall_rating, all_players[item]))
		return sg_pool		

	def get_sf_pool(self):
		sf_pool = []
		all_players = {}			
		number_of_players = (self.number_of_teams * 5)
		for item in range(number_of_players):
			all_players[item] = Small_forward()
			sf_pool.append((all_players[item].overall_rating, all_players[item]))
		return sf_pool

	def get_pf_pool(self):
		pf_pool = []
		all_players = {}			
		number_of_players = (self.number_of_teams * 5)
		for item in range(number_of_players):
			all_players[item] = Power_forward()
			pf_pool.append((all_players[item].overall_rating, all_players[item]))
		return pf_pool

	def get_cr_pool(self):
		cr_pool = []
		all_players = {}			
		number_of_players = (self.number_of_teams * 5)
		for item in range(number_of_players):
			all_players[item] = Center()
			cr_pool.append((all_players[item].overall_rating, all_players[item]))
		return cr_pool

	def make_teams(self, coach_pool, team_name_pool):
		#print team_name_pool
		league_teams = {}
		# initialize team db here
		for item in range(self.number_of_teams):
			coach = coach_pool.pop()
			choice = random.randrange(0, len(team_name_pool))
			team_name = team_name_pool.pop(choice)
			setattr(coach, 'team', team_name)
			print coach.team
			coach.update_coach()
			league_teams[team_name] = Team(coach, team_name)
		return league_teams

	def assign_to_conference(self, team_dict, number_of_teams):
		team_list = []
		for key in team_dict:
			team_list.append(team_dict[key].team_name)

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

	def draft_players(self, pg_pool, sg_pool, sf_pool, pf_pool, cr_pool, team_dict):
		pg_pool.sort()
		sg_pool.sort()
		sf_pool.sort()
		pf_pool.sort()
		cr_pool.sort()
		for key in team_dict:
			team_dict[key].players['PG'] = pg_pool[len(pg_pool)- 1][1]
			pg_pool.pop()
			#print "The", team_dict[key].team_name, "select", team_dict[key].players['PG'].name, team_dict[key].players['PG'].show_overall_rating()
		for key in team_dict:
			team_dict[key].players['SG'] = sg_pool[len(sg_pool) - 1][1]
			sg_pool.pop()
			#print "The", team_dict[key].team_name, "select", team_dict[key].players['SG'].name, team_dict[key].players['SG'].show_overall_rating()
		for key in team_dict:
			team_dict[key].players['SF'] = sf_pool[len(sf_pool) - 1][1]
			sf_pool.pop()
			#print "The", team_dict[key].team_name, "select", team_dict[key].players['SF'].name, team_dict[key].players['SF'].show_overall_rating()
		for key in team_dict:
			team_dict[key].players['PF'] = pf_pool[len(pf_pool) - 1][1]
			pf_pool.pop()
			#print "The", team_dict[key].team_name, "select", team_dict[key].players['PF'].name, team_dict[key].players['PF'].show_overall_rating()
		for key in team_dict:
			team_dict[key].players['CR'] = cr_pool[len(cr_pool) - 1][1]
			cr_pool.pop()
			#print "The", team_dict[key].team_name, "select", team_dict[key].players['CR'].name, team_dict[key].players['CR'].show_overall_rating()
		rest_of_team = ['bench_1', 'bench_2', 'bench_3', 'bench_4', 'bench_5',
						'bench_6', 'bench_7', 'bench_8', 'bench_9' ]


		for item in rest_of_team:
			for key in team_dict:
				type_to_draft = random.randint(1,5)

				if type_to_draft == 1:
					if pg_pool != []:
						team_dict[key].players[item] = pg_pool[len(pg_pool) -1][1]
						pg_pool.pop()
						#print "The", team_dict[key].team_name, "select", team_dict[key].players[item].name, team_dict[key].players[item].show_overall_rating(), team_dict[key].players[item].position
					else:
						type_to_draft += 1
				elif type_to_draft == 2:
					if sg_pool != []:

						team_dict[key].players[item] = sg_pool[len(sg_pool) - 1][1]
						sg_pool.pop()
						#print "The", team_dict[key].team_name, "select", team_dict[key].players[item].name, team_dict[key].players[item].show_overall_rating(), team_dict[key].players[item].position						
					else:
						type_to_draft += 1
				elif type_to_draft == 3:
					if sf_pool != []:

						team_dict[key].players[item] = sf_pool[len(sf_pool) - 1][1]
						sf_pool.pop()
						#print "The", team_dict[key].team_name, "select", team_dict[key].players[item].name, team_dict[key].players[item].show_overall_rating(), team_dict[key].players[item].position
					else:
						type_to_draft += 1
				elif type_to_draft == 4:
					if pf_pool != []:

						team_dict[key].players[item] = pf_pool[len(pf_pool) - 1][1]
						pf_pool.pop()							
						#print "The", team_dict[key].team_name, "select", team_dict[key].players[item].name, team_dict[key].players[item].show_overall_rating(), team_dict[key].players[item].position
					else:
						type_to_draft += 1
				elif type_to_draft == 5:
					if cr_pool != []:
						team_dict[key].players[item] = cr_pool[len(cr_pool) - 1][1]
						cr_pool.pop()								
						#print "The", team_dict[key].team_name, "select", team_dict[key].players[item].name, team_dict[key].players[item].show_overall_rating(), team_dict[key].players[item].position
					else:
						type_to_draft += 1
				else:
					team_dict[key].players[item] = pg_pool[len(pg_pool) -1][1]
					pg_pool.pop()
					#print "The", team_dict[key].team_name, "select", team_dict[key].players[item].name, team_dict[key].players[item].show_overall_rating(), team_dict[key].players[item].position
					
	




	##############################
	# The following should only be run when creating a brand new league, 
	# otherwise these should be built from the database class object extractions
	##############################
	def create_league(self):
		try: 
			if self.team_dict: 
				pass
		except AttributeError:
			print "league teams do not exist, creating now"
			self.insert_league()
			self.coach_pool = self.get_coaches()
			self.pg_pool = self.get_pg_pool()

			self.sg_pool = self.get_sg_pool()

			self.sf_pool = self.get_sf_pool()

			self.pf_pool = self.get_pf_pool()

			self.cr_pool = self.get_cr_pool()

			self.team_dict = self.make_teams(self.coach_pool, self.team_name_pool)

			self.conferences = self.assign_to_conference(self.team_dict, self.number_of_teams)

			self.draft_players(self.pg_pool, self.sg_pool, self.sf_pool, self.pf_pool, self.cr_pool, self.team_dict)

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
		number_of_coaches = coaches[0][0]
		print number_of_coaches
		coach_pool = load_coaches(league_pk, number_of_coaches) # get a list with the coach objects in it



new_or_old = str(raw_input('start a new game or load one? \n type new or load: '))


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

# for item in self.team_dict:
# 	print item, "team schedule"
# 	for line in self.league_schedule:
# 		if item == line[0]:
# 			print "vs", line[1] 
# 		elif item == line[1]:
# 			print "@", line[0]
# 		else: 
# 			pass
# 	print "xxxxxxxxxxxxxxxx"
