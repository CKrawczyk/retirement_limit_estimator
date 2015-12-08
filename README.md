# retirement_based_on_tree.py
Estimate the "worst case scenario" retirement limit based on question tree structure
This will give the "time to saturation" of random votes down the tree.

#expected_information.py
##overview
Extends on the work started by Space Warps for full question trees.

Each user is assumed to have a "correctness" values (main diag of the confusion matrix) taken from a normal distribution with mean "accuracy" (0=random votes, 1=perfect votes) and standard deviation "spread" (as a fraction of a random vote.  E.g., for a 2 answer question spread is x*0.5).  The off diag terms of the confusion matrix are equally spread between the remaining answers.  

The last column of the confusion matrix represents the probability of voting for each answer given the true answer is "null" (i.e., not seen).  These values are taken to keep the total probability of voting for each answer the same assuming flat priors.

The priors for the answers of each question are taken to be flat but the prior for "null" is calculated as the likelihood it will be missed (based on all previous questions having a flat prior).

The derivation for the math used: https://docs.google.com/a/zooniverse.org/document/d/1wD_zK0K3_o4mq4lbavFv2G91S6DHnIzjVptWvb9hVkg/edit?usp=sharing

##function usage
Basic usage is provided in an example below at the bottom of the code.  Here is a quick summary:

```python
correctness, info, true_P = simulate(tree_tasks, accuracy=0.5, spread=0.1, num_classifications=50, num_bootstrap=1000, count_nulls=False)
```

###inputs
`tree_tasks` is a dict containing the shape of the decision tree. Each item of the dictionary contains a list of dicts pointing to the next task for each answer to that task. Example:
```python
tree_tasks = {
  0:[{'next_task': 1}, {'next_task': 2}],
  1:[{'next_task': 3}, {'next_task': 3}],
  2:[{'next_task': 3}, {'next_task': 3}],
  3:'end'}
```

`accuracy` sets the mean of the normal distribution accuracy is taken from. 0=random votes, 1=perfect votes

`spread` sets the width of the normal distribution accuracy is taken from (as a fraction of a random vote accuracy).

`num_classifications` number of classifiers to simulate.

`num_bootstrap` number of times to run the simulation.

`count_nulls` weather to count "missed" votes on the question in the calculation of information and true probabilities (matched expected values when set to `False`).

###outputs
`correctness` an array of shape `[N_tasks, num_bootstrap, num_classifications]` giving either `0` or `1` indicating if the user got the task correct. `np.nanmean(correctness, axis=2)` is useful for plotting.

`info` an array of shape `[N_tasks, num_bootstrap, num_classifications]` giving the amount of information contained in each vote. `np.nanmean(info, axis=2)` is useful for plotting.

`true_P`an array of shape `[N_tasks, num_bootstrap, num_classifications]` giving the probability of the correct answer given each vote. `np.nanmean(true_P, axis=2)` is useful for plotting. NOTE: the average of this value over all bootstaps should be the same as the average of correctness over all bootstaps, but the correctness average breaks down for questions deep in the tree due to "null" votes.  This value is the one the retirement should be based on.
