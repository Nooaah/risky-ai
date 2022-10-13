# HackaGames UnitTest - `pytest`

import pieceOfData as pod

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - P I E C E  O F  D A T A
# ------------------------------------------------------------------------ #

def test_Pod_init():
    gamel= pod.Pod()
    assert gamel.type() == "pod"
    assert gamel.status() == ""
    assert gamel.attributes() == []
    assert gamel.values() == []
    assert gamel.children() == []

def test_Pod_init2():
    gamel= pod.Pod( "Bob", "cool", [1, 2, 3], [4.2, 6.9] )
    assert gamel.type() == "Bob"
    assert gamel.status() == "cool"
    assert gamel.attributes() == [1, 2, 3]
    assert gamel.values() == [4.2, 6.9]
    assert gamel.children() == []
    for i in range(1,3):
        assert gamel.attribute(i) == i
    assert gamel.value(1) == 4.2
    assert gamel.value(2) == 6.9

def test_Pod_dump():
    gamel= pod.Pod()
    assert gamel.dump() == "pod 0 0 0 0 :" # set: "pod-00 (0 0 0 0) state: attrs: values: cells:"
    gamel.setAttributes([3, 8])
    assert gamel.dump() == "pod 0 2 0 0 : 3 8"
    gamel.append( pod.Pod( 'pod', 'bob happy', [4], [0.6, 10.0] ) )
    assert gamel.dump() == "pod 0 2 0 1 : 3 8\n- pod 2 1 2 0 : bob happy 4 0.6 10.0"
    gamel.append( pod.Pod() )
    assert '\n'+ gamel.dump() +'\n' == """
pod 0 2 0 2 : 3 8
- pod 2 1 2 0 : bob happy 4 0.6 10.0
- pod 0 0 0 0 :
"""

def test_Pod_load():
    gamel=pod.Pod( 'board', 'SouriCity', [3, 8] )
    gamel2=pod.Pod().load( gamel.dump() )
    assert '\n'+ gamel2.dump()  +'\n' == """
board 1 2 0 0 : SouriCity 3 8
"""
    gamel.append(pod.Pod( 'human', 'bob happy', [4] ) )
    gamel.append(pod.Pod( 'human', 'lucy' ) )
    gamel3=pod.Pod().load( gamel.dump() )
    assert '\n'+ gamel3.dump()  +'\n' == """
board 1 2 0 2 : SouriCity 3 8
- human 2 1 0 0 : bob happy 4
- human 1 0 0 0 : lucy
"""

def test_Pod_deepDump():
    gamel=pod.Pod( 'board', 'SouriCity', [3, 8] )
    bob=pod.Pod( 'human', 'bob', [4] )
    bob.append(pod.Pod('action', 'Attack', [10]) )
    bob.append(pod.Pod('action', 'Move', [], [2.0]) )
    gamel.append( bob )
    gamel.append(pod.Pod( 'human', 'lucy happy' ) )
    assert '\n'+ gamel.dump()  +'\n' == """
board 1 2 0 2 : SouriCity 3 8
- human 1 1 0 2 : bob 4
  - action 1 1 0 0 : Attack 10
  - action 1 0 1 0 : Move 2.0
- human 2 0 0 0 : lucy happy
"""

def test_Pod_deepLoad():
    gamel=pod.Pod( 'board', 'SouriCity', [3, 8] )
    bob=pod.Pod( 'human', 'bob', [4] )
    bob.append(pod.Pod('action', 'Attack', [10]) )
    bob.append(pod.Pod('action', 'Move', [], [2.0]) )
    gamel.append( bob )
    gamel.append(pod.Pod( 'human', 'lucy happy' ) )
    gamel2=pod.Pod().load( gamel.dump() )
    assert '\n'+ gamel2.dump()  +'\n' == """
board 1 2 0 2 : SouriCity 3 8
- human 1 1 0 2 : bob 4
  - action 1 1 0 0 : Attack 10
  - action 1 0 1 0 : Move 2.0
- human 2 0 0 0 : lucy happy
"""
