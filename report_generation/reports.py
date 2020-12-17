import os
import numpy as np
import matplotlib.pyplot as plt

operations = ['[INSERT', '[UPDATE', '[DELETE', '[READ']
replicas = ['paris', 'tokyo', 'singapore', 'capetown', 'newyork']

# configurations
# applications = ['auction1', 'auction2', 'auction3','sample']
# workloads = ['workloadax', 'workloaday', 'workloadaz', 'workloadbx',
#              'workloadby', 'workloadbz', 'workloadcx', 'workloadcy', 
#              'workloadcz', 'workloaddx', 'workloaddy', 'workloaddz']
# granularities = {'auction1': range(
#     1, 3), 'auction2': range(1, 4), 'auction3': range(1, 9),
#     'sample': range(1, 5)}
# modes = {'auction1': {1: range(1, 10), 2: range(1, 4)},
#          'auction2': {1: range(1, 28), 2: range(1, 10), 3: range(1, 4)},
#          'auction3': {1: range(1, 82), 2: range(1, 55), 3: range(1, 28), 4: range(1, 19),
#                       5: range(1, 28), 6: range(1, 19), 7: range(1, 25), 8: range(1, 17)}
#          'sample': {1: range(1, 28), 2: range(1, 10), 3: range(1, 10), 4: range(1, 4)}}
# placements = ['cent', 'clust', 'dist']

# applications = ['sample1']
# workloads = ['workloadax']
# granularities = {'sample1': range(1, 2)}
# modes = {'sample1': {1: range(1, 2)}}
# placements = ['cent']#, 'clust', 'dist']

applications = ['sample2']
workloads = ['workloadeqeq', 'workloadeqhot', 'workloadhoteq', 'workloadhothot']
granularities = {'sample2': range(1, 2)}
modes = {'sample2': {1: range(1, 4)}}
placements = {'sample2': {1: range(1, 4)}}


def get_result_app_header(app):
    return ('*'*30) + ' ' + app + ' ' + ('*'*30)


def get_result_workload_header(workload):
    return ('-'*30) + ' ' + workload + ' ' + ('-'*30)


def get_latencies(app, workload, lock_config):
    result = []
    error = []
    numbers = []
    for run in range(1, 6):
        number_of_ops = 0
        exec_time = 0
        failures = []
        for replica in replicas:
            number_of_ops_rep = 0
            exec_time_rep = 0
            file_name = os.path.join(folder, app,
                                    workload, lock_config, str(run), replica+'.txt')
            # file_name = os.path.join(folder, str(run), 'wlogs', app,
                                    # workload, lock_config, replica+'.txt')
            with open(file_name) as f:
                for line in f.readlines():
                    # print(line)
                    if line.startswith(tuple(operations)):
                        parts = [x.strip() for x in line.split(',')]
                        if 'FAILED' in parts[0] and parts[1] == 'Total Operations':
                            failures += [replica + ': ' + line.strip()]
                        elif parts[1] == 'Total Operations':
                            ops = int(parts[2])
                            number_of_ops_rep += ops
                            # print('operations', line)
                        elif 'FAILED' not in parts[0] and parts[1].strip() == 'Average':
                            if parts[2] != 'NaN':
                                exec_time_rep += ops * float(parts[2])
                            else:
                                failures += [replica + ': ' + line.strip()]
            number_of_ops += number_of_ops_rep
            exec_time += exec_time_rep
        if number_of_ops < 995 or failures:
            error += [workload + ' --- ' + lock_config + ' operations ' +
                    str(number_of_ops) + '::: ' + ','.join(failures)]
        else:
            latency = exec_time / number_of_ops / 1000.0
            result += ['lock config ' + lock_config + ' --- ' + 'run ' + str(run) + ' operations ' + str(
                number_of_ops) + ' --- ' + 'exec time ' + str(exec_time / 1000.0) + ' --- ' + 'average latency(ms) ' + str(latency)]
            numbers += [latency]
    result += ['-'*40]
    return result, error, numbers


def generate_graph(numbers_graph):
    width = 0.1
    for app in numbers_graph:
        # rows = math.ceil(len(numbers_graph[app])/2)
        fig, ax = plt.subplots(nrows=len(numbers_graph[app]), figsize=(10,10), sharex=True, sharey=False)
        fig.suptitle(app, fontsize=15)
        i = 0
        for wl in numbers_graph[app]:
            # each subplot
            x_pos = np.arange(len(numbers_graph[app][wl]))
            res1 = [np.mean(np.array(numbers_graph[app][wl][config])) for config in numbers_graph[app][wl]]
            err1 = [np.std(np.array(numbers_graph[app][wl][config])) for config in numbers_graph[app][wl]]
            bar1 = ax[i].bar(x_pos, res1, width, yerr=err1, align='center', alpha=0.5, color='white', edgecolor='black', hatch='xxx', capsize=2)

            ax[i].set_xlabel(wl)
            ax[i].set_xticks(x_pos)
            ax[i].set_xticklabels([k for k in numbers_graph[app][wl]])
            ax[i].yaxis.grid(True)
            i += 1
        plt.savefig(app+'.png')
        plt.savefig(app+'.eps', format='eps')
        plt.show()


def generate_report(folder):
    result_string = []
    error_string = []
    numbers_graph = {}
    for app in applications:
        result_string += [get_result_app_header(app)]
        numbers_graph[app] = {}
        for workload in workloads:
            numbers_graph[app][workload] = {}
            result_string += [get_result_workload_header(workload)]
            for gran in granularities[app]:
                # numbers_graph[app][workload][gran] = {}
                for mode in modes[app][gran]:
                    # numbers_graph[app][workload][gran][mode] = {}
                    for placement in placements[app][gran]:
                        print(app, workload, gran, mode, placement)
                        lock_config = str(gran)+'-'+str(mode)+'-'+str(placement)
                        result, error, number = get_latencies(
                            app, workload, lock_config)
                        result_string += result
                        error_string += error
                        # numbers_graph[app][workload][gran][mode][placement] = number
                        numbers_graph[app][workload][lock_config] = number
        result_file = os.path.join(folder, app, 'report.txt')
        with open(result_file, 'w') as rf:
            for r in result_string:
                rf.write(r + '\n')
        error_file = os.path.join(folder, app, 'error.txt')
        with open(error_file, 'w') as ef:
            for e in error_string:
                ef.write(e + '\n')

    generate_graph(numbers_graph)


# folder = os.path.join('/', 'Users', 'snair', 'works',
#                       'dislock-experiments', 'results', 'new', 'small23_1', 'locks')
folder = os.path.join('/', 'Users', 'snair', 'works',
                      'dislock-experiments', 'cluster_results')
generate_report(folder)
