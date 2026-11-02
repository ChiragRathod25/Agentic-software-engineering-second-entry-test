import json
import urllib.request
import urllib.error
from packaging.specifiers import SpecifierSet
from packaging.version import parse as parse_version

PYTHON_TARGET = '3.11'

input_depedencies = ["django==4.2",
                     "numpy==2.3.0",
                     "scipy==1.7.0",
                     "scikit-learn==1.4.0",
                     "fastapi-agent-router==0.3.1",
                     "matplotlib==3.99.0",
                     "six==1.16.0",
                     "requests==2.32.0"]

total_checked = len(input_depedencies)
not_found_count = 0
incompatible_count = 0

highest_pkg = None
highest_min_version = None
highest_spec_str = ""

for item in input_depedencies:
  pkg_name, pinned_ver = item.split("==")
  url = f"https://pypi.org/pypi/{pkg_name}/{pinned_ver}/json"
  
  try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
      data = json.loads(resp.read())
  except urllib.error.HTTPError as e:
    if e.code == 404:
      not_found_count += 1
      continue
    raise
  except urllib.error.URLError:
    not_found_count += 1
    continue

  requires_python = data.get("info",{}).get("requires_python")
  if requires_python:
    spec = SpecifierSet(requires_python)
    if PYTHON_TARGET not in spec:
      incompatible_count += 1

    for s in spec:
      if s.operator in (">=", ">"):
        v = parse_version(s.version)
        if highest_min_version is None or v > highest_min_version:
          highest_min_version = v
          highest_pkg = pkg_name
          highest_spec_str = requires_python

print(f"Dependencies checked: {total_checked}")
print(f"Not found on PyPI: {not_found_count}")
print(f"Incompatible with Python 3.11: {incompatible_count}")
if highest_pkg:
    print(f"Highest requirement: {highest_pkg} ({highest_spec_str})")