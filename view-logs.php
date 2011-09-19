<html>
<head>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
</head>
<body>
  <?php
  require("opendb.php");
  // error_reporting(E_ERROR | E_PARSE);
  $users = "https://github.com/api/v2/json/repos/search/ios";
  $users = json_decode(file_get_contents($users));
  $rBROsitories = $users->repositories;
  foreach($rBROsitories as $key=>$reBRO){
    var_dump($reBRO);
    $username = $reBRO->username;
    if(!$username) header("Location: index.php");
    $repo_url = "https://api.github.com/users/" . $username . "/repos";
    $repos = json_decode(file_get_contents($repo_url));
    $messages = array();
    foreach($repos as $key => $repo) {
      $name = $repo->name;
      $commit_url = "https://api.github.com/repos/" . $username . "/" . $name . "/commits";
      $commits = json_decode(file_get_contents($commit_url));
      foreach($commits as $key => $commit) {
        $message = $commit->commit->message;
        $profanity_url = "http://www.wdyl.com/profanity?q=" . urlencode($message);
        $profanity = json_decode(file_get_contents($profanity_url));

        if(strstr($message, 'README')){
          continue;
        }
        
        $realMessage = $message;
        $pct = count_capitals($message) / strlen(urlencode($message));
        if($profanity->response == 'true') {
          $login = $commit->author->login;
          $avatar = $commit->author->avatar_url;
          $query = "INSERT INTO commits VALUES ('', '$login', '$message', '$avatar')";
          $query = mysql_query($query);
          echo mysql_error($connection);
        } 
      }
    }
  }
  
  function count_capitals($s) {
    return strlen(preg_replace('![^A-Z]+!', '', $s));
  }
  
  function detect_duplicates($s){
    return preg_match('aaa|bbb|ccc|ddd|eee|fff|ggg|hhh|iii|jjj|kkk|lll|mmm|nnn|ooo|ppp|qqq|rrr|sss|ttt|uuu|vvv|www|xxx|yyy|zzz', '', $s);
  }
  ?>
</body>
</html>