cd dislocksim
for placement in cent clust dist
do 
  make dockdown
  export APP=auction1
  export GRANULARITY=1
  export LOCKTYPE=1
  make dockrun &
  P_PID=$!
  sleep 60
  chmod 777 latency-$placement.sh
  ./latency-$placement.sh
  for i in {1..100}
  do
    for j in {1..5}
    do
      curl "http://localhost:600"$j"/" >> ../zoo-benchmark/$placement-$j
    done
  done
done