<?php
// For Data from Mooches Calculator
if (isset($_POST['df'])) {

$start = strtotime($_POST['df']);

$end    = time();
$diff   = $end - $start;

echo '<h3 class="mooches-title">' . ' That was ' . floor($diff / (60 * 60 * 24) / 10) . ' Mooches ago!'. '</h3>'; //Calulate Time then Divide by 10
}
// For Data coming for Timeline
if (!empty($_POST['id'])) {
//Include DB configuration file
    require 'dbconnect.php';
    //Get last ID
    $lastID = $_POST['id'];

    //Limit on data display
    $showLimit =200;

    //Get all rows except already displayed
    $queryAll = $db->query("SELECT COUNT(*) as num_rows FROM mooches_table WHERE id < ".$lastID." ORDER BY id DESC");
    $rowAll = $queryAll->fetch_assoc();
    $allNumRows = $rowAll['num_rows'];
    $i=26;
    $c=26;
    //Get rows by limit except already displayed
    $query = $db->query("SELECT * FROM mooches_table WHERE id < ".$lastID." ORDER BY id DESC LIMIT ".$showLimit);

    if ($query->num_rows > 0) {
        while ($row = $query->fetch_assoc()) {
            $postID = $row["id"]; ?>
            <div class="row no-gutters f-table-row cards">

                <div class="col-sm-1 f-table-col">
                    <div class="firstinfo"><img src="', '.' ,'/' ,'img/'   .$row['img']. '.JPG'.'" width="80"/></div>
                  </div>
                    <div class="clearfix hidden-sm hidden-md hidden-lg"></div>
                    <div class="profileinfo col-sm-2 f-table-col">
                        <p class="name" data-title="Name"> <?php echo $row['Name']; ?> </p>
                    </div>
                    <div class="clearfix hidden-sm hidden-md hidden-lg"></div>
                    <div class="profileinfo col-sm-1 f-table-col">
                        <p class="department" data-title="Affliation"><?php echo $row['Department']; ?></p>
                    </div>
                    <div class="profileinfo col-sm-2 f-table-col">
                        <p class="bio" data-title="Position" ><?php echo $row['Position']; ?></p>
                    </div>

                    <div class="profileinfo col-sm-1 f-table-col">
                        <h4 data-title="Hired"><?php echo $row['DatesHired']; ?></h4>
                    </div>
                    <div class="clearfix hidden-sm hidden-md hidden-lg"></div>
                    <div class="profileinfo col-sm-1 f-table-col">
                          <h4  data-title="Left"><?php echo $row['DatesLeft']; ?></h4>
                    </div>
                    <div class="clearfix hidden-sm hidden-md hidden-lg"></div>
                    <div class="profileinfo  col-sm-1 f-table-col">
                        <h5 class="days-trump" data-title="Total Days"><?php echo $row['TotalTimes']; ?></h5>
                    </div>
                    <div class="profileinfo  col-sm-1 f-table-col">
                        <p class="days-trump"  data-title="Under Trump"><?php echo $row['TimesunderTrump']; ?></p>
                    </div>
                    <div class="profileinfo col-sm-1 f-table-col">
                      <div class="row">
                         <div class="col-md-12">
                              <p class="mooch" data-title="Mooches"><?php echo $row['TimesMooches']; ?></p>
                         </div>
                         </div>
                    </div>
                    <div class="profileinfo  col-sm-1 f-table-col">
                      <div class="row">
                         <div class="col-md-12">
                              <p class="resign" data-title="Fired/Resign"><?php echo $row['FiredResign']; ?></p>
                         </div>
                    </div>
                    </div>


               <button type="button" class="btn btn-info viewmore" data-toggle="collapse" data-target="#commentcard<?php echo $i++; ?>" <i class="fas fa-angle-double-down"></i>

               view notes</button>
            <div id="commentcard<?php echo $c++; ?>"  class="collapse" data-toggle="collapse">
                 <div class="commentcard">
                   <span><?php echo $row['Notes']; ?></span>
                 </div></div>
               </div><!--cards-->
<?php
        } ?>
<?php if ($allNumRows > $showLimit) {
            ?>
    <div class="load-more" lastID="<?php echo $postID; ?>" style="display: none;">
        <img src="img/loading.gif"/>
    </div>
<?php
        } else {
            ?>
    <div class="load-more" lastID="0">
        That's All!
    </div>
<?php
        }
    } else {
        ?>
    <div class="load-more" lastID="0">
        That's All!
    </div>
<?php
    }
}
