#!/usr/local/bin/perl
$maxruns = @ARGV[0];	#number of games
$cores = @ARGV[1];	#number of cpu cores

# games % cores should be 0

$time = time();
print "start time: ${time}, games: ${maxruns}, cores: ${cores} \n";

#count wins
$r = 0;
$b = 0;
$d = 0;
$div = 0;

for ($j = 0; $j < $cores; ++$j){
  my $pid = fork();
  $div = int($maxruns / $cores);

  if($pid == 0){
    $start = $j * $div;
    open(CORE, ">results/${time}_result_core${j}");
    for ($i = $start; $i < $start + $div; ++$i){

      system("python driver.py > output/${time}_run${i}");
      open(RESULT, "output/${time}_run${i}");
      @lines = <RESULT>;
      close(RESULT);
      $outcome = @lines[-1];
      chomp($outcome);
      $draw = index($outcome, "DRAW");
      $winner = substr($outcome, -1, 1);
      if($draw > 0){
        print "Core[${j}] Finished Sim $i: Draw \n";
        print CORE "Core[${j}] Finished Sim $i: Draw \n";
        ++$d;
      }
      elsif($winner eq "r"){
        print "Core[${j}] Finished Sim $i: Red Wins \n";
        print CORE "Core[${j}] Finished Sim $i: Red Wins \n";
        #dont keep files where there is a winner
        unlink("output/${time}_run${i}");
        ++$r;
      }
      elsif($winner eq "b"){
        print "Core[${j}] Finished Sim $i: Black Wins \n";
        print CORE "Core[${j}] Finished Sim $i: Black Wins \n";
        #dont keep files where there is a winner
        unlink("output/${time}_run${i}");
        ++$b;
      }
    }
    print CORE "Core[${j}] Results: R -- ${r}, B -- ${b}, D -- ${d} \n";
    close(CORE);
    exit(0);
  }
}


while( wait() != -1){}
$totaltime = (time() - $time) / 60;
print "total time(mins): ${totaltime} \n";
