<?php

declare(strict_types=1);

require_once __DIR__ . '/store.php';

/**
 * @param array<string, mixed> $db
 * @return array<string, mixed>|null
 */
function svc_find_user(array $db, string $username): ?array
{
    foreach ($db['users'] as $u) {
        if ($u['username'] === $username) {
            return $u;
        }
    }
    return null;
}

/**
 * @param array<string, mixed> $prefs
 * @param array<string, mixed> $user
 */
function svc_prefs_match_user(array $prefs, array $user): bool
{
    $age = (int) $user['age'];
    if ($age > (int) $prefs['age_max'] || $age < (int) $prefs['age_min']) {
        return false;
    }
    $g = $prefs['gender'];
    $ug = $user['gender'];
    if ($ug === 'female' && !empty($g['female'])) {
        return true;
    }
    if ($ug === 'male' && !empty($g['male'])) {
        return true;
    }
    if ($ug === 'nonbinary' && !empty($g['nonbinary'])) {
        return true;
    }
    return false;
}

/**
 * @param array<string, mixed> $db
 */
function svc_is_eligible_for_feed(array $db, array $user, string $currentUsername): bool
{
    if ($user['username'] === $currentUsername) {
        return false;
    }
    $me = svc_find_user($db, $currentUsername);
    if ($me === null) {
        return false;
    }
    if (in_array($user['username'], $me['seen_users'] ?? [], true)) {
        return false;
    }
    foreach ($db['likes'] as $like) {
        if ($like['liked'] === $user['username']) {
            return false;
        }
    }
    foreach ($db['matches'] as $m) {
        $pair = [$m['user1'], $m['user2']];
        if (in_array($user['username'], $pair, true) && in_array($currentUsername, $pair, true)) {
            return false;
        }
    }
    return svc_prefs_match_user($me['preferences'], $user);
}

/**
 * Interest overlap score between current user and a candidate (feed ranking).
 */
function svc_score_user(array $current, array $candidate): float
{
    $score = 0.0;
    $a = $current['interests'] ?? [];
    $b = $candidate['interests'] ?? [];
    foreach ($a as $i1) {
        foreach ($b as $i2) {
            if ($i1 === $i2) {
                $score += 0.05;
            }
        }
    }
    return $score;
}

/**
 * @param array<string, mixed> $db
 * @return array<string, mixed>|null
 */
function svc_feed_next(array $db, string $currentUsername): ?array
{
    $valid = [];
    foreach ($db['users'] as $u) {
        if (svc_is_eligible_for_feed($db, $u, $currentUsername)) {
            $valid[] = $u;
        }
    }
    if ($valid === []) {
        return null;
    }
    $me = svc_find_user($db, $currentUsername);
    if ($me === null) {
        return null;
    }
    $maxUser = $valid[0];
    $maxScore = svc_score_user($me, $maxUser);
    foreach ($valid as $u) {
        $s = svc_score_user($me, $u);
        if ($s > $maxScore) {
            $maxScore = $s;
            $maxUser = $u;
        }
    }
    return $maxUser;
}

/**
 * @param array<string, mixed> $db
 * @return array<int, array<string, mixed>>
 */
function svc_get_users_who_liked_me(array $db, string $currentUsername): array
{
    $out = [];
    foreach ($db['likes'] as $like) {
        if ($like['liker'] !== $currentUsername && $like['liked'] === $currentUsername) {
            $u = svc_find_user($db, $like['liker']);
            if ($u !== null) {
                $out[] = $u;
            }
        }
    }
    return $out;
}

/**
 * @param array<string, mixed> $db
 * @return array<int, array<string, mixed>>
 */
function svc_get_match_users(array $db, string $currentUsername): array
{
    $out = [];
    foreach ($db['matches'] as $m) {
        if ($m['user1'] === $currentUsername) {
            $u = svc_find_user($db, $m['user2']);
            if ($u !== null) {
                $out[] = $u;
            }
        } elseif ($m['user2'] === $currentUsername) {
            $u = svc_find_user($db, $m['user1']);
            if ($u !== null) {
                $out[] = $u;
            }
        }
    }
    return $out;
}

