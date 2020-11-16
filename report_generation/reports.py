import os

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

applications = ['sample']
workloads = ['workloadbx', 'workloadby', 'workloadbz']
granularities = {'sample': range(4, 5)}
modes = {'sample': {1: range(1, 28), 2: range(1, 10), 3: range(1, 10), 4: range(1, 5)}}
placements = ['cent', 'clust', 'dist']

# applications = ['sample']
# workloads = ['workloadcx']
# granularities = {'sample': range(3, 4)}
# modes = {'sample': {3: range(1, 2)}}
# placements = ['cent', 'clust', 'dist']


def get_result_app_header(app):
    return ('*'*30) + ' ' + app + ' ' + ('*'*30)


def get_result_workload_header(workload):
    return ('-'*30) + ' ' + workload + ' ' + ('-'*30)


def get_latencies(app, workload, gran, mode, placement):
    print(app, workload, gran, mode, placement)
    result = []
    error = []
    lock_config = str(gran)+'-'+str(mode)+'-'+placement
    for run in range(1, 6):
        number_of_ops = 0
        exec_time = 0
        failures = []
        for replica in replicas:
            number_of_ops_rep = 0
            exec_time_rep = 0
            # file_name = os.path.join(folder, 'wlogs', app,
                                    # workload, lock_config, str(run), replica+'.txt')
            file_name = os.path.join(folder, str(run), 'wlogs', app,
                                    workload, lock_config, replica+'.txt')
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
        if number_of_ops < 4995: # or failures:
            error += [workload + ' --- ' + lock_config + ' operations ' +
                    str(number_of_ops) + '::: ' + ','.join(failures)]
        else:
            latency = exec_time / number_of_ops / 1000.0
            result += ['lock config ' + lock_config + ' --- ' + 'run ' + str(run) + ' operations ' + str(
                number_of_ops) + ' --- ' + 'exec time ' + str(exec_time / 1000.0) + ' --- ' + 'average latency(ms) ' + str(latency)]
    result += ['-'*40]
    return result, error


def generate_report(folder):
    result_string = []
    error_string = []
    for app in applications:
        result_string += [get_result_app_header(app)]
        for workload in workloads:
            result_string += [get_result_workload_header(workload)]
            for gran in granularities[app]:
                for mode in modes[app][gran]:
                    for placement in placements:
                        result, error = get_latencies(
                            app, workload, gran, mode, placement)
                        result_string += result
                        error_string += error
    result_file = os.path.join(folder, 'report.txt')
    with open(result_file, 'w') as rf:
        for r in result_string:
            rf.write(r + '\n')
    error_file = os.path.join(folder, 'error.txt')
    with open(error_file, 'w') as ef:
        for e in error_string:
            ef.write(e + '\n')


folder = os.path.join('/', 'Users', 'snair', 'works',
                      'dislock-experiments', 'results', 'new', 'small22_1', 'locks')
generate_report(folder)
