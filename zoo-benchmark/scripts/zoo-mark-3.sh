for placement in cent clust dist
do 
  cd dislocksim
  make dockdown
  export APP=auction1
  export GRANULARITY=1
  export LOCKTYPE=1
  make dockrun &
  P_PID=$!
  sleep 60
  chmod 777 latency-$placement.sh
  ./latency-$placement.sh
  cd ..
  chmod 777 paris-diff.sh
  chmod 777 singapore-diff.sh
  chmod 777 newyork-diff.sh
  ./paris-diff.sh >> zoo-benchmark/3/mutex-concurrent-diff-nowait/$placement-1 & wait_pids+=($!)
  ./singapore-diff.sh >> zoo-benchmark/3/mutex-concurrent-diff-nowait/$placement-3 & wait_pids+=($!)
  ./newyork-diff.sh >> zoo-benchmark/3/mutex-concurrent-diff-nowait/$placement-5 & wait_pids+=($!)
  wait "${wait_pids[@]}"

  chmod 777 paris.sh
  chmod 777 singapore.sh
  chmod 777 newyork.sh
  ./paris.sh >> zoo-benchmark/3/mutex-concurrent-nowait/$placement-1 & wait_pids+=($!)
  ./singapore.sh >> zoo-benchmark/3/mutex-concurrent-nowait/$placement-3 & wait_pids+=($!)
  ./newyork.sh >> zoo-benchmark/3/mutex-concurrent-nowait/$placement-5 & wait_pids+=($!)
  wait "${wait_pids[@]}"

  # for i in {1..100}
  # do
  #   for j in {1..5}
  #   do
  #     curl "http://localhost:600"$j"/" >> ../zoo-benchmark/mutex/$placement-$j
  #   done
  # done
  # sleep 30
  for i in {1..100}
  do
    for j in 1 3 5
    do
      curl "http://localhost:600"$j"/" >> zoo-benchmark/3/mutex-concurrent/$placement-$j & wait_pids+=($!)
    done
    wait "${wait_pids[@]}"
  done
  sleep 30
  for i in {1..100}
  do
    for j in 1 3 5
    do
      curl "http://localhost:600"$j"/zoo" >> zoo-benchmark/3/mutex-concurrent-diff/$placement-$j & wait_pids+=($!)
    done
    wait "${wait_pids[@]}"
  done
  # sleep 30
  # for i in {1..100}
  # do
  #   for j in {1..5}
  #   do
  #     curl "http://localhost:600"$j"/" >> ../zoo-benchmark/mutex-concurrent-multithread/$placement-$j & 
  #   done
  # done
  # sleep 30
  # for i in {1..100}
  # do
  #   for j in {1..5}
  #   do
  #     curl "http://localhost:600"$j"/zoo" >> ../zoo-benchmark/mutex-concurrent-diff-multithread/$placement-$j & 
  #   done
  # done
  # export APP=auction1
  # export GRANULARITY=1
  # export LOCKTYPE=6
  # make dockrun &
  # P_PID=$!
  # sleep 60
  # chmod 777 latency-$placement.sh
  # ./latency-$placement.sh
  # for i in {1..100}
  # do
  #   for j in {1..5}
  #   do
  #     curl "http://localhost:600"$j"/zoo" >> ../zoo-benchmark/mutex-concurrent-diff/$placement-$j &
  #   done
  # done
  # make dockdown
done
cd dislocksim
make dockdown