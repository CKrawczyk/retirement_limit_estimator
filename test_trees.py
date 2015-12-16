import expected_information as ei
from pylab import *
from scipy.interpolate import interp1d

# This script will find the retirement limit for a set of trees and a set of user accuracy to get some 'rule of thumb' retirement limits

# Try various user accuracy for 1 question trees
trees1 = [
    {0: [{'next_task': 1}, {'next_task': 1}], 1: 'end'},
    {0: [{'next_task': 1}, {'next_task': 1}, {'next_task': 1}], 1: 'end'},
    {0: [{'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}], 1: 'end'},
    {0: [{'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}], 1: 'end'},
    {0: [{'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}], 1: 'end'},
    {0: [{'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}, {'next_task': 1}], 1: 'end'}
]
acc = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
X = arange(1,101)
'''
for t in trees1:
    print '=================================='
    print 'tree with {0} answers'.format(len(t[0]))
    for a in acc:
        print '----------------'
        print 'accuracy = {0}'.format(a)
        correctness, info, true_P = ei.simulate(t, accuracy=a, spread=0.1, num_classifications=100, num_bootstrap=1000, count_nulls=False)
        P = np.nanmean(true_P, axis=2)
        if (P[-1] > 0.95).any():
            P_int = interp1d(P[-1],X)
            print '0.95 confident at {0} votes'.format(P_int(0.95))
        else:
            print 'more than 100 votes for 0.95 confidence'

# Try various user accuracies for various depth trees where each question has two answers
trees2 = [
    {0: [{'next_task': 1}, {'next_task': 2}], 1: [{'next_task': 2}, {'next_task': 2}], 2: 'end'},
    {0: [{'next_task': 1}, {'next_task': 3}], 1: [{'next_task': 2}, {'next_task': 3}], 2: [{'next_task': 3}, {'next_task': 3}], 3: 'end'},
    {0: [{'next_task': 1}, {'next_task': 4}], 1: [{'next_task': 2}, {'next_task': 4}], 2: [{'next_task': 3}, {'next_task': 4}], 3: [{'next_task': 4}, {'next_task': 4}], 4: 'end'},
    {0: [{'next_task': 1}, {'next_task': 5}], 1: [{'next_task': 2}, {'next_task': 5}], 2: [{'next_task': 3}, {'next_task': 5}], 3: [{'next_task': 4}, {'next_task': 5}], 4: [{'next_task': 5}, {'next_task': 5}], 5: 'end'},
    {0: [{'next_task': 1}, {'next_task': 6}], 1: [{'next_task': 2}, {'next_task': 6}], 2: [{'next_task': 3}, {'next_task': 6}], 3: [{'next_task': 4}, {'next_task': 6}], 4: [{'next_task': 5}, {'next_task': 6}], 5: [{'next_task': 6}, {'next_task': 6}], 6: 'end'},
    {0: [{'next_task': 1}, {'next_task': 7}], 1: [{'next_task': 2}, {'next_task': 7}], 2: [{'next_task': 3}, {'next_task': 7}], 3: [{'next_task': 4}, {'next_task': 7}], 4: [{'next_task': 5}, {'next_task': 7}], 5: [{'next_task': 6}, {'next_task': 7}], 6: [{'next_task': 7}, {'next_task': 7}], 7: 'end'}
]

for t in trees2:
    print '=================================='
    print 'tree with {0} branches'.format(len(t)-1)
    for a in acc:
        print '----------------'
        print 'accuracy = {0}'.format(a)
        correctness, info, true_P = ei.simulate(t, accuracy=a, spread=0.1, num_classifications=100, num_bootstrap=1000, count_nulls=False)
        P = np.nanmean(true_P, axis=2)
        if (P[-1] > 0.95).any():
            P_int = interp1d(P[-1],X)
            print '0.95 confident at {0} votes'.format(P_int(0.95))
        else:
            print 'more than 100 votes for 0.95 confidence'

#GZ CANDELS for a range of accuracies
tree3= {
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

print 'GZ CANDELS tree'
for a in acc:
    print '----------------'
    print 'accuracy = {0}'.format(a)
    correctness, info, true_P = ei.simulate(tree3, accuracy=a, spread=0.1, num_classifications=100, num_bootstrap=1000, count_nulls=False)
    P = np.nanmean(true_P, axis=2)
    if ((P>0.95).any(axis=1)).all():
        cross = []
        for task in P:
            P_int = interp1d(task,X)
            cross.append(P_int(0.95))
        print '0.95 confident at {0} votes'.format(max(cross))
    else:
        print 'more than 100 votes for 0.95 confidence'
'''
tree4 = {
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

print 'GZ2 tree'
for a in acc:
    print '----------------'
    print 'accuracy = {0}'.format(a)
    correctness, info, true_P = ei.simulate(tree4, accuracy=a, spread=0.1, num_classifications=100, num_bootstrap=1000, count_nulls=False)
    P = np.nanmean(true_P, axis=2)
    if ((P>0.95).any(axis=1)).all():
        cross = []
        for task in P:
            P_int = interp1d(task,X)
            cross.append(P_int(0.95))
        print '0.95 confident at {0} votes'.format(max(cross))
    else:
        print 'more than 100 votes for 0.95 confidence'
