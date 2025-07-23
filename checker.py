import requests
from itertools import permutations, product
from tqdm import tqdm  

# === Configuration ===

use_fragments = True          # True = combine fragments, False = generate from chars
fragments = ["a05", "aarau", "agency", "suva", "-", "pay", "parking"]
char_set = "abcdefghijklmnopqrstuvwxyz0123456789"  # charset for subdomains if use_fragments=False

base_domain = "zahls.ch"
redirect_url = "https://signup.zahls.ch/"  # Leave empty ("") if no redirect check
check_redirect = True                      # Check for redirect?

include_empty_subdomain = True             # Also check base domain without subdomain?

min_len = 1  # Minimum length (fragments or chars)
max_len = 3  # Maximum length (fragments or chars)


def generate_subdomains_fragments(fragments, min_len=1, max_len=2, include_empty=False):
    print("Generating subdomains from fragments...")
    subdomains = set()
    if include_empty and min_len <= 0:
        subdomains.add("")

    for r in range(max(min_len, 1), max_len + 1):
        for combo in permutations(fragments, r):
            subdomain = "".join(combo)
            subdomains.add(subdomain)
    return subdomains


def generate_subdomains_chars(char_set, min_len=1, max_len=2, include_empty=False):
    print("Generating subdomains from character set...")
    subdomains = set()
    if include_empty and min_len <= 0:
        subdomains.add("")

    for length in range(max(min_len, 1), max_len + 1):
        for combo in product(char_set, repeat=length):
            subdomain = "".join(combo)
            subdomains.add(subdomain)
    return subdomains


def check_https(subdomain, base_domain):
    if subdomain:
        url = f"https://{subdomain}.{base_domain}"
    else:
        url = f"https://{base_domain}"

    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        final_url = response.url
        status = response.status_code
        return status, final_url, None
    except requests.RequestException as e:
        return None, None, str(e)


def main():
    if use_fragments:
        subdomains = generate_subdomains_fragments(fragments, min_len, max_len, include_empty_subdomain)
    else:
        subdomains = generate_subdomains_chars(char_set, min_len, max_len, include_empty_subdomain)

    print(f"Checking {len(subdomains)} domains/subdomains...\n")

    reachable_domains = []
    unreachable_domains = []

    with tqdm(sorted(subdomains), desc="Checking domains", unit="domain") as progress:
        for sd in progress:
            fqdn = f"{sd}.{base_domain}" if sd else base_domain
            progress.set_postfix_str(f"Current: {fqdn}")

            status, final_url, error = check_https(sd, base_domain)

            if status is None:
                unreachable_domains.append(fqdn)
            else:
                if check_redirect and redirect_url and final_url.startswith(redirect_url):
                    print(f"\n[REDIRECT]      {fqdn} -> Redirected to {redirect_url}")
                else:
                    print(f"\n[OK]            {fqdn} -> Status: {status}, Final URL: {final_url}")
                    reachable_domains.append(fqdn)

    print("\n--- Reachable Domains (without redirect) ---")
    for domain in reachable_domains:
        print(domain)


if __name__ == "__main__":
    main()
