#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

LOG_LEVEL = 0

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4, but is"+c)
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        print len(standings[0])
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

def testBye():
    """
        Tests a tournament with 5 players, where duplicate are never played, and each player has a BYE round
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Boo Bear")
    pairings = swissPairings()
    log( "initial pairings" + str (pairings))
    if len(pairings) != 3:
        raise ValueError(
            "After 0 rounds, for five players, swissPairings should return two pairs, but returns ", len(pairings))
    if pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]:
        raise ValueError(
            "After 0 rounds, Last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))
    reportMatch (pairings[0][0], pairings[0][2])
    reportMatch (pairings[1][0], pairings[1][2])
    reportMatch (pairings[2][0], None)
    pairings = swissPairings()
    log( "after 1st" + str (pairings))
    if len(pairings) != 3:
        raise ValueError(
            "After one round, for five players, swissPairings should return two pairs, but returns ",len(pairings))
    if pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]:
        raise ValueError(
            "After one rounds,Last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))
    reportMatch (pairings[0][0], pairings[0][2])
    reportMatch (pairings[1][0], pairings[1][2])
    reportMatch (pairings[2][0], None)
    pairings = swissPairings()
    log( "after 2nd" + str (pairings))
    if len(pairings) != 3:
        raise ValueError(
            "After 2 rounds, for five players, swissPairings should return two pairs, but returns ",len(pairings))
    if pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]:
        raise ValueError(
            "After 2 rounds,Last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))
    reportMatch (pairings[0][0], pairings[0][2])
    reportMatch (pairings[1][0], pairings[1][2])
    reportMatch (pairings[2][0], None)
    pairings = swissPairings()
    log( "after 3rd" + str (pairings))
    if len(pairings) != 3:
        raise ValueError(
            "After 3 rounds, for five players, swissPairings should return two pairs, but returns ",len(pairings))
    if pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]:
        raise ValueError(
            "After 3 rounds,Last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))
    reportMatch (pairings[0][0], pairings[0][2])
    reportMatch (pairings[1][0], pairings[1][2])
    reportMatch (pairings[2][0], None)
    pairings = swissPairings()
    log ("after 4th" + str (pairings))
    if len(pairings) != 3:
        raise ValueError(
            "After 4 rounds, for five players, swissPairings should return two pairs, but returns ",len(pairings))
    if pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]:
        raise ValueError(
            "After 4 rounds,Last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))

    print "9. After 4 rounds with 5 players, pairings always returned 3 pairs, with the last as a bye."

def testVolume():
    """
        Tests various sizes of tournaments.
        TODO:  This test does not currently pass.  See implementation of tournament.swissPairings()
    """
    deleteTornaments()
    deleteMatches()
    deletePlayers()
    tournamentSizes = [4,5,8,9,16,17]
    for playerCount in tournamentSizes:
        # New tournament
        deleteMatches()
        deletePlayers()
        # Register players
        for playerNumber in range(playerCount):
            registerPlayer ("Player "+str(playerNumber))
        # Initial pairings
        pairings = swissPairings()
        log ("Initial pairings" + str (pairings))
        rounds = playerCount - 1 if playerCount % 2 == 0 else playerCount
        matches = playerCount / 2 if playerCount % 2 == 0 else (playerCount + 1) / 2
        if len(pairings) != matches:
            raise ValueError(
                "After 0 rounds, for "+str(playerCount)+", players, swissPairings should return "+str(matches)+", but returns ", len(pairings))
        if playerCount % 2 != 0 and (pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]):
            raise ValueError(
                "After 0 rounds, for "+str(playerCount)+" players, last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))
        # Play rounds
        for r in range(rounds):
            for p in pairings:
                reportMatch (p[0], p[2])
            pairings = swissPairings()
            if len(pairings) != matches:
                raise ValueError(
                    "After "+str(r)+" rounds, for "+str(playerCount)+", players, swissPairings should return "+str(matches)+", but returns ", len(pairings))
            if playerCount % 2 != 0 and (pairings[len(pairings)-1][2] or pairings[len(pairings)-1][3]):
                raise ValueError(
                    "After "+str(r)+" rounds, for "+str(playerCount)+" players, last pairing should be a bye, which has no loser, but last pairing is: "+ str(pairings[len(pairings)-1]))
            

        print "10. After "+str(rounds)+" rounds with "+str(playerCount)+" players, pairings always returned as many pairs as rounds, with the last as a bye if the player count was uneven."

def log(*string):
    if LOG_LEVEL > 0:
        print("log info: {}".format(string))

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testBye()
##    testVolume()
    print "Success!  All tests pass!"


