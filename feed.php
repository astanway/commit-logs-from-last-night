<?php
    header("Content-Type: application/rss+xml; charset=ISO-8859-1");
 
    require('opendb.php');
    $feed_items = 20;

    $query = "SELECT * FROM new_commits ORDER BY date DESC LIMIT " . $feed_items;
    $result = mysql_query($query);
?>
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Commit Logs From Last Night</title>
        <link>http://www.commitlogsfromlastnight.com/</link>
        <description>because real hackers pivot two hours before their demo</description>
        <language>en-us</language>
        <copyright>Created by @abestanway</copyright>
 
    <?php while($row = mysql_fetch_array($result)){ ?>
        <item>
            <title><?php echo $row['username'] ?></title>
            <description><?php echo $row['message'] ?></description>
            <link><?php echo $row['commiturl'] ?></link>
            <pubDate><?php echo date("D, d M Y H:i:s O", strtotime($row['date'])) ?></pubDate>
        </item>
    <?php } ?>
 
    </channel>
</rss>