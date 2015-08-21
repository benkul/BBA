import random
import sqlite3
from player_last_names import player_last_names
from player_first_names import player_first_names
from game_variables import age, potential, def_iq, off_iq, decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, all_star_quality, height, wingspan, vertical, speed, passing, dribbling, shot_layup, shot_midrange, shot_close, shot_three, shot_ft, steal, block, major_bonus, minor_bonus, rebounding
from game_variables import all_star_threshold, all_star_bonus, all_star_stat_min, all_star_stat_max, number_of_teams
from game_variables import team_name_options
from create_team import Team
from game_variables import budget

def create_stat(stat): # assumes a min/max tuple as input 
	min = stat[0]	   # helper function that aids in class object creation
	max = stat[1]
	selection = random.randrange(min, max)	
	return selection

def rating_to_letter_grade(rating): # helper function that converts number ratings to letter grades
	if rating >= 95:
		letter_grade = "A+"
	elif rating <= 94 and rating >= 90: 
		letter_grade = "A"
	elif rating <=	89 and rating >= 85:
		letter_grade = "A-"
	elif rating <= 84 and rating >= 80:
		letter_grade = "B+"
	elif rating <= 79 and rating >= 75:
		letter_grade = "B"
	elif rating <= 74 and rating >= 70:
		letter_grade = "B-"
	elif rating <= 69 and rating >= 65:
		letter_grade = "C+"
	elif rating <= 64 and rating >= 60:
		letter_grade = "C"
	elif rating <= 59 and rating >= 55:
		letter_grade = "C-"
	elif rating <= 54 and rating >= 50:
		letter_grade = "D+"
	elif rating <= 49 and rating >= 45:
		letter_grade = "D"
	elif rating <= 44 and rating >= 40:
		letter_grade = "D-"
	elif rating <=39:
		letter_grade = "F"
	return letter_grade

def cm_to_in(height):  # heights are stored in cm, this converst to feet/inches for ui output
	in_high = height / 2.54
	feet_high = int(in_high / 12)
	remainder = int(in_high % 12)
	feet_inches = str(feet_high) + "'" + str(remainder) + '"'
	return feet_inches

# Player database table structure for future reference
# database.execute('''CREATE TABLE player_db (Id integer primary key,
# 	league_id REFERENCES league_table(Id), 
# 	team_id REFERENCES team_db(Id), 
# 	salary, name, age, potential, def_iq, off_iq, decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, 
# 	height, wingspan, vertical, speed, passing, dribbling, shot_layup, shot_close, shot_midrange, shot_three, shot_ft, steal, rebounding, 
# 	block, birthday, position)''')

