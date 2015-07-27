

def create_schedule(list):
    """ Create a schedule for the teams in the list and return it"""
    s = []

    if len(list) % 2 == 1: list = list + ["BYE"]

    for i in range(len(list)-1):

        mid = len(list) / 2
        l1 = list[:mid]
        l2 = list[mid:]
        l2.reverse()    

        # Switch sides after each round
        if(i % 2 == 1):
            s = s + [ zip(l1, l2) ]
        else:
            s = s + [ zip(l2, l1) ]

        list.insert(1, list.pop())

    return s


def return_schedule(div1, div2):
    games = []

    print "schedule div 1"
    for round in create_schedule(div1):
        for match in round:
            print match[0] + " - " + match[1]
            games.append(["%s" % match[0],  "%s"  % match[1]])
            games.append(["%s" % match[1],  "%s"  % match[0]])  
        print

    print
    print "schedule div 2"
    for round in create_schedule(div2):
        for match in round:
            print match[0] + " - " + match[1]
            games.append(["%s" % match[0],  "%s"  % match[1]]) 
            games.append(["%s" % match[1],  "%s"  % match[0]])        
        print

    print
    print "combined schedule"
    for round in create_schedule(div1+div2): # each team home
        for match in round:
            print match[0] + " - " + match[1]
            games.append(["%s" % match[0],  "%s"  % match[1]]) 
        print
    for round in create_schedule(div1+div2): # each team away 
        for match in round:
            print match[1] + " - " + match[0]
            games.append(["%s" % match[1],  "%s"  % match[0]]) 
        print
    return games
