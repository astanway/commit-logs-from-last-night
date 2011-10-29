<!DOCTYPE html>
<html>
<head>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
  <link href='http://fonts.googleapis.com/css?family=Marvel:700italic' rel='stylesheet' type='text/css'>
  <style>
  html, body{
    height: 100%;
    width: 100%;
    padding: 0;
    margin: 0;
  }
  
  html, body, #header{
    min-width: 1160px;
  }
  
  #header{
    font-size: 80px;
    text-align: center;
    font-family: 'Georgia';
    margin: 0 auto;
    width: 100%;
    position: fixed;
    height: 160px;
    background: -webkit-gradient(linear, 0% 75%, 0% 100%, from(rgba(255,255,255,1)), to(rgba(255,255,255,0)));
    background: -moz-linear-gradient(-90deg, rgba(255,255,255,1) 70%, rgba(255,255,255,0));
  }
  
  .author{
    padding-left: 10px;
  }
  
  .author{
    font-family: Helvetica;
    color: gray;
    font-size: 13px;
  }
  
  .message{
    font-family: Courier;
    color: black;
    font-size: 18px;
  }
  
  img{
    vertical-align: middle;
  }
  
  #allPosts{
    width: 700px;
    margin: 0 auto;
    text-align: left;
    padding-top: 140px;
  }
  
  td{
    border-bottom: 1px solid rgba(0,0,0,.2);
  }
  #subheader{
    font-size: 12px;
    letter-spacing: 11px;
    font-family: helvetica;
    color: gray;
    padding-top: 5px;
  }
  #twitter{
    position: absolute;
    font-family: Helvetica, Arial, 'sans serif';
    font-size: 13px;
    line-height: 120%;
    width: 110px;
    top: 250px;
    color: gray;
    right: 109px;
    text-align: right;
  }

  #githubForm{
    position: absolute;
    font-family: Helvetica, Arial, 'sans serif';
    font-size: 15px;
    line-height: 120%;
    width: 130px;
    top: 155px;
    color: gray;
    right: 109px;
    text-align: right;
  }
  
  .field{
    height: 25px; width: 100%;
    font-size: 15px;
    border: 3px #b0bac9 solid;
    border-radius: 5px;
    color: #7385a0;
  }
  
  a{
    text-decoration: none;
    color: #4E688A;
  }

  a:hover{
    color: #5F87A7;
  }
  </style>
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
                <?php echo $row['commiter']?>  
        </td>
        <td valign="middle" class="message">
            <?php echo$row['message'];?>
        </td>
      </tr> 
  <?php } ?>
</table>
</body>
</html>