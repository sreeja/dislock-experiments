import os


def generate_workload_properties(workloadname, workload, replicas, operations, appname, outputpath, workloadpath):
    for i, each in enumerate(replicas):
        content = get_core_properties(each, outputpath)
        wl = []
        for j in range(len(operations)):
            wl += [workload[j][i]]
        content += get_workload_properties(wl)
        content += get_custom_properties(i+1, appname)
        if not os.path.exists(os.path.join(workloadpath, appname, workloadname)):
            os.makedirs(os.path.join(workloadpath, appname, workloadname))
        outputfile = os.path.join(workloadpath, appname, workloadname, each)
        with open(outputfile, 'w') as f:
            f.writelines('\n'.join(content))


def get_core_properties(replica, outputpath):
    content = []
    content += ['#	Core Properties']
    content += ['workload=site.ycsb.workloads.RestWorkload']
    content += ['db=site.ycsb.webservice.rest.RestClient']
    content += ['exporter=site.ycsb.measurements.exporter.TextMeasurementsExporter']
    content += ['threadcount=1']
    content += ['fieldlengthdistribution=uniform']
    content += ['measurementtype=raw']
    content += ['measurement.raw.output_file='+outputpath+'/raw/'+replica]
    content += ['']
    return content


def get_workload_properties(wl):
    inserts=0
    reads=0
    updates=0
    deletes=0
    if len(wl) > 3:
        inserts = wl[0]
        reads = wl[1]
        updates = wl[2]
        deletes = wl[3]
    elif len(wl) > 2:
        inserts = wl[0]
        reads = wl[1]
        updates = wl[2]
    elif len(wl) > 1:
        inserts = wl[0]
        reads = wl[1]
    elif len(wl) > 0:
        inserts = wl[0]
    total = reads + updates + deletes + inserts
    content = []
    content += ['#	Workload Properties']
    content += ['fieldcount=1']
    content += ['fieldlength=2500']
    if total:
        content += ['insertproportion='+str(inserts/total)]
        content += ['readproportion='+str(reads/total)]
        content += ['updateproportion='+str(updates/total)]
        content += ['deleteproportion='+str(deletes/total)]
    else:
        content += ['insertproportion=0']
        content += ['readproportion=0']
        content += ['updateproportion=0']
        content += ['deleteproportion=0']
    content += ['requestdistribution=uniform']
    content += ['operationcount='+str(total)]
    content += ['maxexecutiontime=72000']
    content += ['']
    return content


def get_custom_properties(replicaindex, appname, timeout=6000):
    content = []
    content += ['#	Custom Properties']
    content += ['url.prefix=http://localhost:600'+str(replicaindex)+'/']
    content += ['url.trace.read=workloads/'+appname+'/trace_insert.txt']
    content += ['url.trace.insert=workloads/'+appname+'/trace_insert.txt']
    content += ['url.trace.update=workloads/'+appname+'/trace_delete.txt']
    content += ['url.trace.delete=workloads/'+appname+'/trace_delete.txt']
    content += ['# Header must be separated by space. Other delimiters might occur as header values and hence can not be used.']
    content += ['headers=Accept */* Accept-Language en-US,en;q=0.5 Content-Type application/x-www-form-urlencoded user-agent Mozilla/5.0 Connection close']
    content += ['timeout.con='+str(timeout)]
    content += ['timeout.read='+str(timeout)]
    content += ['timeout.exec='+str(timeout)]
    return content


def generate_tracefiles(operations, paramvalues, workloadpath, appname):
    # inserts, reads, updates, deletes
    # do?op=unregisterseller&params=seller-s10
    result = []
    for i, op in enumerate(operations):
        result += [[]]
        for p in paramvalues[operations[op]]:
            result[i] += ['do?op='+op+'&params='+operations[op]+'-'+p]
    if not os.path.exists(os.path.join(workloadpath, appname)):
            os.makedirs(os.path.join(workloadpath, appname))
    result += [[] for each in range(4-len(operations))]
    for i, each in enumerate(['insert', 'read', 'update', 'delete']):
        outputfile = os.path.join(workloadpath, appname, 'trace_'+each+'.txt')
        with open(outputfile, 'w') as f:
            f.writelines('\n'.join(result[i]))


replicas = ['paris', 'tokyo', 'singapore', 'capetown', 'newyork']
workloadpath = os.path.join(os.getcwd(), 'workloads')
operations = {'operationa':'param', 'operationb':'param'}
workload = {'workloadeqeq':[[100,100,100,100,100],[100,100,100,100,100]],
            'workloadeqhot':[[500,0,0,0,0],[500,0,0,0,0]],
            'workloadhoteq':[[200,200,200,200,200],[0,0,0,0,0]],
            'workloadhothot':[[1000,0,0,0,0],[0,0,0,0,0]]}
appname = 'sample2'
paramvalues = {'param':['p1']}

generate_tracefiles(operations, paramvalues, workloadpath, appname)

for each in workload:
    outputpath = os.path.join(os.getcwd(), 'results', appname, each)
    generate_workload_properties(each, workload[each], replicas, operations, appname, outputpath, workloadpath)
