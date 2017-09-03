<?php

$url = 'http://api.probasketballapi.com/game';

$api_key = 'EtnsZl5rhNIQzTb6oY7gFd1UeuiVKHMv';

$query_string = 'api_key='.$api_key.'&game_id=21400001&get_extra=1';

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POSTFIELDS, $query_string);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$result = curl_exec($ch);

curl_close($ch);

echo $result;

?>
			