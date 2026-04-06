<?php

declare(strict_types=1);

/**
 * Absolute path to the JSON database file.
 */
function db_path(): string
{
    return dirname(__DIR__, 2) . DIRECTORY_SEPARATOR . 'data' . DIRECTORY_SEPARATOR . 'database.json';
}

/**
 * Read and decode the database with a shared lock. Exits with 500 JSON on missing file or read error.
 *
 * @return array<string, mixed>
 */
function db_load(): array
{
    $path = db_path();
    if (!is_readable($path)) {
        http_response_code(500);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['error' => 'database not found']);
        exit;
    }
    $fh = fopen($path, 'rb');
    if ($fh === false) {
        http_response_code(500);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['error' => 'cannot read database']);
        exit;
    }
    flock($fh, LOCK_SH);
    $json = stream_get_contents($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
    $data = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
    return $data;
}

/**
 * Atomically rewrite the database file with an exclusive lock.
 *
 * @param array<string, mixed> $data
 */
function db_save(array $data): void
{
    $path = db_path();
    $fh = fopen($path, 'c+b');
    if ($fh === false) {
        http_response_code(500);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['error' => 'cannot write database']);
        exit;
    }
    flock($fh, LOCK_EX);
    ftruncate($fh, 0);
    rewind($fh);
    $out = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    fwrite($fh, $out);
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
}
