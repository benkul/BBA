import random
from player_last_names import player_last_names
from player_first_names import player_first_names
import sqlite3
from game_variables import age, potential, def_iq, off_iq, decision_making, court_awareness, strength, fatigue, stamina, shooting_touch, all_star_quality, height, wingspan, vertical, speed, passing, dribbling, shot_layup, shot_midrange, shot_close, shot_three, shot_ft, steal, block, major_bonus, minor_bonus, rebounding
from game_variables import motivation, coach_off_iq, coach_def_iq, training, offense_playbook, defense_playbook, leadership
from game_variables import all_star_threshold, all_star_bonus, all_star_stat_min, all_star_stat_max, team_name_options
from coach_first_names import coach_first_names
from create_team import  Team
from game_variables import budget
from coach_first_names import coach_first_names
from create_team import Team
from player_init import rating_to_letter_grade
from game_variables import budget, team_name_options
from league_init import League


##
# This whole thing needs to be re-worked around current season schedule methodology 
# Probably wait to refactor till after you've worked out the database calls. 
##
from player_init import Coach, Player, Point_guard, Shooting_guard, Small_forward, Power_forward, Center, rating_to_letter_grade, cm_to_in

season_length = 60

# create test objects

test_player = Player()
test_pg = Point_guard()
test_sg = Shooting_guard()
test_sf = Small_forward()
test_pf = Power_forward()
test_ce = Center()

test_case = (test_pg, test_sg, test_sf, test_pf, test_ce)

test_league = League()

game_day = 1

# confirm player builds
def assert_types(player):
	assert type(player.name) is str
	assert type(player.age) is int
	assert type(player.potential) is int
	assert type(player.def_iq) is int
	assert type(player.off_iq) is int
	assert type(player.decision_making) is int
	assert type(player.court_awareness) is int
	assert type(player.strength) is int
	assert type(player.fatigue) is int
	assert type(player.stamina) is int
	assert type(player.shooting_touch) is int
	assert type(player.all_star_quality) is int
	assert type(player.height) is int
	assert type(player.wingspan) is int
	assert type(player.vertical) is int
	assert type(player.speed) is int
	assert type(player.passing) is int
	assert type(player.dribbling) is int
	assert type(player.shot_layup) is int
	assert type(player.shot_close) is int
	assert type(player.shot_midrange) is int
	assert type(player.shot_three) is int
	assert type(player.shot_ft) is int
	assert type(player.steal) is int
	assert type(player.rebounding) is int
	assert type(player.block) is int
	assert type(player.essentials) is list

def assert_position_creation():
	print "================================================"
	for player in test_case:
		assert_types(player)
		print "test player", player.position, "creation passed"
	print "================================================"


assert_position_creation()
# confirm player sub-class modifiers modify appropriately
def test_player_height_modifier():
	for player in range(700):
		player = Center()
		assert player.height >= 202
		player = Power_forward()
		assert player.height >= 198
		player = Point_guard()
		assert player.height >= 180
		player = Shooting_guard()
		assert player.height >= 184
		player = Small_forward()
		assert player.height >= 189
	print "========================="
	print "player height test passed"
	print "========================="

test_player_height_modifier()

def test_birthday_checking(player, game_day):
	if player.birthday == game_day:
		#print "---------------------"
		#print "player birthday:", player.birthday, player.age
		#print "game_day:", game_day
		#print "---------------------"
		player.player_birthday_check(game_day)
		#print "---------------------"
		#print "player birthday:", player.birthday, player.age
		#print "game_day:", game_day
		#print "---------------------"


for day in range(season_length):
	global game_day
	test_birthday_checking(test_sg, game_day)
	game_day += 1


# confirm player functions return exepcted behaviour
def test_player_game_growth(player):
	#print"======================"
	#print"player potential", rating_to_letter_grade(player.potential), player.potential
	#print"player age", player.age
	#print"begin season essentials"
	#print player.essentials 
	for game in range(season_length):
		print "game ++++++++++++++++"
		for rating in player.essentials:
			player.player_game_growth(player.essentials)
			print getattr(player, rating)
	#print "end season essentials"
	print"======================"	
	#print player.essentials

test_player_game_growth(test_pg)

def check_all_star_percentage():
	temp = 0
	for player in range(400):
		player = Shooting_guard()
		if player.all_star_quality >= all_star_threshold:
			temp += 1
	print"============================"
	print temp, "all stars of 400 created"
	print"============================"

check_all_star_percentage()

def test_player_season_growth(player):
	#print"======================"
	#print"player potential", rating_to_letter_grade(player.potential), player.potential
	#print"player age", player.age
	#print"begin season"
	#for item in player.full_abilities:
	#print player.full_abilities
	player.player_offseason_growth()
	#print "end season"
	#for item in player.full_abilities:
	#print player.full_abilities
	#print"======================"	

test_player_season_growth(test_ce)

def test_career_arc():
	test_sg.age = 18
	temp = 1
	global game_day
	game_day = 1
	while test_sg.age < 40:
		test_player_game_growth(test_sg)
		print "------season ", temp, "--------"
		print "player age", test_sg.age, "player potential", test_sg.potential, "player overall", test_sg.show_overall_rating(), "sg essentials", test_sg.show_essential_rating()
		print test_sg.essentials
		for day in range(season_length):
			test_birthday_checking(test_sg, game_day)
			game_day += 1
		print "------end season", temp, "------"
		test_player_season_growth(test_sg)
		print test_sg.full_abilities
		game_day = 1
		temp += 1

#test_career_arc()


def confirm_teams_have_players(position):
	for key in test_league.team_dict:
		print test_league.team_dict[key].players[position].name

confirm_teams_have_players('PG')
