def get_decision_tree(tree):

    """
    Format used for the decision trees in expected_information.py
    """

    trees = ('gz2','candels','test1','test2')
    if tree not in trees:
        print "\nWarning: tree {0} not loaded into decision_trees.py".format(tree)
        print "Available: {0}\n".format(str(trees))
        return None

    else:
        if tree == 'candels':
            tree_tasks = {
                0:[{'next_task': 1}, {'next_task': 2}, {'next_task': 17},],
                1:[{'next_task': 16}, {'next_task': 16}, {'next_task': 16}],
                2:[{'next_task': 3}, {'next_task': 9}],
                3:[{'next_task': 7}, {'next_task': 5}, {'next_task': 4}, {'next_task': 4}, {'next_task': 4}, {'next_task': 4}],
                4:[{'next_task': 5}, {'next_task': 5}, {'next_task': 5}, {'next_task': 5}],
                5:[{'next_task': 7}, {'next_task': 6}],
                6:[{'next_task': 7}, {'next_task': 16}],
                7:[{'next_task': 8}, {'next_task': 8}],
                8:[{'next_task': 16}, {'next_task': 16}],
                9:[{'next_task': 10}, {'next_task': 11}],
                10:[{'next_task': 16}, {'next_task': 16}],
                11:[{'next_task': 12}, {'next_task': 12}],
                12:[{'next_task': 13}, {'next_task': 15}],
                13:[{'next_task': 14}, {'next_task': 14}, {'next_task': 14}],
                14:[{'next_task': 15}, {'next_task': 15}, {'next_task': 15}, {'next_task': 15}, {'next_task': 15}, {'next_task': 15}],
                15:[{'next_task': 16}, {'next_task': 16}, {'next_task': 16}],
                16:[{'next_task': 17}, {'next_task': 17}, {'next_task': 17}, {'next_task': 17}],
                17:'end'}

        elif tree == 'gz2':
            tree_tasks = {
                0:[{'next_task': 1}, {'next_task': 2}, {'next_task': 10}],
                1:[{'next_task': 9}, {'next_task': 9}, {'next_task': 9}],
                2:[{'next_task': 3}, {'next_task': 4}],
                3:[{'next_task': 9}, {'next_task': 9}, {'next_task': 9}],
                4:[{'next_task': 5}, {'next_task': 5}],
                5:[{'next_task': 6}, {'next_task': 8}],
                6:[{'next_task': 7}, {'next_task': 7}, {'next_task': 7}],
                7:[{'next_task': 8}, {'next_task': 8}, {'next_task': 8}, {'next_task': 8}, {'next_task': 8}, {'next_task': 8}],
                8:[{'next_task': 9}, {'next_task': 9}, {'next_task': 9}, {'next_task': 9}],
                9:[{'next_task': 10}, {'next_task': 10}],
                10:'end'}

        elif tree == 'test1':
            tree_tasks = {
                0:[{'next_task': 1}, {'next_task': 2}, {'next_task': 6}],
                1:[{'next_task': 3}, {'next_task': 3}],
                2:[{'next_task': 4}, {'next_task': 5}],
                3:[{'next_task': 6}, {'next_task': 6}],
                4:[{'next_task': 6}, {'next_task': 6}],
                5:[{'next_task': 6}, {'next_task': 6}],
                6:'end'}

        elif tree == 'test2':

            tree_tasks = {
                0:[{'next_task': 1}, {'next_task': 2}],
                1:[{'next_task': 3}, {'next_task': 3}],
                2:[{'next_task': 3}, {'next_task': 3}],
                3:'end'}

    return tree_tasks

def get_tasks_answers(tree):

    """
    Format used for the decision trees in retirement_based_on_tree.py
    """

    tree_tasks = get_decision_tree(tree)
    
    if tree_tasks != None:

        tasks,answers = {},{}
        tcount = 0
        for t in tree_tasks:
            if type(tree_tasks[t]) == list:
                anslist = [x+tcount for x in range(len(tree_tasks[t]))]
                tasks[t] = anslist
                tcount += len(tree_tasks[t])

                for i,a in enumerate(anslist):
                    answers[a] = tree_tasks[t][i]['next_task']
            else:
                assert tree_tasks[t] == 'end', 'String error in decision tree.'
                tasks[t] = 'end'
    
        return tasks,answers

    else:
        return None,None
