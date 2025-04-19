from py_wf.node import Node 

def test_node():

    def dummy_task1():
        print ("Hello 1 !")
    
    def dummy_task2():
        print ("Hello 2 !")

    def dummy_task3():
        print("Hello 3 !")
    
    node1= Node("hello1",task=dummy_task1)
    node2= Node("hello2",task=dummy_task2)

    # check wether non unique names raise an error
    try:
        nodeInvalid = Node("hello2",task=dummy_task2 )
    except ValueError:
        pass 
    else:
        raise Exception("Non unique task name should have raised an error")
    
    node3= Node("hello3",task=dummy_task3, dependencies= [ node1,node2] )

    assert node3.dependencies[0].name == node1.name
    assert node3.dependencies[1].name == node2.name

    assert len(node3) == 3
    
    
    node3()

    for node in node3:
        assert node.name in set(["hello1","hello2","hello3"])
        print(node)
    
    node3()
    