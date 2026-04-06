<?php

/**
 * JSON HTTP API for the dating SPA. Dispatches on `action` query parameter and request method.
 *
 * Session holds the current user (`$_SESSION['username']`). Invalid or missing session falls back
 * to `default_username` from the database.
 */

declare(strict_types=1);

session_start();

require_once __DIR__ . '/lib/store.php';
require_once __DIR__ . '/lib/pictures.php';
require_once __DIR__ . '/lib/service.php';

header('Content-Type: application/json; charset=utf-8');

/**
 * Emit JSON and terminate the request.
 *
 * @param array<string, mixed>|list<mixed> $data
 */
function api_json(int $code, $data): void
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

/**
 * Parse the request body as JSON. Returns an empty array if the body is empty.
 * On invalid JSON, responds with 400 and exits (does not return).
 *
 * @return array<string, mixed>
 */
function api_read_json_body(): array
{
    $raw = file_get_contents('php://input');
    if ($raw === false || $raw === '') {
        return [];
    }
    try {
        $j = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        return is_array($j) ? $j : [];
    } catch (Throwable $e) {
        api_json(400, ['error' => 'invalid JSON']);
    }
}

/**
 * Shape a raw user row for JSON responses: resolve interest IDs to objects, add picture URLs.
 *
 * @param array<string, mixed> $db
 * @param array<string, mixed> $user
 * @param bool $includePrefs When true, include `preferences` in the output (e.g. session / profile).
 * @return array<string, mixed>
 */
function api_expand_user(array $db, array $user, bool $includePrefs): array
{
    $ids = $user['interests'] ?? [];
    $master = $db['interests'] ?? [];
    $map = [];
    foreach ($master as $x) {
        $map[$x['id']] = $x;
    }
    $interestObjs = [];
    foreach ($ids as $id) {
        if (isset($map[$id])) {
            $interestObjs[] = $map[$id];
        }
    }
    $out = [
        'username' => $user['username'],
        'name' => $user['name'],
        'age' => $user['age'],
        'gender' => $user['gender'],
        'location' => $user['location'],
        'bio' => $user['bio'],
        'interests' => $interestObjs,
        'picture_urls' => pic_urls_for($user['username'], $user['pictures'] ?? []),
    ];
    if ($includePrefs) {
        $out['preferences'] = $user['preferences'];
    }
    return $out;
}

$action = $_GET['action'] ?? '';
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

try {
    $db = db_load();
} catch (Throwable $e) {
    api_json(500, ['error' => 'database error']);
}

if (!isset($_SESSION['username']) || svc_find_user($db, (string) $_SESSION['username']) === null) {
    $_SESSION['username'] = $db['default_username'];
}

$meName = (string) $_SESSION['username'];

if ($action === 'session' && $method === 'GET') {
    $me = svc_find_user($db, $meName);
    if ($me === null) {
        api_json(500, ['error' => 'session user missing']);
    }
    api_json(200, [
        'username' => $meName,
        'user' => api_expand_user($db, $me, true),
    ]);
}

if ($action === 'session' && $method === 'POST') {
    $body = api_read_json_body();
    $id = $body['username'] ?? $body['id'] ?? null;
    if ($id === null || !is_string($id)) {
        api_json(400, ['error' => 'expected username or id']);
    }
    if (svc_find_user($db, $id) === null) {
        api_json(404, ['error' => 'unknown user']);
    }
    $_SESSION['username'] = $id;
    api_json(200, ['ok' => true, 'username' => $id]);
}

if ($action === 'feed' && $method === 'GET') {
    $db = db_load();
    $next = svc_feed_next($db, $meName);
    if ($next === null) {
        api_json(200, ['user' => null]);
    }
    api_json(200, ['user' => api_expand_user($db, $next, false)]);
}

if ($action === 'feed_react' && $method === 'POST') {
    $body = api_read_json_body();
    $target = $body['username'] ?? null;
    $type = $body['type'] ?? '';
    if ($target === null || !is_string($target)) {
        api_json(400, ['error' => 'expected username']);
    }
    if (!is_string($type)) {
        api_json(400, ['error' => 'expected type']);
    }
    $db = db_load();
    if (svc_find_user($db, $target) === null) {
        api_json(404, ['error' => 'unknown user']);
    }
    $result = svc_react($db, $meName, $target, $type);
    api_json(200, $result);
}

if ($action === 'likes' && $method === 'GET') {
    $db = db_load();
    $list = svc_get_users_who_liked_me($db, $meName);
    $out = [];
    foreach ($list as $u) {
        $out[] = api_expand_user($db, $u, false);
    }
    api_json(200, ['users' => $out]);
}

if ($action === 'matches' && $method === 'GET') {
    $db = db_load();
    $list = svc_get_match_users($db, $meName);
    $out = [];
    foreach ($list as $u) {
        $out[] = api_expand_user($db, $u, false);
    }
    api_json(200, ['users' => $out]);
}

