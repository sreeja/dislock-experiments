export root=/data/snair
> $root/log.txt
for app in auction1
do
  for granularity in 1
  do
    for mode in {1..9} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 2
  do
    for mode in {1..3} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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

for app in auction2
do
  for granularity in 1
  do
    for mode in {1..27} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 2
  do
    for mode in {1..9} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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

for app in auction3
do
  for granularity in 1
  do
    for mode in {1..81} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 2
  do
    for mode in {1..54} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 3
  do
    for mode in {1..27} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 4
  do
    for mode in {1..18} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 5
  do
    for mode in {1..27} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 6
  do
    for mode in {1..18} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 7
  do
    for mode in {1..24} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
  for granularity in 8
  do
    for mode in {1..16} 
    do
      for placement in cent clust dist
      do
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
              mkdir -p wlogs/$app/workload$op$replica/$granularity-$mode-$placement
              ./bin/ycsb run rest -s -P workloads/$app/workload$op$replica/$location > wlogs/$app/workload$op$replica/$granularity-$mode-$placement/$location.txt & wait_pids+=($!)
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
