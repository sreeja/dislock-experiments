export root=/Users/snair/works/dislock-experiments/results/prediction
mkdir -p $root
> $root/log.txt

for app in sample1
do
  for granularity in 1
  do
    for mode in {1..3}
    do
      for placement in cent clust dist
      do
		    cd YCSB
        cd ..
        for op in a
        do
          for replica in x
          do
            for run in {1..5}
            do 
              mkdir $root/raw
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
                mkdir -p $root/wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$run
                ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > $root/wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$run/$location.txt & wait_pids+=($!)
                  done
                  wait "${wait_pids[@]}"
              )
              cd ..
              kill $P_PID
              cp -r $root/raw $root/wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$run/
              rm -r $root/raw
              echo "Done " $run $app $granularity $mode $placement $op $replica >> $root/log.txt
            done
          done
        done
      done
    done
  done
done