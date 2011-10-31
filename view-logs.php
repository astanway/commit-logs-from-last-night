<?php
  require("opendb.php");

  $query = mysql_query("SELECT * FROM users ORDER BY id");
  $usernames = array();
  
  while($row = mysql_fetch_array($query)){ 
     array_push($usernames, $row[1]);
  }
  
  mysql_close($connection);

  $repos = array('ios', 'php', 'java', 'ruby', 'python', 'c', 'scala', 'javascript');
  
  foreach($repos as $repo){
    $users = "https://github.com/api/v2/json/repos/search/" . $repo;
    $users = json_decode(file_get_contents($users));
    $rBROsitories = $users->repositories;
    foreach($rBROsitories as $key=>$reBRO){
      $username = $reBRO->username;
      array_push($usernames, $username);
    }
  }
  
  //an attempt to get all the data over time despite github's rate limiting.
  shuffle($usernames);
  
  foreach($usernames as $username){
    process($username, $db_ip, $db_user, $db_pass, $db_name);
  }

function process($username, $db_ip, $db_user, $db_pass, $db_name){
  $repo_url = "https://api.github.com/users/" . $username . "/repos";
  $repos = json_decode(file_get_contents($repo_url));
  $messages = array();
  foreach($repos as $key => $repo) {
   $name = $repo->name;
   $commit_url = "https://api.github.com/repos/" . $username . "/" . $name . "/commits";
   $commits = json_decode(file_get_contents($commit_url));
   foreach($commits as $key => $commit) {
     try{
       $message = $commit->commit->message;  
     } catch (Exception $e){
       continue;
     }
     $profanity_url = "http://www.wdyl.com/profanity?q=" . urlencode($message);
     $profanity = json_decode(file_get_contents($profanity_url));
   
       if($profanity->response == 'true') {
       $login = $commit->committer->login;
       $avatar = $commit->committer->avatar_url;
       $userurl = $commit->committer->url;
       $userurl = str_replace('api.','', $userurl);
       $userurl = str_replace('users/', '', $userurl);
       $date = $commit->commit->committer->date;
       $commiturl = $commit->commit->url;
       $commiturl = str_replace('api.','',$commiturl);
       $commiturl = str_replace('repos/','',$commiturl);
       $commiturl = str_replace('git/commits','commit',$commiturl);

          //hook it up
         $connection = mysql_connect($db_ip, $db_user, $db_pass);
         mysql_select_db($db_name) or die ('Unable to select database!');
         $message = filter_that_shit($message);
         $insert = "INSERT INTO new_commits VALUES ('', '$login', '$message', '$avatar', '$commiturl', '$userurl', '$date', now())";
         $insert = mysql_query($insert);             
         mysql_close($connection);
     } 
   }
  }  
}
?>