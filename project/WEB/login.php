<?php
session_start();
$errmsg = '';

if (isset($_POST['nick']) AND isset($_POST['salasana'])) {

	$usr = $_POST["nick"];

	$db = new SQLite3('recdb/grannylist.db');
   	if(!$db){
      		echo $db->lastErrorMsg();
   	} else {
   	//   echo "Opened database successfully\n";
  	}

	$sql = "SELECT Uid FROM Grannys WHERE Username = '".$usr."'";
	$ret = $db->query($sql);
        while($row = $ret->fetchArray()){
        	$uid = $row['Uid'];
        }
        //$ret = '5L7VDF04SZ6MTQJ';
	//echo $ret;
	$salasana = $_POST['salasana'];	

	$_SESSION['app2_islogged'] = true;
	$_SESSION['uid'] = $uid;
	$_SESSION['kayttaja'] = $usr;

	header("Location: http://" . $_SERVER['HTTP_HOST']
               . dirname($_SERVER['PHP_SELF']) . '/'
               . "main.php");
		exit;
/*		else {

			$errmsg = '<span style="background: yellow;">Tunnus/Salasana vaarin!</span>';

		}*/

}

?>

<?php

if ($errmsg != '')echo $errmsg;

?>

<form action="<?php echo $_SERVER['PHP_SELF'];?>" method="POST">

Kayttajanimi:<input type="text" name="nick" value=""><br>

Salasana:<input type="password" name="salasana" value="" size="3"><br>

<input type='submit' value='laheta'><br>
