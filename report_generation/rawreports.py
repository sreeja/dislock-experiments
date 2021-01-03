import os
import numpy as np
import matplotlib.pyplot as plt


def get_data(folder, wl, gran, mode, place, runs, replicas):
    configs = {}
    for g in gran:
        for m in mode:
            for p in place:
                config = '-'.join([str(g), str(m), str(p)])
                configs[config] = {}
                for r in replicas:
                    configs[config][r] = []
                    for n in runs:
                        if os.path.isfile(os.path.join(folder, wl, config, str(n), 'raw', r)):
                            with open(os.path.join(folder, wl, config, str(n), 'raw', r)) as f:
                                # print('reading', wl, config, n, r)
                                for line in f.readlines():
                                    parts = line.split(',')
                                    if len(parts) == 3 and parts[0] in ['READ','INSERT','DELETE','UPDATE']:
                                        if parts[2].strip().isnumeric():
                                            # print('adding entry', parts[2])
                                            configs[config][r] += [int(parts[2].strip())/1000]
    return configs


def generate_raw_plots(configs, replicas, name):
    fig, ax = plt.subplots()
    x_pos = np.arange(len(configs)*len(replicas))
    colors = {'paris':'red','tokyo':'green','singapore':'yellow','capetown':'blue','newyork':'magenta'}
    for c in configs:
        for r in configs[c]:
            for val in configs[c][r]:
                ax.plot(c+'-combined', val, '.', color='black')
                ax.plot(c+'-'+r, val, 'x', color=colors[r])

    plt.xticks(rotation=90)
    plt.grid(axis='y')
    # ax.legend()
    plt.savefig(name+'.png')
    plt.savefig(name+'.eps', format='eps')
    # plt.show()



folder = os.path.join('/', 'Users', 'snair', 'works',
                      'dislock-experiments', 'cluster_results', 'new', 'sample2')
workloads = ['workloadeqeq', 'workloadeqhot', 'workloadeqclust', 'workloadhoteq','workloadhothot','workloadhotclust']
gran=[1]
mode = [1,2,3]
place = [1,2,3]
runs = [1,2,3,4,5]
replicas = ['paris','tokyo','singapore','capetown','newyork']
for wl in workloads:
    configs = get_data(folder, wl, gran, mode, place, runs, replicas)
    generate_raw_plots(configs, replicas, wl)
