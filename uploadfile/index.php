<?php

include_once 'ConexionAPI.inc.php';


$file_path = $argv[1];
$file_name = $argv[2];

$item_id = $argv[3];


$resp = PodioFile::upload($file_path, $file_name);

$file_id = $resp->file_id;
$file_load = PodioFile::attach($file_id, array('ref_type' => 'item', 'ref_id' => (int)$item_id));

// echo print_r($resp -> file_id);
echo print_r($file_load);

//var_dump($argv)
?>