<!DOCTYPE html>
<html>
<head>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
  <link href='http://fonts.googleapis.com/css?family=Marvel:700italic' rel='stylesheet' type='text/css'>
  <style>
  html, body{
    height: 100%;
    width: 100%;
    overflow-x: hidden;
    padding: 0;
    margin: 0;
  }
  
  body{
    width: 98%;
  }
  
  #header{
    font-size: 80px;
    text-align: center;
    font-family: 'Georgia';
    margin: 0 auto;
    width: 100%;
    position: absolute;
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
  </style>
</head>
<body>
  <div id="header">Commit Logs From Last Night
    <div id="subheader">because real hackers pivot two hours before their demo</div>
    </div>
  <table id="allPosts" cellspacing="0" cellpadding='15'>
  <?php require('opendb.php');
  $query = mysql_query("SELECT * FROM commits ORDER BY id");
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