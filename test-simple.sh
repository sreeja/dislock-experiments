export root=/Users/snair/works
> $root/log.txt

for app in auction2
do
  for granularity in 1
  do
    for mode in 17
    do
      for placement in dist
      do
        for op in c
        do
          for replica in z
          do
            cd cc-experiment
            export APP=$app
            export GRANULARITY=$granularity
            export LOCKTYPE=$mode
            make dockdown-cent
            make dockdown-clust
            make dockdown-dist
            make dockrun-$placement &
            P_PID=$!
            sleep 60
            chmod 777 latency-$placement.sh
            ./latency-$placement.sh
            cd ..
            cd YCSB
            (
                for location in paris tokyo singapore capetown newyork
                do
              mkdir -p $root/wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > $root/wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
                done
                wait "${wait_pids[@]}"
            )
            cd ..
            kill $P_PID
            echo "Done " $app $granularity $mode $placement $op $replica >> $root/log.txt
          done
        done
      done
    done
  done
done