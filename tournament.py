#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

LOG_LEVEL = 0

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("DELETE FROM matches")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("DELETE FROM players")
    conn.commit()
    conn.close()

def deleteTornaments():
    """Remove all the tournament records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("DELETE FROM tournament")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("SELECT * FROM players")
    return cursor.rowcount
    conn.close()

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO players (name) values (%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("""
                        SELECT players.id, name, count(wins), count(wins) + count (losses)
                        FROM players
                        LEFT JOIN matches as wins
                            on wins.winner = players.id
                        LEFT JOIN matches as losses
                            on losses.loser = players.id
                        GROUP BY players.id, name
                        ORDER BY count(wins) desc, players.id 
                    """)
    return cursor.fetchall()
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("""
                        INSERT INTO matches (winner, loser)
                        VALUES (%s, %s)
                    """, (winner, loser,))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ##
    ## TODO:  A known bug exists when the first iteration leaves a pool of more than 1 players needing match,
    ##      and either none are eiligible for a bye, or all have played each other.
    ##
    standings = playerStandings() # list of tuples, each of which contains (id, name, wins, matches)
    length = len(standings)
    l_range = range (length)
    result = []
    blacklist = []
    potentialOpponents = list(standings)
    for playerTuple in standings:
        if playerTuple in blacklist:
            log ("ignore:  playerTuple in blacklist")
            pass
        else: # need to register player
            match = None
            for potentialOpponent in potentialOpponents:
                if playerTuple is potentialOpponent:
                    # player cannot play itself
                    log ("ignore:  playerTuple is blacklist")
                elif potentialOpponent in blacklist:
                    # player already registered by system.
                    log ( "ignore:  playerTuple in blacklist")
                elif havePlayersPlayed (str(playerTuple[0]), str(potentialOpponent[0])):
                    # player and potntialOpponent have already played..
                    log ( "ignore:  players have played", playerTuple[1] +","+ potentialOpponent[1])
                else:
                    # we found a match!
                    match = (playerTuple, potentialOpponent)
                    log ( "match found for players", match[0][1] +","+ match[1][1])
                    break
            if match:
                # Add opponents to result and blacklist, remove from potentialOpponents.
                result.append ((match[0][0], match[0][1], match[1][0], match[1][1]))
                blacklist.append (match[0])
                blacklist.append (match[1])
                if match[0] in potentialOpponents:
                    potentialOpponents.remove (match[0])
                if match[1] in potentialOpponents:
                    potentialOpponents.remove (match[1])
            else:
                log ( "No match found for "+playerTuple[1])
    if len(potentialOpponents) > 0:
        match = None
        log ( "Resolving bye-candidates: ", potentialOpponents)
        byeGiven = length % 2 == 0 # if even, then there is no bye to give.
        for byeCandidate in potentialOpponents:
            for nestedByeCandidate in potentialOpponents:
                if byeCandidate is nestedByeCandidate:
                    # player cannot play itself
                    log ("ignore:  nestedByeCandidate is byeCandidate")
                elif nestedByeCandidate in blacklist:
                    # player already registered by system.
                    log ( "ignore:  nestedByeCandidate in blacklist")
                elif havePlayersPlayed (str(nestedByeCandidate[0]), str(byeCandidate[0])):
                    # nestedByeCandidate and byeCandidate have already played..
                    log ( "ignore:  players have played", nestedByeCandidate[1] +","+ byeCandidate[1])
                else:
                    # we found a match!
                    match = (nestedByeCandidate, byeCandidate)
                    log ( "match found for players", match[0][1] +","+ match[1][1])
                    result.append ((match[0][0], match[0][1], match[1][0], match[1][1]))
                    blacklist.append (match[0])
                    blacklist.append (match[1])
                    break
        for byeCandidate in potentialOpponents:
            if not byeGiven and not byeCandidate in blacklist and hasPlayerHadBye(str(byeCandidate[0])):
                c = len(result)
                i = 0
                while i <= c - 1:
                    if not byeGiven and not havePlayersPlayed (str(byeCandidate[0]), str(result[i][2])) and not hasPlayerHadBye(str(result[i][0])):
                        log ( "Replacing "+ str(result[i][1]) +"(who gets get a bye) with"+str(byeCandidate[1]))
                        result.append ((result[i][0], result[i][1], None, None))
                        result[i] = (byeCandidate[0], byeCandidate[1], result[i][2], result[i][3])
                        byeGiven = True
                        break
                    elif not byeGiven and not havePlayersPlayed (str(byeCandidate[0]), str(result[i][0])) and not hasPlayerHadBye(str(result[i][2])):
                        log ( "Replacing "+ str(result[i][3]) +"(who gets get a bye) with"+str(byeCandidate[1]))
                        result.append ((result[i][2], result[i][3], None, None))
                        result[i] = (byeCandidate[0], byeCandidate[1], result[i][1], result[i][1])
                        byeGiven = True
                        break
                    i += 1
            elif not byeGiven and not byeCandidate in blacklist:
                result.append ((byeCandidate[0], byeCandidate[1], None, None))
                
    return result

def havePlayersPlayed(id1, id2):
    """ Returns a Boolean of whether player with id1 andid2 have played a match."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("""
                        SELECT *
                        FROM Matches
                        WHERE (winner = """+id1+""" and loser = """+id2+""") or (winner = """+id2+""" and loser = """+id1+""")
                    """)
    return cursor.rowcount > 0
    conn.close()

def hasPlayerHadBye(id1):
    """ Returns a Boolean of whether player with id1 has had a bye."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute ("""
                        SELECT *
                        FROM Matches
                        WHERE winner = """+id1+""" and loser is null
                    """)
    return cursor.rowcount > 0
    conn.close()


def log(*string):
    if LOG_LEVEL > 0:
        print("log info: {}".format(string))

    
