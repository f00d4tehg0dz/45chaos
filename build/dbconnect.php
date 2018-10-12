<?php
//--------------------------------------------------------------------------
// Call DB
//--------------------------------------------------------------------------
$host = "127.0.0.1";
$user = "root";
$pass = "";
$dbName = 'mooches';

//Create connection and select DB
$db = new mysqli($host, $user, $pass, $dbName);

if ($db->connect_error) {
    die("Unable to connect database: " . $db->connect_error);
}
