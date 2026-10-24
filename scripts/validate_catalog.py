#!/usr/bin/env python3
"""Offline catalog structure checks (no network or third-party dependencies)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'references' / 'project-catalog.json'
REQUIRED = ('name', 'url', 'category', 'role', 'platforms', 'description',
            'reviewed_on', 'license', 'integration')
URL_PATTERN = re.compile(r'^https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/?$')


def validate_catalog(path=CATALOG):
    errors = []
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return ['Cannot read project catalog JSON: {}'.format(exc)]
    if not isinstance(data, dict):
        return ['Catalog root must be a JSON object']
    if data.get('schema_version') != '1.0':
        errors.append('Unsupported catalog schema_version')
    items = data.get('projects')
    if not isinstance(items, list):
        return ['projects must be an array']
    seen_urls = set()
    for i, entry in enumerate(items):
        tag = 'projects[{}]'.format(i)
        if not isinstance(entry, dict):
            errors.append('{} must be object'.format(tag))
            continue
        for field in REQUIRED:
            if field not in entry:
                errors.append('{} missing {}'.format(tag, field))
        url = entry.get('url', '')
        if not isinstance(url, str) or not URL_PATTERN.match(url):
            errors.append('{} invalid canonical GitHub URL'.format(tag))
        elif url.rstrip('/').casefold() in seen_urls:
            errors.append('{} duplicate URL'.format(tag))
        if isinstance(url, str):
            seen_urls.add(url.rstrip('/').casefold())
        if not isinstance(entry.get('platforms'), list) or not entry['platforms'] or not all(isinstance(x,str) and x for x in entry['platforms']):
            errors.append('{} nonempty platforms string array required'.format(tag))
        for field in ('name','category','description','role','license','integration','reviewed_on'):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append('{} invalid {}'.format(tag,field))
    return errors


if __name__ == '__main__':
    issues = validate_catalog()
    if issues:
        print('Catalog invalid:')
        for issue in issues:
            print(' - ' + issue)
        raise SystemExit(1)
    print('Catalog valid: {} sources'.format(len(json.loads(CATALOG.read_text(encoding='utf-8'))['projects'])))