/**
 * @param array<string, mixed> $db
 */
function svc_get_chat_between(array $db, string $a, string $b): ?array
{
    foreach ($db['chats'] as $chat) {
        $pair = [$chat['user1'], $chat['user2']];
        if (in_array($a, $pair, true) && in_array($b, $pair, true)) {
            return $chat;
        }
    }
    return null;
}

/**
 * @param array<string, mixed> $db
 * @return array<int, array<string, mixed>>
 */
function svc_get_match_chats(array $db, string $currentUsername): array
{
    $matches = svc_get_match_users($db, $currentUsername);
    $rows = [];
    foreach ($matches as $matchUser) {
        $chat = svc_get_chat_between($db, $currentUsername, $matchUser['username']);
        $last = null;
        if ($chat !== null && !empty($chat['messages'])) {
            $msgs = $chat['messages'];
            $last = $msgs[count($msgs) - 1];
        }
        $rows[] = [
            'user' => $matchUser,
            'last_message' => $last,
        ];
    }
    return $rows;
}

/**
 * @param array<string, mixed> $db
 * @return array{match: bool}
 */
function svc_react(array $db, string $currentUsername, string $targetUsername, string $type): array
{
    if ($type === 'nope' || $type === 'pass') {
        $me = svc_find_user($db, $currentUsername);
        if ($me === null) {
            return ['match' => false];
        }
        if (!in_array($targetUsername, $me['seen_users'] ?? [], true)) {
            $me['seen_users'][] = $targetUsername;
            svc_replace_user($db, $me);
            db_save($db);
        }
        return ['match' => false];
    }
    if ($type !== 'like') {
        return ['match' => false];
    }
    foreach ($db['likes'] as $idx => $like) {
        if ($like['liked'] === $currentUsername && $like['liker'] === $targetUsername) {
            unset($db['likes'][$idx]);
            $db['likes'] = array_values($db['likes']);
            $db['matches'][] = [
                'user1' => $currentUsername,
                'user2' => $targetUsername,
                'match_date' => '',
            ];
            $me = svc_find_user($db, $currentUsername);
            if ($me !== null && !in_array($targetUsername, $me['seen_users'] ?? [], true)) {
                $me['seen_users'][] = $targetUsername;
                svc_replace_user($db, $me);
            }
            db_save($db);
            return ['match' => true];
        }
    }
    $me = svc_find_user($db, $currentUsername);
    if ($me === null) {
        return ['match' => false];
    }
    if (!in_array($targetUsername, $me['seen_users'] ?? [], true)) {
        $me['seen_users'][] = $targetUsername;
    }
    svc_replace_user($db, $me);
    $db['likes'][] = [
        'liker' => $currentUsername,
        'liked' => $targetUsername,
        'timestamp' => '',
    ];
    db_save($db);
    return ['match' => false];
}

/**
 * @param array<string, mixed> $db
 * @param array<string, mixed> $user
 */
function svc_replace_user(array &$db, array $user): void
{
    foreach ($db['users'] as $i => $u) {
        if ($u['username'] === $user['username']) {
            $db['users'][$i] = $user;
            return;
        }
    }
}

/**
 * @param array<string, mixed> $db
 */
function svc_send_message(array $db, string $from, string $to, string $text): void
{
    $text = trim($text);
    if ($text === '') {
        return;
    }
    $msg = [
        'sender_id' => $from,
        'receiver_id' => $to,
        'timestamp' => gmdate('c'),
        'message' => $text,
    ];
    $chat = svc_get_chat_between($db, $from, $to);
    if ($chat !== null) {
        foreach ($db['chats'] as $i => $c) {
            if (($c['user1'] === $chat['user1'] && $c['user2'] === $chat['user2'])
                || ($c['user1'] === $chat['user2'] && $c['user2'] === $chat['user1'])) {
                $db['chats'][$i]['messages'][] = $msg;
                db_save($db);
                return;
            }
        }
    }
    $db['chats'][] = [
        'user1' => $from,
        'user2' => $to,
        'messages' => [$msg],
    ];
    db_save($db);
}
