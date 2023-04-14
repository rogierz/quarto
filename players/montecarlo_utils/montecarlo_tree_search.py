import numpy as np
import time,sys,random

def traverse(node):
    while(node.is_fully_expanded()):
        if(node.is_terminal_node()):
            return node
        node = node.best_uct()
    if(node.expand()): # pick best child and return it (probably the one that just expanded)
        return node.best_uct()
    else:
        return node # ???

def resources_left(currenttime,maxtime, currentmemory,maxmemory):
    if(currenttime >= maxtime):
        return False
    if(currentmemory >= maxmemory):
        return False
    return True

def monte_carlo_tree_search(maxtime,maxnodes,root):
    ret = ""
    nodesexpanded = 0
    start = time.time()
    elapsed = 0
    while resources_left(elapsed,maxtime,nodesexpanded,maxnodes) :
        leaf = traverse(root)
        simulation_result = leaf.rollout()
        leaf.backpropagate(simulation_result)

        # resource tracking
        curr = time.time()
        elapsed = curr - start
        nodesexpanded += 1

    if(nodesexpanded>=maxnodes):
        ret = "nodes"
    elif(elapsed >= maxtime):
        ret += "time"
    else:
        ret = "neither"

    n = root.best_child()
    index_selected_piece = n.game.get_selected_piece()
    board_status = n.game.get_board_status()
    space = np.where(board_status == index_selected_piece)
    space = (space[0][0], space[1][0])
    #space = n.game.GetPieceLocation(n.parentpiece) #space parent assigned to that piece
    piece = None
    if n.is_terminal_node():
        piece = None
    elif n.best_child() is None: # if no children yet, chose random piece to give TODO: FIX ME IF POSSIBLE
        pieceint = random.randint(0,len(n.actions)-1)
        piece = n.actions[pieceint][0]
    else:
        piece = n.best_child().piece

    return piece,space,ret,n,elapsed,nodesexpanded