class Player:
	def __init__(self, league_id):
		self.league_id = league_id
		self.db_id = 0 # default value, gets updated when stored in database
		self.name = random.choice(player_first_names) + " " + random.choice(player_last_names)
		self.age = create_stat(age)
		self.potential = create_stat(potential)
		self.def_iq = create_stat(def_iq)
		self.off_iq = create_stat(off_iq)
		self.decision_making = create_stat(decision_making)
		self.court_awareness = create_stat(court_awareness)
		self.strength = create_stat(strength)
		self.fatigue = create_stat(fatigue)
		self.stamina = create_stat(stamina)
		self.shooting_touch = create_stat(shooting_touch)
		self.all_star_quality = create_stat(all_star_quality)
		self.height = create_stat(height)
		self.wingspan = self.height + create_stat(wingspan)
		self.vertical = create_stat(vertical)
		self.speed = create_stat(speed)
		self.passing = create_stat(passing)
		self.dribbling = create_stat(dribbling)
		self.shot_layup = create_stat(shot_layup)
		self.shot_close = create_stat(shot_close)
		self.shot_midrange = create_stat(shot_midrange)
		self.shot_three = create_stat(shot_three)
		self.shot_ft = create_stat(shot_ft)
		self.steal = create_stat(steal)
		self.rebounding = create_stat(rebounding)
		self.block = create_stat(block)
		self.birthday = random.randrange(0, (number_of_teams * 4))
		self.team = ''
		self.salary = 1 # placeholder for league minimum, need transformation in player subclasses that creates salary based on player ability
		self.position = '' 
		self.role = '' # players role on team starter, bench etc
		self.full_abilities = [
			'court_awareness', 
			'decision_making', 
			'passing', 
			'dribbling', 
			'steal', 
			'def_iq', 
			'off_iq', 
			'speed',
			'strength',
			'stamina',
			'shot_layup',
			'shot_close',
			'shot_midrange',
			'shot_three',
			'rebounding',
			'block'
			]


	def all_star_modifier(self):
		if self.all_star_quality >= all_star_threshold:
			essentials = self.player_get_essentials()
			for rating in essentials:
				setattr(self, rating, getattr(self, rating) + all_star_bonus)
				while getattr(self, rating) < all_star_stat_min:
					setattr(self, rating, getattr(self, rating) + all_star_bonus)
				if getattr(self, rating)  > all_star_stat_max:
					setattr(self, rating, all_star_stat_max)
		else: 
			pass

	def change_role(self, new_role):
		self.role = new_role
		return self.role


	def set_db_id(self):
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		player_attributed = (int(self.league_id), str(self.name))
		database.execute('''SELECT Id FROM player_db WHERE league_id = ? AND name = ?''', player_attributed)
		id_number = database.fetchone()
		self.db_id = id_number
		connection.commit()
		connection.close()

	def show_rating(self):
		total = 0
		for rating in self.full_abilities:
			total += getattr(self, rating)
		overall_rating = total / 16 # possibly replace with len(full_abilities)
		return overall_rating

	def show_letter_grade(self):
		return rating_to_letter_grade(self.show_rating())

	def player_game_growth(self):
		essentials = self.player_get_essentials()
		if self.age < 30:  # this works but feels cumbersome, might be worth having a parabolic function that returns bonus
			rating_bonus = 1
			for rating in essentials:
				if self.potential >= 85:
					if random.randrange(1,100) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				elif self.potential >= 70 and self.potential <= 84:
					if random.randrange(1,300) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				elif self.potential >= 55 and self.potential <= 69:
					if random.randrange(1,400) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				elif self.potential <= 54:
					if random.randrange(1,500) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				if getattr(self, rating) >= 99:
					setattr(self, rating, 99)	
		elif self.age >= 30:
			rating_bonus = -1
			for rating in essentials:
				if self.potential >= 85:
					if random.randrange(1,500) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				elif self.potential >= 70 and self.potential <= 84:
					if random.randrange(1,400) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				elif self.potential >= 55 and self.potential <= 69:
					if random.randrange(1,300) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				elif self.potential <= 54:
					if random.randrange(1,100) == 15:
						setattr(self, rating, getattr(self, rating) + rating_bonus)
				if getattr(self, rating) <= 10:
					setattr(self, rating, 10)

	def player_birthday_check(self, game_day):
		if self.birthday == game_day:
			self.age += 1
		return self.age

	def player_offseason_growth(self):
		young_range = (18)
		prime_range = (25)
		beyond_prime = (30)
		older = (33)
		oldest = (36)
		def growth_modifier():
			if self.potential >= 85:
				return 5
			elif self.potential >= 70 and self.potential <= 84:
				return 4
			elif self.potential >= 55 and self.potential <= 69:
				return 3
			elif self.potential <= 54:
				return 2
		off_season_growth = growth_modifier()
		if self.age in range(young_range,prime_range):
			off_season_growth += random.randrange(2,6)
		elif self.age in range(prime_range,beyond_prime):
			off_season_growth += random.randrange(1,3)
		elif self.age in range(beyond_prime,older):
			off_season_growth += random.randrange(-5,0)
		elif self.age in range(older, oldest):
			off_season_growth += random.randrange(-8,-3)
		elif self.age in range(older, oldest):
			off_season_growth += random.randrange(-8,-5)	
		for rating in self.full_abilities:
			setattr(self, rating, getattr(self, rating) + random.randrange(off_season_growth - 4, off_season_growth - 1))
			if getattr(self, rating) >= 99:
				setattr(self, rating, 99)
		return self.full_abilities # not sure if the return here is necessary


	def insert_player(self): # puts the player class object into the player database table
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		player_attributes = (self.league_id, self.team, self.name, self.age, self.potential, self.def_iq, self.off_iq, 
			self.decision_making, self.court_awareness, self.strength, self.fatigue, self.stamina, self.shooting_touch, 
			self.height, self.wingspan, self.vertical, self.speed, self.passing, 
			self.dribbling, self.shot_layup, self.shot_close, self.shot_midrange, self.shot_three, 
			self.shot_ft, self.steal, self.rebounding, self.block, self.birthday, self.salary, self.position, self.role)

		database.execute('''INSERT INTO player_db
		(league_id, team_id, name, age, potential, def_iq, off_iq, decision_making, court_awareness, 
			strength, fatigue, stamina, shooting_touch, height, wingspan, vertical, 
			speed, passing, dribbling, shot_layup, shot_close, shot_midrange, shot_three, shot_ft, steal, 
			rebounding, block, birthday, salary, position, role)
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', player_attributes)
		connection.commit()
		connection.close()

	def update_player(self):
		connection = sqlite3.connect('league.db')
		database = connection.cursor()
		player_attributes = (self.league_id, self.team, self.age, self.potential, self.def_iq, self.off_iq, 
			self.decision_making, self.court_awareness, self.strength, self.fatigue, self.stamina, self.shooting_touch, 
			self.height, self.wingspan, self.vertical, self.speed, self.passing, 
			self.dribbling, self.shot_layup, self.shot_close, self.shot_midrange, self.shot_three, 
			self.shot_ft, self.steal, self.rebounding, self.block, self.birthday, self.salary, self.position, self.role, self.name, self.league_id)
		database.execute('''UPDATE player_db 
			SET league_id=?, 
			team_id=?, 
			age=?, 
			potential=?, 
			def_iq=?, 
			off_iq=?, 
			decision_making=?, 
			court_awareness=?, 
			strength=?, 
			fatigue=?, 
			stamina=?, 
			shooting_touch=?, 
			height=?, 
			wingspan=?, 
			vertical=?, 
			speed=?, 
			passing=?, 
			dribbling=?, 
			shot_layup=?, 
			shot_close=?, 
			shot_midrange=?, 
			shot_three=?, 
			shot_ft=?, 
			steal=?,
			rebounding=?, 
			block=?, 
			birthday=?, 
			salary=?, 
			position=?
			role=?
			WHERE 'name' = ? AND 'league_id' = ? ''', player_attributes) # name isn't uniqe in db, but name is unique within league
		print "player", self.name,  "updated"
		connection.commit()
		connection.close()

		#########################
		#
		# Player database table structure for future reference
		#
		# database.execute('''CREATE TABLE player_db (Id integer primary key,
		# 	league_id REFERENCES league_table(Id), 
		# 	team_id REFERENCES team_db(Id), 
		# 	salary, name, age, potential, def_iq, off_iq, decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, 
		# 	height, wingspan, vertical, speed, passing, dribbling, shot_layup, shot_close, shot_midrange, shot_three, shot_ft, steal, rebounding, 
		# 	block, birthday, position, role)''')
		#
		#########################
	



	def player_get_essentials(self):
		if self.position == 'PG':
			return [
			'court_awareness', 
			'decision_making', 
			'passing', 
			'dribbling', 
			'steal', 
			'def_iq', 
			'off_iq', 
			'speed']
		elif self.position == 'SG':
			return [
			'off_iq', 
			'decision_making', 
			'steal', 
			'passing', 
			'speed', 
			'def_iq', 
			'dribbling', 
			'court_awareness'
			]
		elif self.position == 'SF':
			return [			
			'court_awareness', 
			'decision_making', 
			'speed', 
			'passing', 
			'rebounding', 
			'def_iq', 
			'off_iq', 
			'dribbling'
			]
		elif self.position == 'PF':
			return [
			'court_awareness', 
			'decision_making', 
			'rebounding', 
			'block', 
			'speed', 
			'def_iq', 
			'off_iq', 
			'passing'
			]
		elif self.position == 'C':
			return [
			'court_awareness', 
			'decision_making', 
			'rebounding', 
			'block', 
			'speed',  
			'def_iq', 
			'off_iq', 
			'passing'
			]

	def PG_modifier(self):
		self.court_awareness = major_bonus(self.court_awareness)
		self.decision_making = major_bonus(self.decision_making)
		self.passing = major_bonus(self.passing)
		self.dribbling = major_bonus(self.dribbling)
		self.steal = major_bonus(self.steal)
		self.off_iq = major_bonus(self.off_iq)
		self.speed = major_bonus(self.speed)
		self.height += random.randrange(1,5)
		self.shot_layup += self.shooting_touch
		self.shot_ft += self.shooting_touch
		self.shot_three += self.shooting_touch
		self.position = "PG"
	
	def SG_modifier(self):
		self.shot_layup = major_bonus(self.shot_layup)
		self.shot_midrange = major_bonus(self.shot_midrange)
		self.shot_three = major_bonus(self.shot_three)
		self.off_iq = major_bonus(self.off_iq)
		self.steal = major_bonus(self.steal)
		self.speed = major_bonus(self.speed)
		self.decision_making = major_bonus(self.decision_making)
		self.shooting_touch = minor_bonus(self.shooting_touch)
		self.height += random.randrange(4 , 10)
		self.shot_midrange += self.shooting_touch
		self.shot_ft += self.shooting_touch
		self.shot_three += self.shooting_touch			
		self.position = "SG"

	def SF_modifier(self):
		self.court_awareness = major_bonus(self.court_awareness)
		self.decision_making = major_bonus(self.decision_making)
		self.shot_three = minor_bonus(self.shot_three)
		self.rebounding = major_bonus(self.rebounding)
		self.shot_midrange = minor_bonus(self.shot_midrange)
		self.off_iq = major_bonus(self.off_iq)
		self.def_iq = major_bonus(self.def_iq)
		self.speed = minor_bonus(self.shot_three)
		self.shot_layup = minor_bonus(self.shot_layup)
		self.height += random.randrange(9 , 19)			
		self.shot_layup += self.shooting_touch
		self.shot_ft += self.shooting_touch
		self.shot_three += self.shooting_touch
		self.shot_midrange += self.shooting_touch			
		self.position = "SF"	
	
	def PF_modifier(self):
		self.def_iq = major_bonus(self.def_iq)
		self.decision_making = major_bonus(self.decision_making)
		self.rebounding= major_bonus(self.rebounding)
		self.shot_close = major_bonus(self.shot_close)
		self.block = major_bonus(self.block)
		self.off_iq = minor_bonus(self.off_iq)
		self.def_iq = major_bonus(self.def_iq)
		self.height += random.randrange(18 , 25)			
		self.shot_layup += self.shooting_touch
		self.shot_close += self.shooting_touch
		self.shot_midrange += self.shooting_touch			
		self.position = "PF"	

	def C_modifier(self):
		self.decision_making = major_bonus(self.decision_making)
		self.rebounding= major_bonus(self.rebounding)
		self.shot_close = major_bonus(self.shot_close)
		self.block = major_bonus(self.block)
		self.off_iq = major_bonus(self.off_iq)
		self.def_iq = major_bonus(self.off_iq)
		self.height += random.randrange(22 , 28)			
		self.shot_layup += self.shooting_touch
		self.shot_close += self.shooting_touch		
		self.position = "C"
	

	def player_set_position(self):
		# one time run on inital player setup

		position = random.randrange(1, 6)
		# set position
		if position == 1:
			self.PG_modifier()
		elif position == 2:
			self.SG_modifier()
		elif position == 3:
			self.SF_modifier()
		elif position == 4:
			self.PF_modifier()
		elif position == 5:
			self.C_modifier()
		# provide bonuses for all-stars	
		self.all_star_modifier
		

def load_players(league_id):
	print "starting player load"
	connection = sqlite3.connect('league.db')
	database = connection.cursor()
	database.execute('''SELECT league_id, team_id, name, age, potential, def_iq, off_iq, decision_making, court_awareness, 
			strength, fatigue, stamina, shooting_touch, height, wingspan, vertical, 
			speed, passing, dribbling, shot_layup, shot_close, shot_midrange, shot_three, shot_ft, steal,
			rebounding, block, birthday, salary, position, role FROM player_db WHERE league_id = ?''', league_id)	

	player_pool = []
	player = 0
	player_attribute = database.fetchone()
	while player_attribute != None:
		player_pool.append(Player(league_id))
		print "attempting player resurrection"
		player_pool[player].league_id = player_attribute[0]
		player_pool[player].team = player_attribute[1]
		player_pool[player].name = player_attribute[2]
		player_pool[player].age = player_attribute[3]
		player_pool[player].potential = player_attribute[4]
		player_pool[player].def_iq  = player_attribute[5]
		player_pool[player].off_iq = player_attribute[6]
		player_pool[player].decision_making = player_attribute[7]
		player_pool[player].court_awareness = player_attribute[8]
		player_pool[player].strength = player_attribute[9]
		player_pool[player].fatigue = player_attribute[10]
		player_pool[player].stamina = player_attribute[11]
		player_pool[player].shooting_touch = player_attribute[12]
		player_pool[player].height = player_attribute[13]
		player_pool[player].wingspan = player_attribute[14]
		player_pool[player].vertical = player_attribute[15]
		player_pool[player].speed = player_attribute[16]
		player_pool[player].passing = player_attribute[17]
		player_pool[player].dribbling = player_attribute[18]
		player_pool[player].shot_layup = player_attribute[19]
		player_pool[player].shot_close = player_attribute[20]
		player_pool[player].shot_midrange = player_attribute[21]
		player_pool[player].shot_three = player_attribute[22]
		player_pool[player].shot_ft = player_attribute[23]
		player_pool[player].steal = player_attribute[24]
		player_pool[player].rebounding = player_attribute[25]
		player_pool[player].block = player_attribute[26]
		player_pool[player].birthday = player_attribute[27]
		player_pool[player].salary = player_attribute[28]
		player_pool[player].position = player_attribute[29]
		player_pool[player].position = player_attribute[30]
		print player_pool[player].name, " resurrected"
		player += 1
		player_attribute = database.fetchone()
	connection.commit()		
	connection.close()	
	return player_pool



