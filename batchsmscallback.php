<?php

// DR - https://docs.nexmo.com/messaging/sms-api/api-reference#delivery_receipt
// ?msisdn=66837000111&to=12150000025&network-code=52099&messageId=000000FFFB0356D2&price=0.02000000&status=delivered&scts=1208121359&err-code=0&message-timestamp=2012-08-12+13%3A59%3A37

$time_stamp = date('d-m-Y H:i:s');
echo($time_stamp);


$fp = fopen('batchsms.txt','a');
$fp_log = fopen('batchsms.log','a');

// work with get or post
$request = array_merge($_GET, $_POST);

// Check that this is a delivery receipt.
if (!isset($request['msisdn']) OR !isset($request['to'])) {
    fwrite( $fp_log,$time_stamp . ": This is not a delivery receipt");
    return;
} else {
fwrite( $fp,"{$request['to']};{$request['network-code']};{$request['messageId']};{$request['msisdn']};{$request['status']};{$request['err-code']};{$request['price']};{$request['scts']};{$request['message-timestamp']};{$request['client-ref']}'". "\n" );
}

fclose($fp);
fclose($fp_log);
?>
