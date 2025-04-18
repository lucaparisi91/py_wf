from py_wf.node import Node 

def test_node():

    def dummy_task1():
        print ("Hello 1 !")
    
    def dummy_task2():
        print ("Hello 1 !")

    def dummy_task3():
        print("Hello 3")
    
    node1= Node("hello1",task=dummy_task1)
    node2= Node("hello2",task=dummy_task2)

    # check wether non unique names raise an error
    try:
        nodeInvalid = Node("hello2",task=dummy_task2 )
    except ValueError:
        pass 
    else:
        raise Exception("Non unique task name should have raised an error")
    
    node3= Node("Hello3",task=dummy_task3, dependencies= [ node1,node2] )


    # for node in node3:
    #     print(node.name)    

