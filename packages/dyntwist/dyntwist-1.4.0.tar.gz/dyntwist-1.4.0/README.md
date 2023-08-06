# dyntwist

Discover resolving dynamic DNS domains based on keywords.

#### Usage
```python
import dyntwist

result = dyntwist.dyntwist("solarwinds")
for r in results:
    if r.get("dns"):
        ip  = r["dns"][0]
        if ip != "174.128.255.252" and ip != "0.0.0.0":
            print(r)
```

example result snippet:
```python
{'domain': 'solarwinds.001www.com', 'dns': ['0.0.0.0']}
{'domain': 'solarwinds.16-b.it', 'dns': ['0.0.0.0']}
{'domain': 'solarwinds.32-b.it', 'dns': ['0.0.0.0']}
{'domain': 'solarwinds.64-b.it', 'dns': ['0.0.0.0']}
```

#### Caveats
 - Designed to work on unix style paths (for loading file lists)
