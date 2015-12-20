<?php
require('opendb.php');
$per_page = 50;

function get_num_pages($per_page){
	$query = "SELECT COUNT(*) FROM new_commits ORDER BY id DESC";
	$result = mysql_query($query);
	$result_array = mysql_fetch_array($result);
	$num_messages = $result_array[0];
	return round($num_messages / $per_page);
}

$num_pages = get_num_pages($per_page);

$page = 0;
if(is_numeric($_GET['page'])){
	$page = $_GET['page'];
} 

// Get commits
$query = "SELECT * FROM new_commits ORDER BY date DESC LIMIT " . $page * $per_page . ", " . $per_page;
$result = mysql_query($query);

$prev_page = $page - 1;
$next_page = $page + 1;
if($prev_page < 0){
	$prev_page = false;
}
if($next_page > $num_pages){
	$next_page = false;
}

?>
<!DOCTYPE html>
<html>
<head>
  <title>Commit Logs From Last Night</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
  <link href='http://fonts.googleapis.com/css?family=Marvel:700italic' rel='stylesheet' type='text/css'>
  <link href='css/styles.css' rel='stylesheet' type='text/css'>
  <link rel="icon" href="favicon.ico" type="image/x-icon" />
  <script type="text/javascript" src="js/jquery.infinitescroll.min.js"></script>
  <script type="text/javascript">
    $(document).ready(function(){
      $('#allPosts').infinitescroll({
        navSelector  : "div.pagination",            
                     // selector for the paged navigation (it will be hidden)
        nextSelector : "div.pagination a:first",    
                     // selector for the NEXT link (to page 2)
        itemSelector : "#allPosts tr.post"          
                     // selector for all items you'll retrieve
    });
  });
  </script>
</head>
<body>
<!--<a href="https://github.com/astanway/Commit-Logs-From-Last-Night"><img style="position: fixed; top: 0; left: 0; border: 0; z-index:10;" src="forkme_light_background.png" alt="Fuckin' fork me!"></a>-->
  <div id="header">Commit Logs From Last Night
    <div id="subheader">because real hackers pivot two hours before their demo</div>
        <div id="twitter">This thing tweets at <a href="http://www.twitter.com/CLFLN">@CLFLN</a>
<br><br>
Created by <a href="http://www.twitter.com/abestanway">@abestanway</a>
</br></br>
Watch the <a href="http://bit.ly/19XjyNb">video</a>!
<br><br>
<a href="http://hired.com/?utm_source=partner&utm_medium=abes"><img src="hired.png"></a>
</div>
   </div>

  <table class="allPostsClass" id="allPosts" cellspacing="0" cellpadding='15'>
    <tbody>
  <?php
  while($row = mysql_fetch_array($result)){ 
    if (strlen($row['message']) > 70) continue;
  ?>
      <tr class="post">
        <td>
        <?php echo '<a class="avatarlink" href='. $row['userurl'] . '>'?>
          <img class="avatar" height="70px" src="<?php echo$row['url'];?>"/>
          </a>
        </td>
        <td valign="middle" class="author">
                <?php echo '<div class="commiter">' . $row['commiter'] . " </div><br>" ;?> 
                <?php $datetime = strtotime($row['date']);
                      $mysqldate = date("m/d/y g:i A", $datetime);
                      echo "<span class='date'>". $mysqldate . "</span>";
                 ?>
        </td>
        <td valign="middle" class="message">

          <div class="subMessage">
                <?php echo '<a class="commit" target="_blank" href='. $row['commiturl'] . ' > ' . $row['message'] .'</a>'?>  
          </div>
        </td>
      </tr> 
  <?php } ?>
  </tbody>
</table>
<div class="pagination" style="display:none;">
  <?php
	if($next_page){
		echo '<a class="first" href="?page=' . $next_page . '"> Next</a>';
	}
	?>
</div>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-49063518-1', 'commitlogsfromlastnight.com');
  ga('send', 'pageview');

</script>

<!-- Google Code for Remarketing Tag -->
<!--------------------------------------------------
Remarketing tags may not be associated with personally identifiable information or placed on pages related to sensitive categories. See more information and instructions on how to setup the tag on: http://google.com/ads/remarketingsetup
--------------------------------------------------->
<script type="text/javascript">
/* <![CDATA[ */
var google_conversion_id = 1000219892;
var google_custom_params = window.google_tag_params;
var google_remarketing_only = true;
/* ]]> */
</script>
<script type="text/javascript" src="//www.googleadservices.com/pagead/conversion.js">
</script>
<noscript>
<div style="display:inline;">
<img height="1" width="1" style="border-style:none;" alt="" src="//googleads.g.doubleclick.net/pagead/viewthroughconversion/1000219892/?value=0&amp;guid=ON&amp;script=0"/>
</div>
</noscript>

</body>
</html>
