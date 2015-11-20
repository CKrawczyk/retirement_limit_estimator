from pylab import *

#task = {task_key: [list of answer_keys]}
#answer = {answer_key: next task_key}

#GZ2
#task = {0:[0,1,2], 1:[3,4,5], 2:[6,7], 3:[8,9,10], 4:[11,12], 5:[13,14], 6:[15,16,17], 7:[18,19,20,21,22,23], 8:[24,25], 9:'end'}
#answer = {0:1, 1:2, 2:9, 3:8, 4:8, 5:8, 6:3, 7:4, 8:8, 9:8, 10:8, 11:5, 12:5, 13:6, 14:8, 15:7, 16:7, 17:7, 18:8, 19:8, 20:8, 21:8, 22:8, 23:8, 24:9, 25:9}

#GZ CANDELS
task = {0:[0,1,2], 2:[3,4,5], 3:[6,7], 4:[8,9,10,11,12,13], 5:[14,15,16,17], 6:[18,19], 7:[20,21], 8:[22,23], 9:[24,25], 10:[26,27], 11:[28,29], 12:[30,31], 13:[32,33], 14:[34,35,36], 15:[37,38,39,40,41,42], 16:[43, 44, 45], 17:[46,47,48,49], 18:'end'}
answer = {0:2, 1:3, 2:18, 3:17, 4:17, 5:17, 6:4, 7:10, 8:8, 9:6, 10:5, 11:5, 12:5, 13:5, 14:6, 15:6, 16:6, 17:6, 18:8, 19:7, 20:8, 21:8, 22:9, 23:9, 24:17, 25:17, 26:11, 27:12, 28:17, 29:17, 30:13, 31:13, 32:14, 33:16, 34:15, 35:15, 36:15, 37:16, 38:16, 39:16, 40:16, 41:16, 42:16, 43:17, 44:17, 45:17, 46:18, 47:18, 48:18, 49:18}

#Test 1
#task = {0:[0, 1], 1:[2, 3, 4], 2:[5, 6, 7], 3:[8], 4:'end'}
#answer = {0:1, 1:4, 2:2, 3:2, 4:2, 5:3, 6:3, 7:3, 8:4}

#Test 2
#task = {0:[0, 1, 2], 1:[3, 4], 2:[5, 6], 3:[7, 8], 4:[9, 10], 5:[11, 12], 6:'end'}
#answer = {0:1, 1:2, 2:6, 3:3, 4:3, 5:4, 6:5, 7:6, 8:6, 9:6, 10:6, 11:6, 12:6}

def run(task, answer, N=300, Ntrials=100):
    vote_fraction = zeros([Ntrials, N, len(answer)])
    vote_total = zeros([Ntrials, N, len(answer)])
    for t in range(Ntrials):
        answer_count = {}
        for a in answer.keys():
            answer_count[a] = 0
        for i in range(N):
            next_task = 0
            while task[next_task] != 'end':
                ans = np.random.choice(task[next_task])
                next_task = answer[ans]
                answer_count[ans] += 1
            for j in task.keys():
                if task[j] != 'end':
                    tot = sum([answer_count[k] for k in task[j]])
                    if tot > 0:
                        for k in task[j]:
                            vote_fraction[t, i, k] = float(answer_count[k])/tot
                            vote_total[t, i, k] = tot
        vote_fraction_change = abs(diff(vote_fraction, axis=1))/vote_fraction[:, :-1, :]
    return vote_fraction, vote_fraction_change, vote_total

N=150
vote_fraction, vote_fraction_change, vote_total = run(task, answer, N=N, Ntrials=500)

vf = nanmean(vote_fraction, axis=0)
vfc = nanmean(vote_fraction_change, axis=0)
vt = nanmean(vote_total, axis=0)

colors = cm.Set1(linspace(0,255,len(answer)).astype(int))
figure(1)
for i in range(len(answer)):
    plot(vf[:,i], color=colors[i])
xlabel('# votes')
ylabel('vote fraction')

figure(2)
for i in range(len(answer)):
    plot(vfc[:,i], color=colors[i])
hlines(0.05, xmin=0, xmax=N)
xlabel('# votes')
ylabel('change in vote fraction')
ylim(0, 0.1)

show()
