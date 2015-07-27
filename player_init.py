import random
from player_last_names import player_last_names
from player_first_names import player_first_names
import sqlite3
from game_variables import age, potential, def_iq, off_iq, decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, all_star_quality, height, wingspan, vertical, speed, passing, dribbling, shot_layup, shot_midrange, shot_close, shot_three, shot_ft, steal, block, major_bonus, minor_bonus, rebounding
from game_variables import motivation, coach_off_iq, coach_def_iq, training, offense_playbook, defense_playbook, leadership
from game_variables import all_star_threshold, all_star_bonus, all_star_stat_min, all_star_stat_max, number_of_teams
from game_variables import team_name_options
from coach_first_names import coach_first_names
from create_team import Team
from game_variables import budget



class Coach:
	def __init__(self, coach_name):
		def create_stat(stat): # assumes a min/max tuple as input 
			min = stat[0]
			max = stat[1]
			selection = random.randrange(min, max)	
			return selection
		self.name = coach_name
		self.team = ''
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

		self.coach_rating = coach_rating()


		def add_to_coach_db(): # incomplete work, need code to create coach object and push to sqlite & return rowid for coach
			coach_object = []		# this would need to be called after teams are created, or updated with team unique id
			rowid = 1 				# since not all coaches will have a team, it makes sense to update the field after initializing the league
			return rowid

		self.id = add_to_coach_db()	






class Player:
	def __init__(self):
		def create_stat(stat): # assumes a min/max tuple as input 
			min = stat[0]
			max = stat[1]
			selection = random.randrange(min, max)	
			return selection

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
		self.essentials = []
		self.team = ''
		self.salary = 1 # placeholder for league minimum, need transformation in player subclasses that creates salary based on player ability
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
			for rating in self.essentials:
				setattr(self, rating, getattr(self, rating) + all_star_bonus)
				while getattr(self, rating) < all_star_stat_min:
					setattr(self, rating, getattr(self, rating) + all_star_bonus)
				if getattr(self, rating)  > all_star_stat_max:
					setattr(self, rating, all_star_stat_max)
		else: 
			pass

	def essential_rating(self, essentials):
		total = 0
		for rating in essentials:
			total += getattr(self, rating)
		output_rating = total / 8
		return output_rating


	def get_rating(self, rating):
		output_rating = int(rating)
		return output_rating


	def overall_rating(self, full_abilities):
		total = 0
		for rating in full_abilities:
			total += getattr(self, rating)
		overall_rating = total / 16 # possibly replace with len(full_abilities)
		return overall_rating

	def show_essential_rating(self):
		return rating_to_letter_grade(self.essential_rating(self.essentials))

	def show_overall_rating(self):
		return rating_to_letter_grade(self.overall_rating(self.full_abilities))

	def player_game_growth(self, essentials):
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



class Point_guard(Player):
	def __init__(self):		
		Player.__init__(self)
		def PG_modifier():
			self.court_awareness = major_bonus(self.court_awareness)
			self.decision_making = major_bonus(self.decision_making)
			self.passing = major_bonus(self.passing)
			self.dribbling = major_bonus(self.dribbling)
			self.steal = major_bonus(self.steal)
			self.off_iq = major_bonus(self.off_iq)
			self.speed = major_bonus(self.speed)
			self.height += random.randrange(1,5)
			self.position = "point guard"
			self.shot_layup += self.shooting_touch
			self.shot_ft += self.shooting_touch
			self.shot_three += self.shooting_touch
		self.essentials = [
			'court_awareness', 
			'decision_making', 
			'passing', 
			'dribbling', 
			'steal', 
			'def_iq', 
			'off_iq', 
			'speed']
		self.rating = self.overall_rating(self.full_abilities)

		PG_modifier()
		self.all_star_modifier()

class Shooting_guard(Player):
	def __init__(self):		
		Player.__init__(self)
		def SG_modifier():
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
			self.position = "shooting guard"
		self.essentials = [
			'off_iq', 
			'decision_making', 
			'steal', 
			'passing', 
			'speed', 
			'def_iq', 
			'dribbling', 
			'court_awareness'
			]
		SG_modifier()
		self.rating = self.overall_rating(self.full_abilities)		

class Small_forward(Player):
	def __init__(self):		
		Player.__init__(self)
		def SF_modifier():
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
			self.position = "small forward"
		self.essentials = [
			'court_awareness', 
			'decision_making', 
			'speed', 
			'passing', 
			'rebounding', 
			'def_iq', 
			'off_iq', 
			'dribbling'
			]
		SF_modifier()
		self.rating = self.overall_rating(self.full_abilities)		

		

class Power_forward(Player):
	def __init__(self):		
		Player.__init__(self)
		def PF_modifier():
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
			self.position = "power forward"
		self.essentials = [
			'court_awareness', 
			'decision_making', 
			'rebounding', 
			'block', 
			'speed', 
			'def_iq', 
			'off_iq', 
			'passing'
			]
		PF_modifier()
		self.rating = self.overall_rating(self.full_abilities)		
		

class Center(Player):
	def __init__(self):		
		Player.__init__(self)
		def C_modifier():
			self.decision_making = major_bonus(self.decision_making)
			self.rebounding= major_bonus(self.rebounding)
			self.shot_close = major_bonus(self.shot_close)
			self.block = major_bonus(self.block)
			self.off_iq = major_bonus(self.off_iq)
			self.def_iq = major_bonus(self.off_iq)
			self.height += random.randrange(22 , 28)			
			self.shot_layup += self.shooting_touch
			self.shot_close += self.shooting_touch		
			self.position = "power forward"
		self.essentials = [
			'court_awareness', 
			'decision_making', 
			'rebounding', 
			'block', 
			'speed',  
			'def_iq', 
			'off_iq', 
			'passing'
			]
		C_modifier()
		self.rating = self.overall_rating(self.full_abilities)		

		




def rating_to_letter_grade(rating):
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

def cm_to_in(height):
	in_high = height / 2.54
	feet_high = int(in_high / 12)
	remainder = int(in_high % 12)
	feet_inches = str(feet_high) + "'" + str(remainder) + '"'
	return feet_inches




