import math
import random

def get_h_cost(board):
    h = 0
    for i in range(len(board)):
        for j in range(i+1,len(board)):
            if(board[i][0] == board[j][0]):
                h += 1#Columna
            elif(board[i][1]==board[j][1]):
                h += 1#Renglo
            elif(abs(board[i][0]-board[j][0]) == abs(board[i][1]-board[j][1])):#Diagonales
                h += 1
    return h

def moveQueen(queenPos,board):
    board_copy = list(board)
    found_move = False
    movX=board_copy[queenPos][0]
    movY=board_copy[queenPos][1]
    
    while not found_move:
        movement = random.randint(0,2)

        if(movement==0): movement = -1
        elif(movement==1): movement = 1
        else: movement = 0

        #print("moveX; ", movement)

        if(movX > 1 and movX < len(board)):
            movX += movement
        elif(movX == 1):
            movX += abs(movement)
        else:
            movX -= abs(movement)

        if(movement!=0): movement = random.randint(0,2)
        else: movement = random.randint(0,1);

        if(movement==0): movement = -1
        elif (movement==1): movement = 1
        else: movement = 0

        #print("moveY; ",movement)

        if(movY>1 and movY < len(board)):
            movY += movement
        elif(movY==1):
            movY += abs(movement)
        else:
            movY -= abs(movement)

        board_copy[queenPos] = (movX,movY)
        if board[queenPos] == board_copy[queenPos]: continue
        for i in range(len(board)):
            if(queenPos == i): continue
            if(board_copy[queenPos] == board_copy[i]):
                found_move = False
                break
            else:
                found_move = True
    
    return board_copy

def moveQueen1(queenPos,board):
    found_move = False
    board_copy = list(board)
    movX = board_copy[queenPos][0]
    movY = board_copy[queenPos][1]
    
    while not found_move:
        
        movement = random.randint(0,2)

        if(movement==0): movement = -1
        elif(movement==1): movement = 1
        else: movement = 0

        if(movX > 1 and movX < len(board)):
            movX += movement
        elif(movX == 1):
            movX += abs(movement)
        else :
            movX -= abs(movement)

        if(movement!=0): movement = random.randint(0,2)
        else: movement = random.randint(0,1);

        if(movement==0): movement = -1
        elif (movement==1): movement = 1
        else: movement = 0

        if(movY>1 and movY < len(board)):
            movY += movement
        elif(movY==1):
            movY += abs(movement)
        else:
            movY -= abs(movement)

        
        if (board[queenPos] == (movX,movY)): continue
        for i in range(len(board)):
            if((movX,movY) == board_copy[i]):
                return (False, board)
            else:
                board_copy[queenPos] =(movX,movY)
                return (True,board_copy)

'''
Dada una posicion busca un movimiento,
Revisa toda la vecindad inmediata
No acepta lugares repeditos.
'''
def best_move(queenPos,board):
    found_move = False
    found_better = False
    result = list(board)
    h_to_beat = get_h_cost(board)
    movement = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,1),(1,-1)]
    
    for i in range(len(movement)):
        board_copy = list(board)
        
        movX = board_copy[queenPos][0] + movement[i][0]
        movY = board_copy[queenPos][1] + movement[i][1]

        if(movX < 1 or movY > len(board)): continue
        elif(movY < 1 or movY > len(board)): continue

        found_move = True
        
        for j in range(len(board)):
            if((movX,movY) == board_copy[j]):
                found_move = False
                break
            
        if(found_move):
            board_copy[queenPos] =(movX,movY)
            new_h_cost = get_h_cost(board_copy)
            if(new_h_cost < h_to_beat):
                h_to_beat = new_h_cost
                result = list(board_copy)
                found_better = True
            
    return (found_better,result)
    

def make_gready(board):
    h_to_beat = get_h_cost(board)
    while True:
        board_copy = list(board)
        posQueen = random.randint(0,len(board)-1)
        result = tuple(moveQueen1(posQueen,board_copy))
        #print("res ",result)
        if(result[0]):
            new_h_cost = get_h_cost(result[1])
            if (new_h_cost < h_to_beat):
                #print ("Nuevo costo ",new_h_cost, "viejo ", h_to_beat)
                return result[1]
            
def annealing(board):
  temp = len(board)**2
  anneal_rate = 0.95
  steps = 0
  new_h_cost = get_h_cost(board)
   
  while new_h_cost > 0:
    board = make_annealing_move(board,new_h_cost,temp)
    new_h_cost = get_h_cost(board)
    #La temperatura no debe ser 0
    new_temp = max(temp * anneal_rate,0.01)
    temp = new_temp
    steps += 1
    print(steps)
    if steps >= 50000:
      break
    
  print("\n h_cost: ", new_h_cost, " steps", steps)  
  return board
 
def make_annealing_move(board,h_to_beat,temp):
  board_copy = list(board)
  found_move = False
 
  while not found_move:
    '''
    board_copy = list(board)
    new_row = random.randint(0,len(board)-1)
    new_col = random.randint(0,len(board)-1)
    board_copy[new_col] = new_row
    '''
    board_copy = list(board)
    posQueen = random.randint(0,len(board)-1)
    board_copy = moveQueen(posQueen,board_copy)
    new_h_cost = get_h_cost(board_copy)
    #Si hay mejor movimiento
    if new_h_cost < h_to_beat:
      found_move = True
    #No hay mejor movimiento
    else:
      #Diferencia del Error
      delta_e = h_to_beat - new_h_cost
      #No mayor a 1
      accept_probability = min(1,math.exp(delta_e/temp))
      found_move = random.random() <= accept_probability
   
  return board_copy

def make_annealing_accep(board,h_to_beat,temp):
    board_copy = list(board)
    found_move = False
 
    board_copy = list(board)
    posQueen = random.randint(0,len(board)-1)
    board_copy = moveQueen(posQueen,board_copy)
    new_h_cost = get_h_cost(board_copy)
    #Si hay mejor movimiento
    if new_h_cost < h_to_beat:
      found_move = True
    #No hay mejor movimiento
    else:
      #Diferencia del Error
      delta_e = h_to_beat - new_h_cost
      #No mayor a 1
      accept_probability = min(1,math.exp(delta_e/temp))
      found_move = random.random() <= accept_probability
   
    return found_move

tablero = [(1,1),(1,2),(2,2),(2,1),(5,5),(6,6),(7,7),(8,8)]

tablero = annealing(tablero)

print(tablero)

'''
print(tablero)
print(get_h_cost(tablero))
result = best_move(0,tablero)
print(result)
print(get_h_cost(result[1]))
'''

def get_t0(n):
    t0=0
    percen=0
    while(percen < .8 or percent < 1):
        board = []
        for(i = 0; i < n; i+=1):
            board[i] = (random.randint(1,n),random.randint(1,n))

        accep = make_annealing_accep(board)
        if(accep):




