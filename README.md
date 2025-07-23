# Subdomain Checker

A Python tool to generate and check the availability of subdomains under a given base domain. Supports subdomain generation using custom fragments or character sets, and can verify HTTP status and redirects.

---

## Features

* Generate subdomains by combining fragments or characters.
* Configurable minimum and maximum length of generated subdomains.
* Optionally include the base domain (without subdomain) in checks.
* Check HTTPS availability of generated subdomains.
* Detect and report redirects to a specified URL.
* Progress bar with live updates using `tqdm`.

---

## Requirements

* Python 3.7+
* `requests`
* `tqdm`

Install dependencies with:

```bash
pip install requests tqdm
```

---

## Configuration

Edit the variables at the top of `subdomain_checker.py` to customize:

* `use_fragments`: `True` to combine fragments, `False` to generate from charset.
* `fragments`: List of strings used when `use_fragments=True`.
* `char_set`: Characters used when `use_fragments=False`.
* `base_domain`: The root domain to check.
* `redirect_url`: URL prefix to detect redirects (empty string disables).
* `check_redirect`: Enable or disable redirect checking.
* `include_empty_subdomain`: Include the base domain without subdomain.
* `min_len` / `max_len`: Minimum and maximum length of generated subdomains.

---

## Usage

Run the script:

```bash
python subdomain_checker.py
```

The script will generate subdomains according to your configuration, check their HTTPS status, and print reachable domains and detected redirects.

Example output:

```
Checking 42 domains/subdomains...

[OK]            a05.zahls.ch -> Status: 200, Final URL: https://a05.zahls.ch/home
[REDIRECT]      pay.zahls.ch -> Redirected to https://signup.zahls.ch/

--- Reachable Domains (without redirect) ---
a05.zahls.ch
aarauagenturzahls.ch
...
```

---

## Notes

* The script uses a timeout of 5 seconds per request.
* Permutations are used when combining fragments (order matters).
* When using character sets, all combinations with repetition are generated.
* The progress bar updates live without cluttering the terminal.

---

## License

MIT License
