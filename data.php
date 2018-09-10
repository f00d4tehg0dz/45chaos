<?php

// For Data from Mooches Calculator

if (isset($_POST['df']))
	{
	$start = strtotime($_POST['df']);
	$end = time();
	$diff = $end - $start;
	echo '<h3 class="mooches-title">' . ' That was ' . floor($diff / (60 * 60 * 24) / 10) . ' Mooches ago!' . '</h3>'; //Calulate Time then Divide by 10
	}

require 'dbconnect.php';

// storing  request (ie, get/post) global array to a variable

$requestData = $_REQUEST;
$columns = array(

	// datatable column index  => database column name

	0 => 'img',
	1 => 'Name',
	2 => 'Department',
	3 => 'Position',
	4 => 'DatesHired',
	5 => 'DatesLeft',
	6 => 'TotalTimes',
	7 => 'TimesunderTrump',
	8 => 'TimesMooches',
	9 => 'FiredResign',
	10 => 'Notes',
);

// getting total number records without any search

$sql = "SELECT img, Name, Department, Position, DatesHired, DatesLeft, TotalTimes, TimesunderTrump, TimesMooches, FiredResign, Notes ";
$sql.= " FROM mooches_table";
$query = mysqli_query($db, $sql) or die("data.php: get departures");
$totalData = mysqli_num_rows($query);
$totalFiltered = $totalData; // when there is no search parameter then total number rows = total number filtered rows.
$sql = "SELECT img, Name, Department, Position, DatesHired, DatesLeft, TotalTimes, TimesunderTrump, TimesMooches, FiredResign, Notes";
$sql.= " FROM mooches_table WHERE 1=1";

if (!empty($requestData['search']['value']))
	{ // if there is a search parameter, $requestData['search']['value'] contains search parameter
	$sql.= " AND ( img LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR Name LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR Department LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR Position LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR DatesHired LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR DatesLeft LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR TotalTimes LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR TimesunderTrump LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR TimesMooches LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR FiredResign LIKE '" . $requestData['search']['value'] . "%' ";
	$sql.= " OR Notes LIKE '" . $requestData['search']['value'] . "%' )";
	}

$query = mysqli_query($db, $sql) or die("data.php: get departures");
$totalFiltered = mysqli_num_rows($query); // when there is a search parameter then we have to modify total number filtered rows as per search result.
$sql.= " ORDER BY " . $columns[$requestData['order'][0]['column']] . "   " . $requestData['order'][0]['dir'] . "   LIMIT " . $requestData['start'] . " ," . $requestData['length'] . "   ";
/* $requestData['order'][0]['column'] contains colmun index, $requestData['order'][0]['dir'] contains order such as asc/desc , $requestData['start'] contains start row number ,$requestData['length'] contains limit length. */
$query = mysqli_query($db, $sql) or die("data.php: get departures");
$data = array();

while ($row = mysqli_fetch_array($query))
	{ // preparing an array
	$nestedData = array();
	$nestedData[] = $row["img"];
	$nestedData[] = $row["Name"];
	$nestedData[] = $row["Department"];
	$nestedData[] = $row["Position"];
	$nestedData[] = $row["DatesHired"];
	$nestedData[] = $row["DatesLeft"];
	$nestedData[] = $row["TotalTimes"];
	$nestedData[] = $row["TimesunderTrump"];
	$nestedData[] = $row["TimesMooches"];
	$nestedData[] = $row["FiredResign"];
	$nestedData[] = $row["Notes"];
	$data[] = $nestedData;
	}

$json_data = array(
	"draw" => intval($requestData['draw']) , // for every request/draw by clientside , they send a number as a parameter, when they recieve a response/data they first check the draw number, so we are sending same number in draw.
	"recordsTotal" => intval($totalData) , // total number of records
	"recordsFiltered" => intval($totalFiltered) , // total number of records after searching, if there is no searching then totalFiltered = totalData
	"data" => $data

	// total data array

);
echo json_encode($json_data); // send data as json format
