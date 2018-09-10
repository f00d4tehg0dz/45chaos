<?php
$start  = strtotime('1985-02-16');
$end    = time(); // Waktu sekarang
$diff   = $end - $start;
echo 'Your age is ' . floor($diff / (60 * 60 * 24 * 365)) . ' years'; // Your age is 28 years
echo 'Your age is ' . floor($diff / (60 * 60 * 24) / 10) . ' days'; // Your age is 10400 days
?>
