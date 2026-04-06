<?php

declare(strict_types=1);

/**
 * Build public image URLs for the SPA (relative to site root).
 *
 * @param list<string> $pictures
 * @return list<string>
 */
function pic_urls_for(string $username, array $pictures): array
{
    $urls = [];
    foreach ($pictures as $p) {
        if ($p === null || $p === '') {
            continue;
        }
        if (str_contains((string) $p, '/static/images/') || str_contains(strtolower((string) $p), 'avatar')) {
            $urls[] = 'backend/image.php?shared=' . rawurlencode('avatar.png');
        } else {
            $base = basename((string) $p);
            $urls[] = 'backend/image.php?u=' . rawurlencode($username) . '&f=' . rawurlencode($base);
        }
    }
    return $urls;
}

/**
 * Resolve filesystem path for an image (used by image.php).
 */
function pic_fs_path(string $username, string $filename): ?string
{
    $root = dirname(__DIR__, 2) . DIRECTORY_SEPARATOR . 'data' . DIRECTORY_SEPARATOR . 'images' . DIRECTORY_SEPARATOR;
    if (!preg_match('/^[a-zA-Z0-9_\\-]+$/', $username)) {
        return null;
    }
    $fn = basename($filename);
    if (!preg_match('/^[a-zA-Z0-9_.\\-]+$/', $fn)) {
        return null;
    }
    $path = $root . $username . DIRECTORY_SEPARATOR . $fn;
    if (is_readable($path)) {
        return $path;
    }
    return null;
}

/**
 * Resolve filesystem path for a file in the shared images root (`data/images/<name>`).
 */
function pic_fs_shared(string $name): ?string
{
    $root = dirname(__DIR__, 2) . DIRECTORY_SEPARATOR . 'data' . DIRECTORY_SEPARATOR . 'images' . DIRECTORY_SEPARATOR;
    $fn = basename($name);
    if (!preg_match('/^[a-zA-Z0-9_.\\-]+$/', $fn)) {
        return null;
    }
    $path = $root . $fn;
    if (is_readable($path)) {
        return $path;
    }
    return null;
}
