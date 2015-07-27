from game_variables import budget
import random

class Team:
	def __init__(self, coach, team_name):
		self.coach = coach
		self.team_name = team_name
		self.budget = 100
		self.home_court_advantage = random.randrange(50,100)
		self.possessions = 100
		self.percentage_close = .25
		self.percentage_midrange = .25
		self.percentage_three = .25
		self.percentage_layup =  .25
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




