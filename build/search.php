<?php
    require 'dbconnect.php';

  if (isset($_GET['term'])) {
      #$query = $_REQUEST['query'];
         $key=$_GET['term'];
      $query = mysqli_query ($db, "SELECT * FROM mooches_table WHERE Name LIKE '%{$key}%'");
  	$array = array();
    while($row=mysqli_fetch_assoc($query))
 {
   $array[] = $row['Name'];

 }
 echo json_encode($array);
 mysqli_close($db);
}

if (isset($_GET['q'])) {
 //Get the search term from our "q" GET variable.
$q = isset($_GET['q']) ? trim($_GET['q']) : '';

//Array to hold results so that we can
//return them back to our Ajax function.
$query = mysqli_query ($db, "SELECT * FROM mooches_table WHERE Name LIKE '%{$q}%'");

while($row = mysqli_fetch_array($query)) {


    echo "<div class='content'>";
    echo "<div class='politican-card'>";
    echo "<div class='politician-f-info'>";
    echo '<img src="', '.' ,'/' ,'img/'   .$row['img']. '.JPG'.'"/>';
    echo "<div class='politician-profile-info col-5 col-sm-4'>";
    echo "<h1>".$row['Name']."</h1>";
      echo "<h2>".$row['Department']."</h2>";
      echo "<h2>".$row['Position']."</h2>";
      echo "</div>";
      echo '<div class="politician-profile-info col-3 col-sm-2 hired-left"> <h3> Hired: '.$row['DatesHired'].' </h3>';
          echo     '<h3> Left: '.$row['DatesLeft']. '</h3> </div>';
          echo '<div class="politician-profile-info col-3 col-sm-2"> <p class="days-trump">Days Under Trump: '.$row['TimesunderTrump'].'</p>';
            echo '<p> Days in Office: '.$row['TotalTimes']. '</p> </div>';



    echo  "</div>";
  echo "</div>";
  echo '<div class="badgescard"><span class="bio">'.$row['Notes'].'</span></div>';
        echo "<h3 class='mooches-title'>",'NUMBER OF MOOCHES' , ' '.$row['TimesMooches']. '!',"</h3>";
  }
#echo json_encode($row);
mysqli_close($db);

//Display the results in JSON format so that
//we can parse it with JavaScript.
#echo json_encode($results);
}
?>
