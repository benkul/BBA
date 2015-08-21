# Player Variables

def major_bonus(stat):
	stat += 10
	return stat

def minor_bonus(stat):
	stat += 5
	return stat


#player variables
age 				= (18, 38)
potential 			= (30, 100)
def_iq 				= (35, 100)
off_iq 				= (35, 100)
decision_making 	= (39, 100)
court_awareness 	= (39, 100)
strength 			= (39, 100)
fatigue 			= (40, 100)
stamina 			= (40, 100)
shooting_touch 		= (5, 15)
all_star_quality 	= (0, 100)
height 				= (180, 190)
wingspan 			= (0, 13)
vertical 			= (20, 50)
speed 				= (40, 100)
passing 			= (50, 100)
dribbling 			= (50, 100)
shot_layup 			= (35, 65)
shot_close 			= (35, 50)
shot_midrange 		= (30, 50)
shot_three 			= (30, 49)
shot_ft 			= (55, 98)
steal 				= (40, 100)
block 				= (39, 60)
rebounding 			= (40, 100)
all_star_threshold 	= 90
all_star_bonus 		= 13
all_star_stat_min	= 64
all_star_stat_max 	= 96

#coach variables
motivation 			= (40, 100)
coach_off_iq		= (40, 100)
coach_def_iq		= (40, 100)
training			= (40, 100)
leadership			= (40, 100)
offense_playbook 	= {'1' : 'motion', '2' : 'flex', '3' : 'triangle'}
defense_playbook 	= {'1' : 'man', '2' : 'zone', '3' : 'trap'}

#team variables
budget 				= 100 # figured in millions of $
home_court_advantage= (50,100)
team_name_options = [
	"Chicago Cows",
	"Indianapolis Impalas",
	"Miami Manatees",
	"Tampa Bay Turtles",
	"Denver Donkeys",
	"Phoenix Pumas",
	"Portland Pythons",
	"New Orleans Osprey",
	"Houston Hawks",
	"Boston Bears",
	"Los Angeles Leopards",
	"Brooklyn Bulldogs ",
	"Minneapolis Moose",
	"Montreal Mice",
	"Memphis Mallards",
	"Toronto Terns",
	"Sacramento Stallions",
	"Dallas Ducks",
	"Philadelphia Pigeons",
	"Cleveland Cougars",
	"Seattle Seals",
	"Detroit Doves",
	"Atlanta Ants",
	"Hartford Hares",
	"St. Louis Swans",
	"Wichita Warthogs",
	"Louisville Lions",
	"Jersey City Jackals",
	"Oakland Owls",
	"Orlando Otters",
	"Washington Woodpeckers",
	"Baltimore Badgers",
	"Boise Beavers",
	"Charleston Catfish",
	"Cincinatti Crows",
	"Buffalo Bison"
]

# league variables
number_of_teams 		= 12
salary_cap 				= 100
number_of_players		= (number_of_teams * 30)
