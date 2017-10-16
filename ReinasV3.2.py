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
'''
Dada una posicion encuentra un movimiento,
no acepta lugares repeditos.
Avanza mas de un lugar.
'''
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

        for i in range(len(board)):
            if(queenPos == i): continue
            if((movX,movY) == board_copy[i]):
                found_move = False
                break
            else:
                found_move = True
    board_copy[queenPos] = (movX,movY)
    return board_copy
'''
Dada una posicion busca un movimiento,
Si dicho movimiento no es aceptable se
le avisa al usuario
No acepta lugares repeditos.
'''
def moveQueen1(queenPos,board):
    board_copy = list(board)
    movX = board_copy[queenPos][0]
    movY = board_copy[queenPos][1]
    
    while True:
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

        for i in range(len(board)):
            if(queenPos == i): continue
            if(movX,movY) == board_copy[i]:
                return (False, board)
            
        board_copy[queenPos] = (movX,movY)
        return (True,board_copy)

            
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

def make_annealing_accep(board,temp):
    found_move = False
    h_to_beat = get_h_cost(board)
 
    posQueen = random.randint(0,len(board)-1)
    result = moveQueen1(posQueen,board)
    if(result[0]):
        new_h_cost = get_h_cost(result[1])
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

def make_board(numQueen):
    n=1
    board=[]
    accepted = True
    posX=random.randint(1,numQueen)
    posY=random.randint(1,numQueen)
    newQueen = (posX,posY)
    board.append((newQueen))
    while n<numQueen:
        posX=random.randint(1,numQueen)
        posY=random.randint(1,numQueen)
        newQueen = (posX,posY)
        for i in range(len(board)):
            if(newQueen == board[i]):
                accepted = False
                break
        
        if(accepted):
            board.append(newQueen)
            n += 1
        accepted = True
    return board            

def get_t0(numQueens,t0,n):
  while(True):
    percen=0
    numAccep = 0
    for i in range(n):
      board = make_board(numQueens)

      accep = make_annealing_accep(board,t0)
      if(accep):
        numAccep += 1
        
    percen = numAccep/n
    print("Percent: ", percen)
    if(percen < .83):
      t0 += t0 * .05
    elif(percen > .87):
      t0 -= t0 * .5
    else:
      return t0

def annealing_iter_always(board,temp,n):
  alpha = 0.95
  beta = 1.05
  new_h_cost = get_h_cost(board)
  steps = 0
  iteration=0
   
  while new_h_cost > 0:
    board = make_annealing_move(board,new_h_cost,temp)
    new_h_cost = get_h_cost(board)
    steps += 1
    if steps >= n:
      temp = max(temp * alpha,0.01)
      n = int(n * beta)
      steps = 0
      iteration+=1
      if(iteration >= 1000): break
    
  print("\n h_cost: ", new_h_cost, "steps", steps)  
  return board

def annealing_iter_sometimes(board,temp,n):
  alpha = 0.95
  beta = 1.05
  new_h_cost = get_h_cost(board)
  steps = 0
  iteration=0
   
  while new_h_cost > 0:
    result = tuple(make_annealing(board,temp))
    if(result[0]):
      board = result[1]
      new_h_cost = get_h_cost(board)
    steps += 1
    if steps >= n:
      temp = max(temp * alpha,0.01)
      n = int(n * beta)
      steps = 0
      iteration+=1
      if(iteration >= 1000): break
    
  print("\n h_cost: ", new_h_cost, "steps", steps)  
  return board
def make_annealing(board,temp):
    found_move = False
    h_to_beat = get_h_cost(board)
    posQueen = random.randint(0,len(board)-1)
    result = tuple(moveQueen1(posQueen,board))
    if(result[0]):
      new_h_cost = get_h_cost(result[1])
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
   
    if(found_move):
        return(True, result[1])
    else:
        return(False, board)
def get_n0(board,temp,n):
  steps = 0
  lastChange=0
  result = ()
   
  while steps<1000:
    result = tuple(make_annealing(board,temp))
    
    lastChange += 1  
    steps += 1

    if(result[0]):
      board=result[1]
      lastChange=0
      
    if lastChange >= n:
      break

  return steps-lastChange

def get_worst_trap(board,temp,n):
  steps = 0
  lastChange=0
  worst = 0
  result = ()
   
  while steps<n:
    result = tuple(make_annealing(board,temp))
    
    lastChange += 1  
    steps += 1

    if(result[0]):
      board=result[1]
      if lastChange > worst:
        worst = lastChange
      lastChange=0
    

  return worst
#tablero = [(1,1),(1,2),(2,2),(2,1),(5,5),(6,6),(7,7),(8,8)]
tablero = []
tablero = make_board(8)
print(tablero)
t0 = get_t0(8,30,100)
n1 = get_worst_trap(tablero,t0,1000)
n0 = get_n0(tablero,t0,n1-1)
print("Temp chila: ", t0," peor: ", n1, " N chila: ", n0)
tablero=annealing_iter_sometimes(tablero,t0,n0)
print(tablero)
'''
print(tablero)
print(get_h_cost(tablero))
result = best_move(0,tablero)
print(result)
print(get_h_cost(result[1]))
'''





