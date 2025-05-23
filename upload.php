<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$data = json_decode(file_get_contents('php://input'), true);

if (!$data || !isset($data['image'])) {
    http_response_code(400);
    echo "No image data received";
    exit;
}

$imageData = $data['image'];
$imageData = str_replace('data:image/png;base64,', '', $imageData);
$imageData = str_replace(' ', '+', $imageData);
$decodedImage = base64_decode($imageData);

if ($decodedImage === false) {
    http_response_code(400);
    echo "Base64 decode failed";
    exit;
}

$dir = __DIR__ . '/img';

if (!is_dir($dir)) {
    if (!mkdir($dir, 0777, true)) {
        http_response_code(500);
        echo "Failed to create directory";
        exit;
    }
}

$fileName = $dir . '/' . time() . '_' . bin2hex(random_bytes(4)) . '.png';

if (file_put_contents($fileName, $decodedImage) === false) {
    http_response_code(500);
    echo "Failed to save image";
    exit;
}

http_response_code(200);
echo "Image saved successfully";
