SELECT id, cgroup, login, password
FROM internal
WHERE 1=1
    AND login='$login' AND password = '$password'