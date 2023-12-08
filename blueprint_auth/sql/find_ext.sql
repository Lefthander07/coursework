SELECT id, cgroup, login, password
FROM external
WHERE 1=1
    AND login='$login' AND password = $password