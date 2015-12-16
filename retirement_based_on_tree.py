from pylab import *
import sys
from decision_trees import get_tasks_answers

import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning,append=True)

def run(tasks, answers, Nvotes=300, Ntrials=100):
    vote_fraction = zeros([Ntrials, Nvotes, len(answers)])
    vote_total = zeros([Ntrials, Nvotes, len(answers)])
    for t in range(Ntrials):
        answer_count = {}
        for a in answers.keys():
            answer_count[a] = 0
        for i in range(Nvotes):
            next_task = 0
            while tasks[next_task] != 'end':
                ans = np.random.choice(tasks[next_task])
                next_task = answers[ans]
                answer_count[ans] += 1
            for j in tasks.keys():
                if tasks[j] != 'end':
                    tot = sum([answer_count[k] for k in tasks[j]])
                    if tot > 0:
                        for k in tasks[j]:
                            vote_fraction[t, i, k] = float(answer_count[k])/tot
                            vote_total[t, i, k] = tot
        vote_fraction_change = abs(diff(vote_fraction, axis=1))/vote_fraction[:, :-1, :]
    return vote_fraction, vote_fraction_change, vote_total

def plot_results(vote_fraction, vote_fraction_change, vote_total,save_fig=False):

    vf = nanmean(vote_fraction, axis=0)
    vfc = nanmean(vote_fraction_change, axis=0)
    vt = nanmean(vote_total, axis=0)
    
    colors = cm.Set1(linspace(0,255,len(answers)).astype(int))
    figure(1)
    for i in range(len(answers)):
        plot(vf[:,i], color=colors[i])
    xlabel('# votes')
    ylabel('vote fraction')
    title(tree)
    
    if save_fig:
        savefig("fraction_vs_votes.png")

    figure(2)
    for i in range(len(answers)):
        plot(vfc[:,i], color=colors[i])
    hlines(0.05, xmin=0, xmax=Nvotes)
    xlabel('# votes')
    ylabel('change in vote fraction')
    title(tree)
    ylim(0, 0.1)
    
    if save_fig:
        savefig("fractionchange_vs_votes.png")
    else:
        show()

if __name__ == "__main__":

    try:
        tree = sys.argv[1]
    except IndexError:
        tree = 'candels'
    
    Nvotes = 150
    Ntrials = 500
    tasks,answers = get_tasks_answers(tree)
    vote_fraction, vote_fraction_change, vote_total = run(tasks, answers, Nvotes, Ntrials)
    plot_results(vote_fraction, vote_fraction_change, vote_total,True)

