

p1="minimax"
p2="minimax_old"
max=2
for i in `seq 2 $max`
do
    python gamePlay.py $p1 $p2
    python gamePlay.py $p2 $p1
done

