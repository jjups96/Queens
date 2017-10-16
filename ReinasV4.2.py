import math
import random

def get_h_cost(board):
  h = 0
  for i in range(len(board)):
    #Checa Columna
    for j in range(i + 1,len(board)):
      #Checa renglon
      if board[i] == board[j]:
        h += 1
      #Diferencia entre actual y checada
      offset = j - i
      #Checa diagonales
      if board[i] == board[j] - offset or board[i] == board[j] + offset:
        h += 1
     
  return h

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
    if steps >= 50000:
      break
    
  print("\n h_cost: ", new_h_cost, "steps", steps)  
  return board
 
def make_annealing_move(board,h_to_beat,temp):
  board_copy = list(board)
  found_move = False
 
  while not found_move:
    board_copy = list(board)
    new_row = random.randint(0,len(board)-1)
    new_col = random.randint(0,len(board)-1)
    board_copy[new_col] = new_row
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
'''
Simula recibir un lugar, hace movimiento
y regresa si es mejor movimiento
'''
def make_annealing_accep(board,temp):
  '''
  new_row = random.randint(0,len(board)-1)
  new_col = random.randint(0,len(board)-1)
  board_copy[new_col] = new_row
  '''
  found_move = False
 
  h_to_beat = get_h_cost(board)
  new_col = random.randint(0,len(board)-1)
  movement = random.randint(0,1)

  if(movement==0): movement = -1
  else: movement = 1

  #print("moveX; ", movement)
  movX = board[new_col]
  if(movX > 0 and movX < len(board)-1):
      movX += movement
  elif(movX == 0):
      movX += abs(movement)
  else:
      movX -= abs(movement)

  board[new_col]= movX 
  new_h_cost = get_h_cost(board)
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

def get_t0(numQueens,t0,n):
  while(True):
    percen=0
    numAccep = 0
    for i in range(n):
      board = []
      for j in range(numQueens):
        board.append(random.randint(0,numQueens))

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
  board_copy = list(board)
  found_move = False
 
  board_copy = list(board)
  h_to_beat = get_h_cost(board_copy)
  new_col = random.randint(0,len(board)-1)
  movement = random.randint(0,1)

  if(movement==0): movement = -1
  else: movement = 1

  #print("moveX; ", movement)
  movX = board_copy[new_col]
  if(movX > 0 and movX < len(board)-1):
      movX += movement
  elif(movX == 0):
      movX += abs(movement)
  else:
      movX -= abs(movement)

  board_copy[new_col]=movX 
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
   
  if(found_move):
    return(True, board_copy)
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

tablero = []
for j in range(8):
  tablero.append(random.randint(0,8))
print(tablero)
t0 = get_t0(8,30,100)
n1 = get_worst_trap(tablero,t0,1000)
n0 = get_n0(tablero,t0,n1-1)
print("Temp chila: ", t0," peor: ", n1, " N chila: ", n0)
tablero = annealing_iter_sometimes(tablero,t0,n0)
print(tablero)
'''
t0 = get_t0(8,8,100)
tablero = [1,2,3,4,5,6,7,8]
tableroS = annealing_iter(tablero,t0)
print(tableroS)
'''
