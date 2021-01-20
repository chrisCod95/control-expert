<?php
require_once 'PodioLibraries/PodioAPI.php';
$client_id = 'control-expert';
$client_secret = 'c1Gk3EkXvHiYKmsvqiMsIoYDwKEfoabwgrxouASMojU0sesscxQKfJZegZ1Fl4dm';

$app_id = '25060003';
$app_token = 'a1bc3002c84a464a9a883245eb2482d6';

Podio::setup($client_id, $client_secret);
Podio::authenticate_with_app($app_id, $app_token);


