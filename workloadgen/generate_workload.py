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
    content += ['url.trace.read=workloads/'+appname+'/trace_read.txt']
    content += ['url.trace.insert=workloads/'+appname+'/trace_insert.txt']
    content += ['url.trace.update=workloads/'+appname+'/trace_update.txt']
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


replicas = ['houston', 'paris', 'singapore']    # don't change this
workloadpath = os.path.join(os.getcwd(), 'workloads', 'go')

# operations = {'operationa':'param', 'operationb':'param'}
# workload = {'workloadeqeq':[[167,167,166],[167,167,166]],
#             'workloadeqhot':[[0,500,0],[0,500,0]],
#             'workloadeqclust':[[250,250,0],[250,250,0]],
#             'workloadhoteq':[[333,334,333],[0,0,0]],
#             'workloadhothot':[[0,1000,0],[0,0,0]],
#             'workloadhotclust':[[500, 500,0],[0,0,0]],
#             'workloadG':[[0,500,0],[250,0,250]],
#             'workloadF':[[0,500,0],[167,167,166]],
# }
# appname = 'sample2'
# paramvalues = {'param':['p1']}


# operations = {'operationa':'param', 'operationb':'param'}
# workload = {'workloadeqeq':[[100,100,100,100,100],[100,100,100,100,100]],
#             'workloadeqhot':[[500,0,0,0,0],[500,0,0,0,0]],
#             'workloadeqclust':[[167,167,166,0,0],[167,166,166,0,0]],
#             'workloadhoteq':[[200,200,200,200,200],[0,0,0,0,0]],
#             'workloadhothot':[[1000,0,0,0,0],[0,0,0,0,0]],
#             'workloadhotclust':[[334,333,333,0,0],[0,0,0,0,0]],
#             'workloadG':[[500,0,0,0,0],[0,0,0,250,250]],
#             'workloadF':[[500,0,0,0,0],[100,100,100,100,100]],
# }
# appname = 'sample2'
# paramvalues = {'param':['p1']}


operations = {'operationa':'param', 'operationb':'param', 'operationc':'param'}
workload = {'workloadeqeq':[[111,111,111],[111,111,111], [111,111,111]],
            'workloadeqhot':[[0,333,0],[0,333,0],[0,333,0]],
            'workloadeqclust':[[167,167,0],[167,167,0],[167,167,0]],
            'workloadabceq':[[303,303,303],[25,25,25],[5,5,5]],
            'workloadabchot':[[0,909,0],[0,75,0],[0,15,0]],
            'workloadabcclust':[[455,455,0],[37,37,0],[8,8,0]],
            'workloadbaceq':[[25,25,25],[303,303,303],[5,5,5]],
            'workloadbachot':[[0,75,0],[0,909,0],[0,15,0]],
            'workloadbacclust':[[37,37,0],[455,455,0],[8,8,0]],
            'workloadmoreaeq':[[183,183,183],[75,75,75],[75,75,75]],
            'workloadmoreahot':[[0,550,0],[0,225,0],[0,225,0]],
            'workloadmoreaclust':[[275,275,0],[112,112,0],[112,112,0]],
            'workloadlessaeq':[[33,33,33],[150,150,150],[150,150,150]],
            'workloadlessahot':[[0,100,0],[0,450,0],[0,450,0]],
            'workloadlessaclust':[[50,50,0],[225,225,0],[225,225,0]]}
appname = 'sample3'
paramvalues = {'param':['p1']}

# operations = {'operationa':'param', 'operationb':'param', 'operationc':'param'}
# workload = {'workloadeqeq':[[75,75,75,75,75],[75,75,75,75,75], [75,75,75,75,75]],
#             'workloadeqhot':[[375,0,0,0,0],[375,0,0,0,0],[375,0,0,0,0]],
#             'workloadeqclust':[[125,125,125,0,0],[125,125,125,0,0],[125,125,125,0,0]],
#             'workloadabceq':[[200,200,200,200,200],[20,20,20,20,20],[5,5,5,5,5]],
#             'workloadabchot':[[1000,0,0,0,0],[100,0,0,0,0],[25,0,0,0,0]],
#             'workloadabcclust':[[334,333,333,0,0],[34,33,33,0,0],[9,8,8,0,0]],
#             'workloadbaceq':[[20,20,20,20,20],[200,200,200,200,200],[5,5,5,5,5]],
#             'workloadbachot':[[100,0,0,0,0],[1000,0,0,0,0],[25,0,0,0,0]],
#             'workloadbacclust':[[34,33,33,0,0],[334,333,333,0,0],[9,8,8,0,0]],
#             'workloadmoreaeq':[[125,125,125,125,125],[50,50,50,50,50],[50,50,50,50,50]],
#             'workloadmoreahot':[[625,0,0,0,0],[250,0,0,0,0],[250,0,0,0,0]],
#             'workloadmoreaclust':[[209,208,208,0,0],[84,83,83,0,0],[84,83,83,0,0]],
#             'workloadlessaeq':[[25,25,25,25,25],[100,100,100,100,100],[100,100,100,100,100]],
#             'workloadlessahot':[[125,0,0,0,0],[500,0,0,0,0],[500,0,0,0,0]],
#             'workloadlessaclust':[[42,42,41,0,0],[167,167,166,0,0],[167,167,166,0,0]]}
# appname = 'sample3'
# paramvalues = {'param':['p1']}

generate_tracefiles(operations, paramvalues, workloadpath, appname)

outputpath = os.path.join('/data/snair/golocks')
for each in workload:
    generate_workload_properties(each, workload[each], replicas, operations, appname, outputpath, workloadpath)
