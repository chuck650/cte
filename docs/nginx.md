# nginx Web Server

## Installing

## Verifying the default server

Verify the nginx service is running.

```bash
$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2020-04-20 14:32:24 UTC; 10h ago
     Docs: man:nginx(8)
  Process: 13840 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
  Process: 13842 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
 Main PID: 13844 (nginx)
    Tasks: 3 (limit: 4915)
   Memory: 6.3M
   CGroup: /system.slice/nginx.service
           ├─13844 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
           ├─13845 nginx: worker process
           └─13846 nginx: worker process
```

Verify the nginx service is bound to port 80 on IPv4 addresses.

```bash
$ sudo ss -plnt | grep ':80'
LISTEN    0         128                0.0.0.0:80               0.0.0.0:*        users:(("nginx",pid=13846,fd=6),("nginx",pid=13845,fd=6),("nginx",pid=13844,fd=6))
```

Verify the http connection returns `HTTP/1.1 200 OK`.

```bash
$ curl -I localhost
HTTP/1.1 200 OK
Server: nginx/1.16.1 (Ubuntu)
Date: Tue, 21 Apr 2020 01:01:52 GMT
Content-Type: text/html
Content-Length: 612
Last-Modified: Mon, 13 Apr 2020 03:16:01 GMT
Connection: keep-alive
ETag: "5e93d971-264"
Accept-Ranges: bytes
```

## Configuring a virtual host

Configure the server.

[nginx documention](https://nginx.org/en/docs/http/configuring_https_servers.html "Configuring ssl/tls")

```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
}
```

Test the configuration.

```bash
sudo nginx -t
```

Reload the configuration.

```bash
sudo nginx -s reload
```

Confirm ports are open/listening.

```bash
sudo ss -plnt4 | awk '$4 ~ /:(80|443)/ {print $4, $6}'
```

Test the site.

```bash
openssl s_client -connect netsec-www.netsec.cte:443
```
