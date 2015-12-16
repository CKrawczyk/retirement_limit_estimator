import numpy as np
from operator import itemgetter
import warnings
import sys
warnings.filterwarnings("ignore")

try:
    import progressbar as pb
    pb_installed = True
    widgets = [pb.Percentage(), pb.Bar(marker='=', left='[', right=']'), ' ', pb.ETA()]
except:
    print "a progressbar will not be shown, please install the 'probressbar' package to see one"
    pb_installed = False

def confusion_matrix(truth):
    #construct a confusion matrix that use truth to indicate the "true positive" rates for all responses
    #"false positives" are evenly split between remaining choices
    #"true positive" goes down the main diag
    N = len(truth)
    truth[truth>=1] = 0.999
    truth[truth<=0] = 0.001
    M = np.zeros([N,N + 1])
    for ndx,n in enumerate(truth):
        other = (1 - n)/(N - 1.0)
        M[:,ndx] = other
        M[ndx,ndx] = n
    #last column is for when none of the choices are "correct"
    #in that case keep the prob for each vote the same (assuming flat priors)
    #i.e. the user is likely to pick the answer they pick more often
    M[:,-1] = np.dot(M[:,:-1], np.array([1.0/N]*N))
    return M

def M_collection(mu, sig, N):
    truth = np.random.normal(mu, sig, size=[N, len(mu)])
    M = []
    for t in truth:
        M.append(confusion_matrix(t))
    return np.array(M)

def above_random(val, N):
    #Take val between [0,1] and scale it into the range of [1/N, 1]
    #i.e. 0=random guessing, 1=always right
    rand = 1.0/N
    return (1-rand)*val + rand

def scale_spread(val, N):
    #Take val and scale it by 1/N
    #i.e. let the spread of the simulated users scale depending on number of choices
    rand = 1.0/N
    return val*rand

class Task:
    def __init__(self, N, actual_classification=None, priors=None, count_nulls=True):
        '''params:
        N - Number of answers to pick from
        actual_classification - index of the correct answer, when `None` an aswers is picked at random, when `N` none of the answers are correct
            i.e., this branch of the tree is wrong
        '''
        self.count_nulls = count_nulls
        self.N = N
        if priors is not None:
            self.P = priors
        else:
            self.P = np.array([1.0/(N+1)]*(N+1))
        self.votes = np.array([], dtype='int')
        self.last_vote = None
        self.shannon = np.array([])
        self.correctness = np.array([], dtype='int')
        self.true_P = np.array([])
        if actual_classification is None:
            self.actual_classification = np.random.choice(self.N, p=self.P)
        else:
            self.actual_classification = actual_classification
    def vote(self, M, null=False):
        if null:
            self.last_vote = self.N
        else:
            self.last_vote = np.random.choice(self.N, p=M[:, self.actual_classification])
            #M contains the probabilities if the question is seen
            #The probability that the question is seen needs to be multiplied in to get the full conditional matrix
            #M *= prob_seen
            #Fill in the bottom row of the matrix based on the continuity that every column must add to 1 (keeps total prob=1)
            #M = np.vstack([M, np.ones(M.shape[1]) - M.sum(axis=0)])
            prob_classification = np.dot(M, self.P)
            P = self.P * M[self.last_vote, :] / prob_classification[self.last_vote]
            assert (P>=0).all(), "Prob < 0!, M is {0}, prob_classification is {1}, last_vote is {2}, P is {3}".format(M, prob_classification, self.last_vote, self.P)
            assert (P<=1).all(), "Prob > 1!, M is {0}, prob_classification is {1}, last_vote is {2}, P is {3}".format(M, prob_classification, self.last_vote, self.P)
            assert np.isclose(P.sum(), 1.0), "Total prob is {0} and not 1! M is {1}, prob_classification is {2}, last_vote is {3}".format(P.sum(), M, prob_classification, self.last_vote)
            self.P = P
        self.get_shannon()
        self.votes = np.append(self.votes, self.last_vote)
        self.get_correctness()
        self.get_true_P()
        return self.last_vote
    def get_shannon(self):
        #this will propperly treat p=1 and p=0 as values of 0
        if (self.count_nulls):
            new_shannon = np.nansum(-self.P * np.log2(self.P))
            self.shannon = np.append(self.shannon, new_shannon)
        else:
            if (self.last_vote < self.N):
                P = self.P[:-1]
                P /= P.sum()
                new_shannon = np.nansum(-P * np.log2(P))
                self.shannon = np.append(self.shannon, new_shannon)
            else:
                self.shannon = np.append(self.shannon, np.nan)
    def get_correctness(self):
        vote_count = np.bincount(self.votes, minlength=self.N+1)
        self.correctness = np.append(self.correctness, np.argmax(vote_count)==self.actual_classification)
    def get_true_P(self):
        if (self.count_nulls) or  ((self.last_vote < self.N) and (self.actual_classification < self.N)):
            self.true_P = np.append(self.true_P, self.P[self.actual_classification])
        else:
            self.true_P = np.append(self.true_P, np.nan)

