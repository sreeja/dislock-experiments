import os
import numpy as np
import matplotlib.pyplot as plt


def get_data(folder, wl, gran, mode, place, runs, replicas):
    configs = {}
    for g in gran:
        for m in mode[g]:
            for p in place[g]:
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


def get_individual_data(folder, wl, gran, mode, place, runs, replicas):
    configs = {}
    for g in gran:
        for m in mode[g]:
            for p in place[g]:
                config = '-'.join([str(g), str(m), str(p)])
                configs[config] = {}
                for r in replicas:
                    configs[config][r] = {'READ':[],'INSERT':[],'DELETE':[],'UPDATE':[]}
                    for n in runs:
                        if os.path.isfile(os.path.join(folder, wl, config, str(n), 'raw', r)):
                            with open(os.path.join(folder, wl, config, str(n), 'raw', r)) as f:
                                # print('reading', wl, config, n, r)
                                for line in f.readlines():
                                    parts = line.split(',')
                                    if len(parts) == 3 and parts[0] in ['READ','INSERT','DELETE','UPDATE']:
                                        if parts[2].strip().isnumeric():
                                            # print('adding entry', parts[2])
                                            configs[config][r][parts[0]] += [int(parts[2].strip())/1000]
    return configs


def generate_raw_plots(configs, replicas, name1, name2):
    fig, ax = plt.subplots(figsize=(14,8))
    x_pos = np.arange(len(configs)*len(replicas))
    colors = {'paris':'red','tokyo':'green','singapore':'yellow','capetown':'blue','newyork':'magenta'}
    for c in configs:
        for r in configs[c]:
            for val in configs[c][r]:
                ax.plot(c+'-combined', val, '.', color='black')
                ax.plot(c+'-'+r, val, 'x', color=colors[r])

    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.savefig(name2+'/'+name1+'.png')
    plt.savefig(name2+'/'+name1+'.eps', format='eps')
    plt.show()


def generate_individual_raw_plots(configs, replicas, name1, name2):
    fig, ax = plt.subplots(figsize=(20,8))
    # x_pos = np.arange(len(configs)*len(replicas))
    colors = {'paris':'red','tokyo':'green','singapore':'yellow','capetown':'blue','newyork':'magenta'}
    for c in configs:
        for r in configs[c]:
            for op in configs[c][r]:
                for val in configs[c][r][op]:
                    # ax.plot(c+'-combined-'+op, val, '.', color='black')
                    ax.plot(c+'-'+r+'-'+op, val, 'x', color=colors[r])

    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.savefig(name2+'/individual'+name1+'.png')
    plt.savefig(name2+'/individual'+name1+'.eps', format='eps')
    plt.show()


def generate_box_plots(configs, replicas, name1, name2, percentile=None):
    fig, ax = plt.subplots(figsize=(14,8))
    x_pos = np.arange(len(configs)*len(replicas))
    data = {}
    for c in configs:
        data[c+'-combined'] = []
        for r in configs[c]:
            data[c+'-'+r] = []
            for val in configs[c][r]:
                data[c+'-combined'] += [val]
                data[c+'-'+r] += [val]
    if percentile:
        # print('has percentile')
        ax.boxplot(data.values(), showfliers=False, whis=[100-percentile,percentile])
    else:
        # print('no percentile, so default')
        ax.boxplot(data.values(), showfliers=False)

    plt.xticks(range(1,len(data)+1), data.keys(), rotation=90)
    plt.grid(axis='y')
    plt.savefig(name2+'/'+name1+'.png')
    plt.savefig(name2+'/'+name1+'.eps', format='eps')
    plt.show()


def generate_individual_box_plots(configs, replicas, name1, name2, percentile=None):
    fig, ax = plt.subplots(figsize=(20,8))
    # x_pos = np.arange(len(configs)*len(replicas))
    data = {}
    for c in configs:
        # for op in ['READ','INSERT','DELETE','UPDATE']:
        #     data[c+'-combined-'+op] = []
        for r in configs[c]:
            for op in configs[c][r]:
                if len(configs[c][r][op]):
                    data[c+'-'+r+'-'+op] = []
                    for val in configs[c][r][op]:
                        # data[c+'-combined-'+op] += [val]
                        data[c+'-'+r+'-'+op] += [val]
    if percentile:
        ax.boxplot(data.values(), showfliers=False, whis=[100-percentile,percentile])
    else:
        ax.boxplot(data.values(), showfliers=False)

    plt.xticks(range(1,len(data)+1), data.keys(), rotation=90)
    plt.grid(axis='y')
    plt.savefig(name2+'/individual'+name1+'.png')
    plt.savefig(name2+'/individual'+name1+'.eps', format='eps')
    plt.show()


def generate_violin_plot(configs, replicas, name1, name2):
    fig, ax = plt.subplots(figsize=(14,8))
    x_pos = np.arange(len(configs)*len(replicas))
    data = {}
    for c in configs:
        data[c+'-combined'] = []
        for r in configs[c]:
            data[c+'-'+r] = []
            for val in configs[c][r]:
                data[c+'-combined'] += [val]
                data[c+'-'+r] += [val]
    ax.violinplot(data.values())

    plt.xticks(range(1,len(data)+1), data.keys(), rotation=90)
    plt.grid(axis='y')
    plt.savefig(name2+'/'+name1+'.png')
    plt.savefig(name2+'/'+name1+'.eps', format='eps')
    plt.show()


def generate_individual_violin_plot(configs, replicas, name1, name2):
    fig, ax = plt.subplots(figsize=(20,8))
    x_pos = np.arange(len(configs)*len(replicas))
    data = {}
    for c in configs:
        for op in ['READ','INSERT','DELETE','UPDATE']:
            data[c+'-combined-'+op] = []
        for r in configs[c]:
            for op in configs[c][r]:
                # if not c+'-combined-'+op in data:
                #     data[c+'-combined-'+op] = []
                data[c+'-'+r+'-'+op] = []
                for val in configs[c][r][op]:
                    data[c+'-combined-'+op] += [val]
                    data[c+'-'+r+'-'+op] += [val]
    ax.violinplot(data.values())

    plt.xticks(range(1,len(data)+1), data.keys(), rotation=90)
    plt.grid(axis='y')
    plt.savefig(name2+'/'+name1+'.png')
    plt.savefig(name2+'/'+name1+'.eps', format='eps')
    plt.show()