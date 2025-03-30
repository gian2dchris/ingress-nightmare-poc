# ingress-nightmare-poc
Ingress Nightmare PoC - no RCE, yet :)

NGINX Configuration Injection Injections PoCs
----
Could not find a public configuration injection PoCs to exploit that affected both `1.11.x` and `1.12.x` ingress controller versions without any prerequisites so I created exploits for all configuration injections and documented the requirements and affected versions.

| CVE | PoC | Affected Versions| Notes|
|---|---|---|---|
| [CVE-2025-24514](https://github.com/kubernetes/kubernetes/issues/131006) | [auth-url-review.json](https://github.com/gian2dchris/ingress-nightmare-poc/blob/main/injection/auth-url-review.json) | < 1.11.5 | Can not exploit 1.12.x deployments which run with `--enable-annotation-validation` by default|
| [CVE-2025-1097](https://github.com/kubernetes/kubernetes/issues/131007) | [auth-tls-match-cn-review.json](https://github.com/gian2dchris/ingress-nightmare-poc/blob/main/injection/auth-tls-match-cn-review.json) | < 1.11.4 and < 1.12.1| Exploitation requires the attacker to know a valid in-cluster TLS secret. | 
| [CVE-2025-1098](https://github.com/kubernetes/kubernetes/issues/131008) | [mirror-annotations-review.json](https://github.com/gian2dchris/ingress-nightmare-poc/blob/main/injection/mirror-annotations-review.json) | < 1.11.4 / < 1.12.1 | No requirements ! |

Notes - TODOs
---
| Steps | Implemented |
|----|----|
| Generate a malicious `.so` lib that can be loaded as an openssl engine | :white_check_mark: |
| Trigger NGINX client-body buffer feature to write `.so` on filesystem | :white_check_mark: |
| Injects `ssl_engine` directive to load the malicious library | :white_check_mark: |
| Bruteforce ProcFS paths to load the malicious `.so` | :white_check_mark: |


*`*Why no RCE ? :(*

I am using the README for documentation in case I decide to spend more time on this in the future. The PoC succesfully does the steps mentioned above and is *relatively* stable. The main issue is that the malicious lib payload is larger than 8KB (size of client-body buffer) causing nginx-ingress-controller to gracefully shutdown with a core dumped error and openssl to raise a Bus error. Wiz poc video mentions the payload is padded to reach the size of 8KB, so all you have to do for rce is decrease the payload size below 8KB :) 

```
$ openssl req -engine ./proc.so 
Bus error
```