if ($action === 'user' && $method === 'GET') {
    $uname = $_GET['username'] ?? '';
    if ($uname === '') {
        api_json(400, ['error' => 'missing username']);
    }
    $db = db_load();
    $u = svc_find_user($db, $uname);
    if ($u === null) {
        api_json(404, ['error' => 'not found']);
    }
    api_json(200, ['user' => api_expand_user($db, $u, false)]);
}

if ($action === 'preferences' && $method === 'GET') {
    $db = db_load();
    $me = svc_find_user($db, $meName);
    if ($me === null) {
        api_json(500, ['error' => 'session user missing']);
    }
    api_json(200, ['preferences' => $me['preferences']]);
}

if ($action === 'preferences' && $method === 'POST') {
    $body = api_read_json_body();
    $p = $body['preferences'] ?? $body;
    if (!isset($p['gender'], $p['age_min'], $p['age_max'], $p['distance_meters'])) {
        api_json(400, ['error' => 'invalid preferences']);
    }
    $db = db_load();
    $me = svc_find_user($db, $meName);
    if ($me === null) {
        api_json(500, ['error' => 'session user missing']);
    }
    $me['preferences'] = [
        'gender' => [
            'male' => !empty($p['gender']['male']),
            'female' => !empty($p['gender']['female']),
            'nonbinary' => !empty($p['gender']['nonbinary']),
        ],
        'age_min' => (int) $p['age_min'],
        'age_max' => (int) $p['age_max'],
        'distance_meters' => (int) $p['distance_meters'],
    ];
    svc_replace_user($db, $me);
    db_save($db);
    api_json(200, ['ok' => true, 'preferences' => $me['preferences']]);
}

if ($action === 'interests' && $method === 'GET') {
    api_json(200, ['interests' => $db['interests'] ?? []]);
}

if ($action === 'chats' && $method === 'GET') {
    $db = db_load();
    $rows = svc_get_match_chats($db, $meName);
    $out = [];
    foreach ($rows as $row) {
        $u = $row['user'];
        $last = $row['last_message'];
        $out[] = [
            'user' => api_expand_user($db, $u, false),
            'last_message' => $last,
        ];
    }
    api_json(200, ['chats' => $out]);
}

if ($action === 'chat_messages' && $method === 'GET') {
    $with = $_GET['with'] ?? '';
    if ($with === '') {
        api_json(400, ['error' => 'missing with']);
    }
    $db = db_load();
    $matches = svc_get_match_users($db, $meName);
    $ok = false;
    foreach ($matches as $m) {
        if ($m['username'] === $with) {
            $ok = true;
            break;
        }
    }
    if (!$ok) {
        api_json(403, ['error' => 'not a match']);
    }
    $chat = svc_get_chat_between($db, $meName, $with);
    $messages = $chat['messages'] ?? [];
    api_json(200, ['messages' => $messages]);
}

if ($action === 'chat_send' && $method === 'POST') {
    $with = $_GET['with'] ?? '';
    if ($with === '') {
        api_json(400, ['error' => 'missing with']);
    }
    $body = api_read_json_body();
    $text = $body['message'] ?? '';
    if (!is_string($text)) {
        api_json(400, ['error' => 'expected message string']);
    }
    $db = db_load();
    $matches = svc_get_match_users($db, $meName);
    $ok = false;
    foreach ($matches as $m) {
        if ($m['username'] === $with) {
            $ok = true;
            break;
        }
    }
    if (!$ok) {
        api_json(403, ['error' => 'not a match']);
    }
    svc_send_message($db, $meName, $with, $text);
    api_json(200, ['ok' => true]);
}

if ($action === 'users' && $method === 'GET') {
    $db = db_load();
    $out = [];
    foreach ($db['users'] as $u) {
        if ($u['username'] === $meName) {
            continue;
        }
        $out[] = api_expand_user($db, $u, false);
    }
    api_json(200, ['users' => $out]);
}

if ($action === 'admin_clear' && $method === 'POST') {
    $body = api_read_json_body();
    $what = $body['what'] ?? '';
    $scope = $body['scope'] ?? '';
    if (!is_string($what) || !is_string($scope)) {
        api_json(400, ['error' => 'expected what and scope strings']);
    }
    if (!in_array($what, ['likes', 'matches', 'messages'], true)) {
        api_json(400, ['error' => 'what must be likes, matches, or messages']);
    }
    if (!in_array($scope, ['me', 'all'], true)) {
        api_json(400, ['error' => 'scope must be me or all']);
    }
    $db = db_load();
    svc_admin_clear($db, $meName, $what, $scope);
    db_save($db);
    api_json(200, ['ok' => true]);
}

api_json(404, ['error' => 'unknown action']);
