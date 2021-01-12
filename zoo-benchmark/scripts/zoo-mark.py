import os
import numpy as np
import matplotlib.pyplot as plt


def autolabel(rects, j, i):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax[j,i].text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%f' % height,
                ha='center', va='bottom', rotation='vertical')

# fig, ax = plt.subplots(nrows=3, ncols=5, figsize=(11.69,8.27), sharex=True, sharey=True)
fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(9,7), sharex=True, sharey=True)

# Set the title for the figure
# fig.suptitle('Zookeeper benckmarks', fontsize=15)
j=0
for mode in ['shared', 'exclusive', 'mutex']:
    i = 0
    # for exp in ['', '-concurrent', '-concurrent-diff', '-concurrent-nowait', '-concurrent-diff-nowait']:
    for exp in ['', '-concurrent-nowait', '-concurrent-diff-nowait']:
        responses = {}
        for placement in ['cent', 'clust', 'dist']:
            responses[placement] = {}
            for replica in [1,2,3,4,5]:
                responses[placement][replica] = []
                filename = os.path.join('/Users/snair/works/dislock-experiments', 'zoo-benchmark', mode+exp, placement+'-'+str(replica))
                with open(filename) as f:
                    for line in f.readlines():
                        parts = line.split(':')
                        if len(parts) > 2:
                            responses[placement][replica] += [float(parts[2].strip())]

        x_pos = np.arange(3)
        width = 0.1
        resp0 = [np.mean(np.array(responses[placement][1])) for placement in responses]
        resperr0 = [np.std(np.array(responses[placement][1])) for placement in responses]
        resp1 = [np.mean(np.array(responses[placement][2])) for placement in responses]
        resperr1 = [np.std(np.array(responses[placement][2])) for placement in responses]
        resp2 = [np.mean(np.array(responses[placement][3])) for placement in responses]
        resperr2 = [np.std(np.array(responses[placement][3])) for placement in responses]
        resp3 = [np.mean(np.array(responses[placement][4])) for placement in responses]
        resperr3 = [np.std(np.array(responses[placement][4])) for placement in responses]
        resp4 = [np.mean(np.array(responses[placement][5])) for placement in responses]
        resperr4 = [np.std(np.array(responses[placement][5])) for placement in responses]

        # fig, ax = plt.subplots()
        bar0 = ax[j,i].bar(x_pos - 2*width, resp0, width, yerr=resperr0, align='center', alpha=0.5, color='green', edgecolor='black', hatch='+++', capsize=2)
        bar1 = ax[j,i].bar(x_pos - width, resp1, width, yerr=resperr1, align='center', alpha=0.5, color='white', edgecolor='black', hatch='///', capsize=2)
        bar2 = ax[j,i].bar(x_pos, resp2, width, yerr=resperr2, align='center', alpha=0.5, color='red', edgecolor='black', hatch='', capsize=2)
        bar3 = ax[j,i].bar(x_pos + width, resp3, width, yerr=resperr3, align='center', alpha=0.5, color='yellow', edgecolor='black', hatch='xxx', capsize=2)
        bar4 = ax[j,i].bar(x_pos + 2*width, resp4, width, yerr=resperr4, align='center', alpha=0.5, color='blue', edgecolor='black', hatch='---', capsize=2)
        autolabel(bar0, j, i)
        autolabel(bar1, j, i)
        autolabel(bar2, j, i)
        autolabel(bar3, j, i)
        autolabel(bar4, j, i)
        ax[j,i].set_xlabel(mode+exp)
        ax[j,i].set_xticks(x_pos)
        # ax[i].set_xlabel('Placement of zookeeper servers')
        ax[j,i].set_xticklabels(['P', 'P, C, N', 'all'])

        ax[j,i].yaxis.grid(True)
        # ax[i].plot(x, y1)
        # ax[i].set_title(exp)
        # ax[j,i].legend((bar0[0], bar1[0], bar2[0], bar3[0], bar4[0]), ('paris', 'tokyo', 'singapore', 'capetown', 'newyork'), bbox_to_anchor=(0., 1.02, 1., .5), loc='lower right', borderaxespad=0., mode="expand", ncol=3)

        i += 1
    j += 1

fig.legend((bar0[0], bar1[0], bar2[0], bar3[0], bar4[0]), ('paris', 'tokyo', 'singapore', 'capetown', 'newyork'), loc = 'upper center', ncol=5)

plt.savefig('zoo-benchmark-3-new.png')
plt.savefig('zoo-benchmark-3-new.eps', format='eps')
plt.show()
