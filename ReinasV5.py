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

def make_move_steepest_hill(board):
  moves = {}
  for col in range(len(board)):
    best_move = board[col]
     
    for row in range(len(board)):
      if board[col] == row:
        #No evaluamos el actual
        continue
       
      board_copy = list(board)
      #Mover a nuevo renglon
      board_copy[col] = row
      moves[(col,row)] = get_h_cost(board_copy)
   
  best_moves = []
  h_to_beat = get_h_cost(board)
  for k,v in moves.iteritems():
    if v < h_to_beat:
      h_to_beat = v
       
  for k,v in moves.iteritems():
    if v == h_to_beat:
      best_moves.append(k)
   
  #Mejor movimiento al azar
  if len(best_moves) > 0:
    pick = random.randint(0,len(best_moves) - 1)
    col = best_moves[pick][0]
    row = best_moves[pick][1]
    board[col] = row
   
  return board

def make_gready(board):
  h_to_beat = get_h_cost(board)
  for col in range(len(board)): 
    for row in range(len(board)):
      if board[col] == row:
        #No evaluamos el actual
        continue
       
      board_copy = list(board)
      #Mover a nuevo renglon
      board_copy[col] = row
      new_h_cost = get_h_cost(board_copy)
       
      #Hacer mejor primer movimiento
      if new_h_cost < h_to_beat:
        board[col] = row
        return board

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
    posQueen1 = random.randint(0,len(board)-1)
    posQueen2 = random.randint(0,len(board)-1)
    board_copy[posQueen1], board_copy[posQueen2] = board_copy[posQueen2], board_copy[posQueen1]
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

tablero = [0,1,2,3,4,5,6,7]

tableroS = annealing(tablero)

print(tableroS)
