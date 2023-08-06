#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import glob
import os

import nslookup

# globally load dynamic domains list from absolute path in python lib
pwd = os.path.abspath(os.path.dirname(__file__))
domains_files = glob.glob(pwd + "/dyn_lists/*")
domainslist = []
for file in domains_files:
    domainslist += [domain.strip() for domain in open(file, 'r').readlines()]

# use cloudflare DNS servers, avoid local filtering DNS configs
cloudflare_dns = ["1.1.1.1", "1.0.0.1"]
dns = nslookup.Nslookup(dns_servers=cloudflare_dns)


def dyntwist(keyword):
    """Given keyword, load dynamic domains from corpus to see what dynamic subdomains resolve with that keyword."""
    dynamic_domains = set(["{}.{}".format(keyword, dyn_domain.strip('.')) for dyn_domain in domainslist])

    futures_list = []
    results = []

    # https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html#generic-workflows-for-running-tasks-concurrently
    worker_max = 2 * os.cpu_count()
    with ThreadPoolExecutor(max_workers=worker_max) as executor:
        for domain in dynamic_domains:
            futures = executor.submit(process_domain, domain)
            futures_list.append(futures)
        for future in futures_list:
            try:
                result = future.result(timeout=60)
                results.append(result)
            except Exception:
                results.append(None)
    return results


def process_domain(domain):
    """Given domain, check DNS resolution and return domain object data"""
    ips = dns.dns_lookup(domain).answer
    return {"domain": domain, "dns": ips}
