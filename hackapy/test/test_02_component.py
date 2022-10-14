# HackaGames UnitTest - `pytest`

import hackapy.component as cpn

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Board_init():
    board= cpn.Board(3)
    print( board )
    assert str(board) == """Board :
- Cell-1 :
- Edge-1 :
- Cell-2 :
- Edge-2 :
- Cell-3 :
- Edge-3 :"""
    assert board.cells() == [ board.child(1), board.child(3), board.child(5) ]
   
def test_Board_connection():
    board= cpn.Board(3)
    board.connect(1, 2)
    board.connect(2, 2)
    board.connect(2, 3)
    board.connect(3, 2)
    assert str(board) == """Board :
- Cell-1 :
- Edge-1 : [2]
- Cell-2 :
- Edge-2 : [2, 3]
- Cell-3 :
- Edge-3 : [2]"""

    assert board.edgesFrom(1) == [2]
    assert board.edgesFrom(2) == [2, 3]
    assert board.edgesFrom(3) == [2]
    
    assert board.isEdge(1, 2)
    assert board.isEdge(2, 2)
    assert board.isEdge(3, 2)
    assert not board.isEdge(2, 1)
    assert not board.isEdge(1, 3)
    assert not board.isEdge(3, 1)
  
def test_Board_iterator():
    board= cpn.Board(3)
    board.connect(1, 2)
    board.connect(2, 2)
    board.connect(2, 3)
    board.connect(3, 2)

    ref= [
        [ "Cell-1 :", [2]],
        [ "Cell-2 :", [2, 3]],
        [ "Cell-3 :", [2] ]
    ]
    i= 0
    for cell, edges in board :
        assert board.iCell() == i+1
        assert str(cell) == ref[i][0]
        assert edges == ref[i][1]
        i+=1
