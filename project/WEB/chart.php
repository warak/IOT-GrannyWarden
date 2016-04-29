<?php // content="text/plain; charset=utf-8"
require_once ('jpgraph-3.5.0b1/src/jpgraph.php');
require_once ('jpgraph-3.5.0b1/src/jpgraph_line.php');

session_start();
//echo "<h1>".$_POST['time']."</h1>";
if (!isset($_SESSION['app2_islogged']) || $_SESSION['app2_islogged'] !== true) {
   echo "Session expired ";
   echo "[ <a href='login.php'>login</a> ]";
}

class MyDB extends SQLite3
   {
      function __construct($data)
      {
         $this->open($data);
      }
   }

if(!isset($_POST['time'])){
echo "time is not set go set it  <a href='main.php'>main</a>";
exit;
}


$data = "recdb/".$_SESSION['uid']."/".$_SESSION['uid']."_sleep.db";
//echo $data;
$db = new MyDB($data);
   if(!$db){
	echo $db->lastErrorMsg();
	echo"data is missing! go back to main page <a href='main.php'>main</a>";
   } else {
//      echo "Opened database successfully\n";
   }
$data2="recdb/".$_SESSION['uid']."/".$_SESSION['uid']."_Actions.db";
$db2 = new MyDB($data2);
   if(!$db2){
        echo $db->lastErrorMsg();
        echo"data is missing! go back to main page <a href='main.php'>main</a>";
   } else {
//      echo "Opened database successfully\n";
   }
$sql2="SELECT Time From TTime INNER JOIN TActions ON TTime.Id = TActions.TimeId WHERE TActions.Action = 12 AND TTime.Time > '".$_POST['time']."' ORDER BY TTime.Time LIMIT 1";
$ret = $db2->query($sql2);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
	$wakeup=$row['Time'];
}
//echo $wakeup;

$sql ="SELECT * FROM Sleep WHERE Time >= '".$_POST['time']."%' AND Time <= '". $wakeup."%'";
//$sql = "SELECT * FROM Sleep WHERE Time >= '2016-04-20 16:54%'";
$ret = $db->query($sql);
$i=0;

while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
        $parse=explode(".",$row['Time']);
	$datay1[$i]=$row['X'];
	$datay2[$i]=$row['Y'];
	$datay3[$i]=$row['Z'];
	$time[$i]=$parse[0];
	$i++;
}

$graph = new Graph(1400,800);
$graph->SetScale("textlin");

$theme_class=new UniversalTheme;

$graph->SetTheme($theme_class);
$graph->img->SetAntiAliasing(false);
$graph->title->Set('These points of data make a beutiful line');
$graph->SetBox(false);

$graph->img->SetAntiAliasing();

$graph->yaxis->HideZeroLabel();
$graph->yaxis->HideLine(false);
$graph->yaxis->HideTicks(false,false);

$graph->xgrid->Show();
$graph->xgrid->SetLineStyle("solid");
$graph->xaxis->SetTickLabels($time);
$graph->xgrid->SetColor('#E3E3E3');

// Create the first line
$p1 = new LinePlot($datay1);
$graph->Add($p1);
$p1->SetColor("#6495ED");
$p1->SetLegend('X');

// Create the second line
$p2 = new LinePlot($datay2);
$graph->Add($p2);
$p2->SetColor("#B22222");
$p2->SetLegend('Y');

// Create the third line
$p3 = new LinePlot($datay3);
$graph->Add($p3);
$p3->SetColor("#FF1493");
$p3->SetLegend('Z');

$graph->legend->SetFrameWeight(1);

// Output line
$graph->Stroke();
//echo "these points of data make a beautiful line";
?>
