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

