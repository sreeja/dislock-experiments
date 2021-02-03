export root=/Users/snair/works/dislock-experiments/results/prediction
# export root=/data/snair/locks
mkdir -p $root
> $root/log.txt

for app in sample2
do
  for granularity in 1
  do
    for mode in 1 2 3
    do
      for placement in 1 2 3
      do
		    cd YCSB
        cd ..
        # for workload in workloadeqeq workloadeqhot workloadeqclust workloadabceq workloadabchot workloadabcclust workloadbaceq workloadbachot workloadbacclust workloadmoreaeq workloadmoreahot workloadmoreaclust workloadlessaeq workloadlessahot workloadlessaclust
        for workload in workloadeqeq
        do
          for run in 1 2 3 4 5
          do 
            mkdir $root/raw
            cd dislocksim-go
            export APP=$app
            export GRANULARITY=$granularity
            export MODE=$mode
            export PLACEMENT=$placement
            make down
            make run &
            P_PID=$!
            sleep 60
            chmod 777 latency.sh
            ./latency.sh
            cd ..
            cd YCSB
            (
                for location in houston paris singapore
                do
              mkdir -p $root/wlogs/$app/$workload/$granularity-$mode-$placement/$run
              ./bin/ycsb run rest -s -P workloads/go/$app/$workload/$location > $root/wlogs/$app/$workload/$granularity-$mode-$placement/$run/$location.txt & wait_pids+=($!)
                done
                wait "${wait_pids[@]}"
            )
            cd ..
            kill $P_PID
            cp -r $root/raw $root/wlogs/$app/$workload/$granularity-$mode-$placement/$run/
            rm -r $root/raw
            echo "Done " $run $app $granularity $mode $placement $workload >> $root/log.txt
          done
        done
      done
    done
  done
done