def simulate(tree_tasks, accuracy=0.5, spread=0.1, num_classifications=50, num_bootstrap=1000, count_nulls=True):
    priors = get_priors(tree_tasks)
    num_tasks = len(tree_tasks) - 1
    info = np.zeros([num_tasks, num_classifications, num_bootstrap])
    correctness = np.zeros([num_tasks, num_classifications, num_bootstrap])
    true_P = np.zeros([num_tasks, num_classifications, num_bootstrap])
    if pb_installed:
        pbar = pb.ProgressBar(widgets=widgets, maxval=num_bootstrap)
        pbar.start()
    for j in range(num_bootstrap):
        correct_answers = {}
        next_task = 0
        while tree_tasks[next_task] != 'end':
            correct = np.random.choice(tree_tasks[next_task])
            correct_answers[next_task] = np.argmax(np.array(tree_tasks[next_task])==correct)
            next_task = correct['next_task']
        tasks = {}
        M = {}
        for k,v in tree_tasks.iteritems():
            if v == 'end':
                tasks[k] = v
            else:
                N = len(v)
                tasks[k] = Task(N, actual_classification=correct_answers.get(k, N), priors=priors[k], count_nulls=count_nulls)
                mu = [above_random(accuracy, N)]*N
                sig = [scale_spread(spread, N)]*N
                M[k] = M_collection(mu, sig, num_classifications)
        for i in range(num_classifications):
            next_task = 0
            all_tasks = tasks.keys()
            while tasks[next_task] != 'end':
                all_tasks.remove(next_task)
                last_vote = tasks[next_task].vote(M[next_task][i], null=False)
                next_task = tree_tasks[next_task][last_vote]['next_task']
            all_tasks.remove(next_task)
            for t in all_tasks:
                tasks[t].vote(M[t][i], null=True)
        for k,v in tasks.iteritems():
            if v != 'end':
                info[k, :, j] = v.shannon
                correctness[k, :, j] = v.correctness
                true_P[k, :, j] = v.true_P
        if pb_installed:
            pbar.update(j+1)
    if pb_installed:
        pbar.finish()
    return correctness, info, true_P

def do_sort(tree_tasks, t, D):
    if tree_tasks[t] != 'end':
        for a in tree_tasks[t]:
            i = a['next_task']
            if (i not in D) or (D[i] <= D[t]):
                D[i] = D[t] + 1
            do_sort(tree_tasks, i, D)
    return

def get_priors(tree_tasks):
    prob_seen = {0: 1.0}
    priors = {}
    #Make sure to iterate over the tasks in order
    task_depth = {0: 0}
    do_sort(tree_tasks, 0, task_depth)
    task_order = [x[0] for x in sorted(task_depth.iteritems(), key=itemgetter(1))]
    for t in task_order[:-1]:
        prob_lead = 1./len(tree_tasks[t])
        for adx, a in enumerate(tree_tasks[t]):
            i = a['next_task']
            if tree_tasks[i] != 'end':
                ps = prob_seen.get(i, 0)
                ps += prob_seen[t] * prob_lead
                prob_seen[i] = ps
    for k in prob_seen.keys():
        N = len(tree_tasks[k])
        priors[k] = np.array([prob_seen[k]/N]*N + [1-prob_seen[k]])
    return priors

def plot_results(correctness, info, true_P, save_fig=False):
    from matplotlib import rcParams
    import matplotlib.pyplot as plt

    #==============
    #Plotting stuff
    C = np.nanmean(correctness, axis=2)
    #S = np.nanpercentile(info, [15.9,50,84.1], axis=2)
    Sm = np.nanmean(info, axis=2)
    #P = np.nanpercentile(true_P, [15.9,50,84.1], axis=2)
    Pm = np.nanmean(true_P, axis=2)
    def fill_plot(x, percentiles, m, color):
        plt.fill_between(x, percentiles[0], percentiles[2], color=color, alpha=0.1)
        plt.plot(x, percentiles[1], color=color)
        plt.plot(x, m, color=color, ls='--')
    X = np.arange(1, info.shape[1] + 1)
    colors = list(plt.cm.YlOrRd(np.linspace(50,255,info.shape[0]).astype(int)))[::-1]
    rcParams['axes.color_cycle'] = colors

    plt.figure(1, figsize=(22,8))
    plt.subplot(131)
    plt.hlines(0.95, 0, info.shape[1], linestyles='dashed', colors='k')
    plt.hlines(0.90, 0, info.shape[1], linestyles='dashdot', colors='k')
    plt.plot(X, C.T)
    plt.ylim(0,1)
    plt.xlabel("# classifications")
    plt.ylabel("Correctness (by majority vote)")
    plt.title(tree)
    plt.legend(['Task {0}'.format(i) for i in range(info.shape[0])], loc=4)

    plt.subplot(132)
    plt.plot(X,Sm.T)
    #for cdx, c in enumerate(colors):
    #    fill_plot(X, S[cdx].T, Sm[cdx], c)
    #plt.title("Users are {0} of the way between 'random' and 'perfect' with spread of {1} of 'random'".format(accuracy, spread))
    plt.xlabel("# classifications")
    plt.ylabel("Bits contained in vote")

    plt.subplot(133)
    plt.hlines(0.95, 0, info.shape[1], linestyles='dashed', colors='k')
    plt.hlines(0.90, 0, info.shape[1], linestyles='dashdot', colors='k')
    plt.plot(X,Pm.T)
    #for cdx, c in enumerate(colors):
    #    fill_plot(X, P[cdx].T, Pm[cdx], c)
    plt.ylim(0,1)
    plt.xlabel("# classifications")
    plt.ylabel("P(actual classification | new vote)")

    plt.tight_layout()

    if save_fig:
        plt.savefig("expected_information.png")
    else:
        plt.show()

    return None


if __name__ == '__main__':

    try:
        tree = sys.argv[1]
    except IndexError:
        tree = 'candels'
    
    from decision_trees import ei_tree
    tree_tasks = ei_tree(tree)

    if tree_tasks != None:
        accuracy = 0.5
        spread = 0.1
        correctness, info, true_P = simulate(tree_tasks, accuracy=accuracy, spread=spread, num_classifications=100, num_bootstrap=1000, count_nulls=False)
        plot_results(correctness, info, true_P, save_fig=True)

