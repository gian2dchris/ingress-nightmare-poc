# ingress-nightmare-poc
Ingress Nightmare PoC - not an RCE, yet.

NGINX Configuration Injection Injections PoCs
----
Configuration injection PoCs to exploit `CVE-2025-1974`, affected versions and prerequisites.

| CVE | PoC | Affected Versions| Notes |
|---|---|---|---|
| [CVE-2025-24514](https://github.com/kubernetes/kubernetes/issues/131006) | [auth-url-review.json](https://github.com/gian2dchris/ingress-nightmare-poc/blob/main/injection/auth-url-review.json) | < 1.11.5 | Can not exploit 1.12.x deployments which run with `--enable-annotation-validation` by default|
| [CVE-2025-1097](https://github.com/kubernetes/kubernetes/issues/131007) | [auth-tls-match-cn-review.json](https://github.com/gian2dchris/ingress-nightmare-poc/blob/main/injection/auth-tls-match-cn-review.json) | < 1.11.4 and < 1.12.1| Exploitation requires the attacker to know a valid in-cluster TLS secret. | 
| [CVE-2025-1098](https://github.com/kubernetes/kubernetes/issues/131008) | [mirror-annotations-review.json](https://github.com/gian2dchris/ingress-nightmare-poc/blob/main/injection/mirror-annotations-review.json) | < 1.11.4 / < 1.12.1 | No requirements ! |

Why not RCE ? 
---
| Steps | Implemented |
|----|----|
| Generate a malicious openssl engine | :white_check_mark: |
| Trigger NGINX client-body buffer feature (write `.so` on filesystem) | :white_check_mark: |
| Inject `ssl_engine` directive in nginx test configuration | :white_check_mark: |
| Bruteforce ProcFS paths | :white_check_mark: |
| Load malicious engine | :x: |

The main issue is that the malicious lib payload is larger than 8KB and is partially written on disk due to the size of client-body buffer causing nginx-ingress-controller to gracefully shutdown (core dumped error in logs) and openssl to raise a Bus error. Wiz poc video mentions the payload is padded to reach the size of 8KB, so we are looking for an engine / payload size < 8KB :) 

```
$ openssl req -engine ./proc.so 
Bus error
```
