export root=/data/snair
> $root/log.txt

for app in auction2
do
  for granularity in 1
  do
    for mode in {1..27} 
    do
      for placement in cent clust dist
      do
		    cd YCSB
        cd ..
        for op in a
        do
          for replica in x
          do
            cd dislocksim
            export APP=$app
            export GRANULARITY=$granularity
            export LOCKTYPE=$mode
            make dockdown
            make dockrun &
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