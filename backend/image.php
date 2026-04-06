<?php

declare(strict_types=1);

require_once __DIR__ . '/lib/pictures.php';

$shared = $_GET['shared'] ?? '';
$u = $_GET['u'] ?? '';
$f = $_GET['f'] ?? '';

$path = null;
if ($shared !== '') {
    $path = pic_fs_shared($shared);
} elseif ($u !== '' && $f !== '') {
    $path = pic_fs_path($u, $f);
}

if ($path === null) {
    http_response_code(404);
    header('Content-Type: text/plain; charset=utf-8');
    echo 'Not found';
    exit;
}

$mime = null;
if (function_exists('finfo_open')) {
    $fi = finfo_open(FILEINFO_MIME_TYPE);
    if ($fi !== false) {
        $mime = finfo_file($fi, $path) ?: null;
        finfo_close($fi);
    }
}
if ($mime === null || $mime === 'application/octet-stream') {
    $ext = strtolower(pathinfo($path, PATHINFO_EXTENSION));
    $types = [
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'gif' => 'image/gif',
        'webp' => 'image/webp',
    ];
    $mime = $types[$ext] ?? 'application/octet-stream';
}

header('Content-Type: ' . $mime);
header('Cache-Control: public, max-age=86400');
readfile($path);
