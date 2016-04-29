<?php
   class MyDB extends SQLite3
   {
      function __construct($data)
      {
         $this->open($data);
      }
   }
session_start();
if (!isset($_SESSION['app2_islogged']) || $_SESSION['app2_islogged'] !== true) {
   echo "[Kirjautunut: --] ";
   echo "[ <a href='login.php'>Kirjaudu</a> ]";
}
else {
echo "[Granny: <span style='background: green;'>".$_SESSION['kayttaja']."</span> ] ";
echo"<h1>Latest input: ";
$data="recdb/".$_SESSION['uid']."/".$_SESSION['uid']."_Actions.db";
$db = new MyDB($data);
   if(!$db){
      	echo $db->lastErrorMsg();
   } else {
   //   echo "Opened database successfully\n";
   }

$sql = "SELECT Action, Reason, Time FROM TActions INNER JOIN TReason ON TActions.Action = TReason.Id INNER JOIN TTime ON TActions.TimeId = TTime.Id ORDER BY TActions.Id DESC LIMIT 1";
$ret = $db->query($sql);
//echo "<table border=10><tr><td>Uname</td><td>Uid</td></tr>";
while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
	echo $row['Reason'].' '.$row['Time'];
	$lastinput=strtotime($row['Time']);
}
$timenow = strtotime(date('Y-m-d-H:i'));
//echo "<br>".$timenow."<br>";
$tflip=($timenow-$lastinput)/60;
//echo "<br>".$tflip;
echo "</h1><br>";
if ($tflip>30){
	echo "<h2 style='color:red'>Granny might be dead. time from last input:" . $tflip . "minutes<h2><br>";
	}
$dir = "recdb/".$_SESSION['uid'];
$files = scandir($dir);
//print_r($files[2]);
$i=0;
$j=0;
foreach ($files as $f){
//echo $f;
if(substr($f, -3) == 'png'){
	$lastp= $f;
	$ftime=explode("_",$lastp);
	$ftimes[$i]=$ftime;
	$i++;
	echo "<br>".$ftime[1];
	}
}


}
//echo $lastp;
$imgaddr = "recdb/".$_SESSION['uid']."/".$lastp;
echo "Picture of latest visitor: <img src='".$imgaddr."' style='width:304px;height:228px;'><br>";

/*
$data="recdb/".$_SESSION['uid']."/".$_SESSION['uid']."_sleep.db";
//echo $data;
$db2 = new MyDB($data);

$db2 = new MyDB($data);
   if(!$db){
        echo $db->lastErrorMsg();
   } else {
   //   echo "Opened database successfully\n";
   }

$sql = "SELECT Time FROM Sleep";
$ret = $db2->query($sql);
//echo "<table border=10><tr><td>Uname</td><td>Uid</td></tr>";
while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
        echo $row['Time']."<br>";
}
*/
$sql="SELECT Time FROM TTime INNER JOIN TActions ON TTime.Id = TActions.TimeId WHERE TActions.Action = 11";
$ret = $db->query($sql);
//echo "<table border=10><tr><td>Uname</td><td>Uid</td></tr>";
echo "<form action='singlechar.php' method='POST'><select name='time'>";

while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
	echo "<option value='".$row['Time']."'>".$row['Time']."</option>";
//        echo $row['Time']."<br>";
//        $lastinput=strtotime($row['Time']);


}
echo "</select><input type='submit' name='submit'></form>"


?>
