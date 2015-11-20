import matplotlib
#matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings("ignore")

def shannon(p):
    #this will propperly treat p=1 and p=0 as values of 0
    return np.nansum(-p * np.log2(p))

def confusion_matrix(truth):
    #construct a confusion matrix that use truth to indicate the "true positive" rates for all responses
    #"false positives" are evenly split between remaining choices
    #"true positive" goes down the main diag
    N = len(truth)
    M = np.zeros([N,N])
    for ndx,n in enumerate(truth):
        other = (1 - n)/(N - 1.0)
        M[:,ndx] = other
        M[ndx,ndx] = n
    return M

def weighted_choice(weights):
    #return a random index based on the weights entered (don't need to be normalized)
    rnd = np.random.uniform(0,1) * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def clip(x, min_val=0, max_val=1):
    #make probability values stay in a sane range
    x[x>max_val] = max_val
    x[x<min_val] = min_val
    return x

def M_collection(mu, sig, N):
    truth = np.random.normal(mu, sig, size=[N, len(mu)])
    truth = clip(truth)
    M = []
    for t in truth:
        M.append(confusion_matrix(t))
    return np.array(M)

num_classifications = 30
num_bootstrap = 1000
info = np.zeros([num_classifications, num_bootstrap])
info_gain = np.zeros([num_classifications, num_bootstrap])
correctness = np.zeros([num_classifications, num_bootstrap])

N=5
mu = [.55]*N
sig = [.1]*N

for j in range(num_bootstrap):
    M = M_collection(mu, sig, num_classifications)
    P = np.array([1.0/N]*N)
    actual_classification = weighted_choice(P)
    votes = np.array([], dtype='int')
    for i in range(num_classifications):
        old_shannon = shannon(P)
        prob_classification = np.dot(M[i], P)
        report = weighted_choice(M[i,:,actual_classification])
        votes = np.append(votes, report)
        P = P * M[i, report, :] / prob_classification[report]
        assert np.isclose(sum(P), 1.0)
        new_shannon = shannon(P)
        gain = old_shannon-new_shannon
        info[i, j] = new_shannon
        info_gain[i, j] = gain
        #check if the correct answer is in the majority
        vote_count = np.bincount(votes, minlength=N)
        if np.argmax(vote_count)==actual_classification:
            correctness[i, j] = 1
        else:
            correctness[i, j] = 0

C = correctness.mean(axis=1)
S = info.mean(axis=1)
G = info_gain.mean(axis=1)
X = np.arange(1, num_classifications + 1)
x_cross = False
if max(C) >= 0.95:
    cc = interp1d(C,X)
    x_cross = cc(0.95)
    ss = interp1d(X,S)
    s_cross = ss(x_cross)
    gg = interp1d(X,G)
    g_cross = gg(x_cross)
    print "0.95 correctness crossing: {0}".format(x_cross)
    print "Bit value at crossing: {0}".format(s_cross)
    print "Delta Bit value at crossing: {0}".format(g_cross)
else:
    print "Does not cross 0.95 correctness"
print "==============="

plt.figure(1, figsize=(15,15))
plt.subplot(221)
plt.hlines(0.95, 0, num_classifications, linestyles='dashed', colors='k')
if x_cross:
    plt.vlines(x_cross, 0, 1, linestyles='dashed', colors='k')
plt.plot(X, C)
plt.ylim(0,1)
plt.xlabel("# classifications")
plt.ylabel("Correctness")
plt.subplot(222)
plt.plot(X, S)
if x_cross:
    y_lim = plt.gca().get_ylim()
    plt.hlines(s_cross, 0, num_classifications, linestyles='dashed', colors='k')
    plt.vlines(x_cross, y_lim[0], y_lim[1], linestyles='dashed', colors='k')
    plt.ylim(y_lim[0], y_lim[1])
plt.xlabel("# classifications")
plt.ylabel("Bits")
plt.subplot(223)
plt.plot(X, G)
if x_cross:
    y_lim = plt.gca().get_ylim()
    plt.hlines(g_cross, 0, num_classifications, linestyles='dashed', colors='k')
    plt.vlines(x_cross, y_lim[0], y_lim[1], linestyles='dashed', colors='k')
    plt.ylim(y_lim[0], y_lim[1])
plt.xlabel("# classifications")
plt.ylabel("Delta Bits")
plt.tight_layout()
plt.show()
