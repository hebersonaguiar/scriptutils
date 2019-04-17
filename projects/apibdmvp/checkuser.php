<?php
header('Content-type: application/json');
header("Access-Control-Allow-Origin: *");

$servername = "mysql";
$username = "root";
$password = "my-secret-pw";
$dbname = "appmvp";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	}

	$login_p = $_POST['login_p'];

	$sql = 'SELECT * FROM items WHERE login ="'. $login_p . '"';
	
	$result = $conn->query($sql);
	$response = array();

	if ($result->num_rows > 0) {
	    while($row = $result->fetch_assoc()) {
	        $response['cpf'] = $row["cpf"];
	        $response['login'] = $row["login"];
	        $response['firstname'] = $row["firstname"];
	        $response['lastname'] = $row["lastname"];
	        $response['department'] = $row["department"];
	        $response['rg'] = $row["rg"];
	        $response['room'] = $row["room"];
	        $response['phone'] = $row["phone"];
	        $response['ticketid'] = $row["ticketid"];
	        $response['ticketnumber'] = $row["ticketnumber"];
    	}
    echo json_encode($response);
    } else {
	    echo "0";
	}

$conn->close(); 
?>

