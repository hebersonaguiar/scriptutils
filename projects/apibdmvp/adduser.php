<?php
header("Access-Control-Allow-Origin: *");
$servername = "mysql";
$username = "root";
$password = "my-secret-pw";
$dbname = "appmvp";

try {
	$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
	// set the PDO error mode to exception
	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	$cpf_p     	  	= $_POST['cpf_p'];
	$firstname_p  	= $_POST['firstname_p'];
	$lastname_p   	= $_POST['lastname_p'];
	$login_p 	  	= $_POST['login_p'];
	$department_p 	= $_POST['department_p'];
	$rg_p  		  	= $_POST['rg_p'];
	$room_p   	  	= $_POST['room_p'];
	$phone_p   	  	= $_POST['phone_p'];
	$ticketid_p	  	= $_POST['ticketid_p'];
	$ticketnumber_p = $_POST['ticketnumber_p'];

	$sql = "INSERT INTO items (cpf, firstname, lastname, login, department, rg, room, phone, ticketid, ticketnumber) VALUES ('$cpf_p','$firstname_p','$lastname_p','$login_p','$department_p','$rg_p','$room_p','$phone_p','$ticketid_p', '$ticketnumber_p')";
	// use exec() because no results are returned
	$conn->exec($sql);
	echo "New record created successfully";
    }
catch(PDOException $e)
    {
   	 echo $sql . "<br>" . $e->getMessage();
    }

$conn = null;
?>

