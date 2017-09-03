<?php

$url = 'https://probasketballapi.com/draftkings/players';

$api_key = 'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv';

$query_string = 'api_key='.$api_key.'&first_name=LeBron&last_name=James';

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POSTFIELDS, $query_string);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$result = curl_exec($ch);

curl_close($ch);

echo $result;

$result=json_decode($result);

$db = $dkplayers;
$collection = $dkplayers->Collection;
$collection->insert($result)


?>