cd ..
cd dislocksim-go
for placement in 1 2 3
do 
  make down
  export APP=sample2
  export GRANULARITY=1
  export MODE=2
  export PLACEMENT=$placement
  make run &
  P_PID=$!
  sleep 10
  chmod 777 latency.sh
  ./latency.sh
  
  for i in {1..1000}
  do
    curl "http://localhost:6001/do?op=operationa&params=param-p1" >> log$placement-ex-1
    curl "http://localhost:6002/do?op=operationa&params=param-p1" >> log$placement-ex-2
    curl "http://localhost:6003/do?op=operationa&params=param-p1" >> log$placement-ex-3
    curl "http://localhost:6001/do?op=operationb&params=param-p1" >> log$placement-sh-1
    curl "http://localhost:6002/do?op=operationb&params=param-p1" >> log$placement-sh-2
    curl "http://localhost:6003/do?op=operationb&params=param-p1" >> log$placement-sh-3
  done
done
cd dislocksim-go
make down