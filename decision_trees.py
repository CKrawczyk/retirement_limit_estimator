def get_tasks_answers(tree):

    """
    tasks = {task_key: [list of answer_keys]}
    answers = {answer_key: next task_key}

    Used in retirement_based_on_tree.py
    """

    trees = ('gz2','candels','test1','test2')
    if tree not in trees:
        print "\nWarning: tree {0} not loaded into decision_trees.py".format(tree)
        print "Available: {0}\n".format(str(trees))
        return None,None

    else:
        if tree == 'gz2':

            # Galaxy Zoo 2

            tasks = {0:[0,1,2], 1:[3,4,5], 2:[6,7], 3:[8,9,10], 4:[11,12], 5:[13,14], 6:[15,16,17], 7:[18,19,20,21,22,23], 8:[24,25], 9:'end'}
            answers = {0:1, 1:2, 2:9, 3:8, 4:8, 5:8, 6:3, 7:4, 8:8, 9:8, 10:8, 11:5, 12:5, 13:6, 14:8, 15:7, 16:7, 17:7, 18:8, 19:8, 20:8, 21:8, 22:8, 23:8, 24:9, 25:9}
        
        elif tree == 'candels':

            # Galaxy Zoo: CANDELS

            tasks = {0:[0,1,2], 1:[3,4,5], 2:[6,7], 3:[8,9,10,11,12,13], 4:[14,15,16,17], 5:[18,19], 6:[20,21], 7:[22,23], 8:[24,25], 9:[26,27], 10:[28,29], 11:[30,31], 12:[32,33], 13:[34,35,36], 14:[37,38,39,40,41,42], 15:[43, 44, 45], 16:[46,47,48,49], 17:'end'}
            answers = {0:1, 1:2, 2:17, 3:16, 4:16, 5:16, 6:3, 7:9, 8:7, 9:5, 10:4, 11:4, 12:4, 13:4, 14:5, 15:5, 16:5, 17:5, 18:7, 19:6, 20:7, 21:16, 22:8, 23:8, 24:16, 25:16, 26:10, 27:11, 28:16, 29:16, 30:12, 31:12, 32:13, 33:15, 34:14, 35:14, 36:14, 37:15, 38:15, 39:15, 40:15, 41:15, 42:15, 43:16, 44:16, 45:16, 46:17, 47:17, 48:17, 49:17}

        elif tree == 'test1':

            # Simple test batch with 4 questions, 9 answers

            tasks = {0:[0, 1], 1:[2, 3, 4], 2:[5, 6, 7], 3:[8], 4:'end'}
            answers = {0:1, 1:4, 2:2, 3:2, 4:2, 5:3, 6:3, 7:3, 8:4}
            
        elif tree == 'test2':

            # Simple test batch with 5 questions, 13 answers

            tasks = {0:[0, 1, 2], 1:[3, 4], 2:[5, 6], 3:[7, 8], 4:[9, 10], 5:[11, 12], 6:'end'}
            answers = {0:1, 1:2, 2:6, 3:3, 4:3, 5:4, 6:5, 7:6, 8:6, 9:6, 10:6, 11:6, 12:6}

        return tasks,answers

def ei_tree(tree):

    # Return decision tree in format for expected_information.py

    tasks,answers = get_tasks_answers(tree)

    if tasks != None:
        tree_tasks = {}
        for t in tasks:
            anslist = tasks[t]
            if type(anslist) == list:
                tree_tasks[t] = []
                for a in anslist:
                    tree_tasks[t].append({'next_task':answers[a]})
            else:
                assert anslist == 'end', 'String error in decision tree.'
                tree_tasks[t] = anslist

        return tree_tasks
    else:
        return None

