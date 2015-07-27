import random


home_team_wins = 0
away_team_wins = 0

def simulate_game(home_team, away_team):
	home_team_score = 0
	away_team_score = 0
	print home_team
	print away_team
	global home_team_wins
	global away_team_wins

	def points_close(team):
		close_chances = team.possessions * team.percentage_close
		close_percentage = team.close_percentage() # need to handle this by player distribution
		return int((close_chances * close_percentage)/100 * 2)
	
	def points_midrange(team):
		midrange_chances = team.possessions * team.percentage_midrange
		midrange_percentage = team.midrange_percentage()  # need to handle this by player distribution
		return int((midrange_chances * midrange_percentage)/100 * 2)
	
	def points_three(team):
		three_chances = team.possessions * team.percentage_three
		three_percentage = team.three_percentage()  # need to handle this by player distribution
		return int((three_chances * three_percentage)/100 * 3)
	
	def points_layup(team):
		layup_percentage = team.possessions * team.percentage_layup
		layup_percentage = team.layup_percentage() # need to handle this by player distribution
		return int((three_chances * layup_percentage)/100 * 2)

	def points_ft(team):
		team_ft_chances = random.randrange(15,30)
		ft_percentage = team.ft_percentage() # hackish, this whole bit
		return int((team_ft_chances * ft_percentage)/100)

	home_team_score += points_close(home_team)
	print home_team_score
	home_team_score += points_midrange(home_team)
	home_team_score += points_three(home_team)
	home_team_score += points_ft(home_team)

	away_team_score += points_close(away_team)	
	away_team_score += points_midrange(away_team)
	away_team_score += points_three(away_team)
	away_team_score += points_ft(away_team)
	
	if home_team_score > away_team_score:
		print "the home team wins!"
		home_team_wins += 1
	elif away_team_score > home_team_score:
		print "the away team wins!"
		away_team_wins += 1
	else:
		home_team_score += 1
		print "the home team wins!"
		home_team_wins += 1


	print "+++++++++++++++++++++++++++++++++++"
	print "away team: ", away_team_score
	print "home team: ", home_team_score
	print "+++++++++++++++++++++++++++++++++++"
	print home_team_wins, "home team wins"
	print away_team_wins, "away_team_wins"





