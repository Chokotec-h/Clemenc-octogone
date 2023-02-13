
import pickle
from graphics import *
import traceback


players = []
games = []

gamepop = 0

def threaded_client(conn, player):
    global gamepop
    global currentPlayer
    if len(players) < player+1 :
        players.append(player+1)
    if player%2 == 0:
        games.append([False,False])
        currentgame = len(games)-1
        gamestatuses.append(f"Game {player//2 + 1:2}        |        Status : Waiting for opponent")
    else :
        currentgame = len(games)-1
        gamestatuses[currentgame] = f"Game {player//2 + 1:2}        |        Status : Connected"
    window.gamestatusestk.set(gamestatuses)
    lengames = len(games)
    if "Player_removed" in games[currentgame]:
        games[currentgame] = [False,False]
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True :
        try :
            if len(games) > lengames :
                lengames = len(games)
            if len(games) < lengames :
                if gamepop == currentgame :
                    print("Game deleted")
                    print("Lost connection")
                    conn.close()
                    return
                if gamepop < currentgame :
                    currentgame -= 1
                    player -= 2
                    currentPlayer -= 2
            data = pickle.loads(conn.recv(8192*16))
            players[player] = data

            if data == "Waiting" :
                games[currentgame][player%2] = True
            if isinstance(data,list):
                if data[0] == "Chars": # ["Chars",ready,name]
                    games[currentgame][player%2] = data[1:]
                if data[0] == "Stage" and player%2 == 0: # ["Stage",stage]
                    games[currentgame] = [data[1],data[1]]
                if data[0] == "Countdown" and player%2 == 0: # ["Countown",countdown]
                    games[currentgame] = [data[1],data[1]]
                if data[0] == "Game": # ["Battle",char,time] si hôte ; ["Battle",char] sinon
                    games[currentgame][player%2] = data[1:]
            if not data :
                print("Disconnected")
                break
            else :
                reply = games[currentgame]
                print("Recieved : ", data)
                print("Sending : ",reply)
                conn.sendall(pickle.dumps(reply))
        except :
            traceback.print_exc()
            break
    try :
        games.pop(currentgame)
        gamestatuses.pop(currentgame)
        gamepop = currentgame
        window.gamestatusestk.set(gamestatuses)
    except:
        pass
        
    print("Lost connection")
    conn.close()

window = Window(threaded_client)
window.mainloop()
