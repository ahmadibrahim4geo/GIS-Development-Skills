#!/usr/bin/env python3
"""Search the curated API list without issuing network requests."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'references'/'free-geospatial-apis.json'


def search(services, query='', category='', access=''):
    matches=[]
    for s in services:
        if category and s['category']!=category:
            continue
        if access and s['access']!=access:
            continue
        searchable=' '.join([s['name'],s['category'],s['coverage'],' '.join(s['use_cases']),s['caveat']]).casefold()
        if query and query.casefold() not in searchable:
            continue
        matches.append(s)
    return matches


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--query',default='')
    p.add_argument('--category',default='')
    p.add_argument('--access',default='')
    args=p.parse_args()
    services=json.loads(CATALOG.read_text(encoding='utf-8'))['services']
    for s in search(services,args.query,args.category,args.access):
        print(f"{s['name']} | {s['category']} | {s['access']} | {s['documentation_url']}")


if __name__=='__main__':
    main()