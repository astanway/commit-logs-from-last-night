<!DOCTYPE html>
<html>
<head>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
  <link href='http://fonts.googleapis.com/css?family=Marvel:700italic' rel='stylesheet' type='text/css'>
  <link href='styles.css' rel='stylesheet' type='text/css'>
</head>
<body>
  <div id="header">Commit Logs From Last Night
    <div id="subheader">because real hackers pivot two hours before their demo</div>
        <div id="twitter">a <a href="http://hackny.org">hackNY</a> hack by <a href="http://www.twitter.com/abestanway">@abestanway</a></div>
        <div id="githubForm">
          <form action="" method="post" >
            <?php if (isset($_POST['username'])){
              echo "Success!";
            } else {
              echo "Wanna be famous?";
            }?>
            
            <input type="text" class="field" name="username" placeholder="GitHub Username"></input>
            <input type="submit" value="Submit">
          </form>
        </div>
    </div>
  <table id="allPosts" cellspacing="0" cellpadding='15'>
  <?php require('opendb.php');
  if (isset($_POST['username'])){
    $username = filter_that_shit($_POST['username']);
    $repo_url = "https://api.github.com/users/" . $username;
    $repos = json_decode(file_get_contents($repo_url));
    if ($repos != NULL){ 
      $query = mysql_query("INSERT INTO users (username) VALUES ('$username')");
    }
  }
  $query = mysql_query("SELECT * FROM commits ORDER BY date DESC");
  while($row = mysql_fetch_array($query)){ ?>
      <tr class="post">
        <td>
          <img height="70px" src="<?php echo$row['url'];?>"/>
        </td>
        <td valign="middle" class="author">
                <?php echo '<a href='. $row['userurl'] . '>' . $row['commiter'] .'</a>'?>  
        </td>
        <td valign="middle" class="message">
            <?php echo$row['message'];?>
        </td>
      </tr> 
  <?php } ?>
</table>
</body>
</html>