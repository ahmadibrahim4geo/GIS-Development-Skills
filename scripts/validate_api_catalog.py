#!/usr/bin/env python3
"""Offline structural validator for curated web service entries."""
import json
import re
from urllib.parse import urlsplit
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'references' / 'free-geospatial-apis.json'
REQUIRED = ('id', 'name', 'category', 'documentation_url', 'service_url',
            'access', 'authentication', 'coverage', 'formats', 'limits',
            'attribution', 'use_cases', 'caveat', 'verified_on')
ALLOWED_ACCESS = {'free-noncommercial', 'free-key-required', 'free-registration',
                  'free-limited', 'public-fair-use', 'public-with-asset-restrictions',
                  'restricted-public', 'temporarily-unavailable'}


def validate_catalog(path=CATALOG):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return ['Cannot read API catalog JSON: {}'.format(exc)]
    if not isinstance(data, dict):
        return ['API catalog root must be a JSON object']
    errors = []
    if data.get('schema_version') != '1.0':
        errors.append('Unsupported API schema_version')
    items = data.get('services')
    if not isinstance(items, list):
        return ['services must be an array']
    ids = set()
    for i, item in enumerate(items):
        tag = f'services[{i}]'
        if not isinstance(item, dict):
            errors.append(tag+' must be object')
            continue
        for field in REQUIRED:
            if field not in item:
                errors.append(f'{tag} missing {field}')
        for field in REQUIRED:
            if field in ('formats','use_cases'):
                if not isinstance(item.get(field), list) or not item[field] or not all(isinstance(s,str) and s.strip() for s in item[field]):
                    errors.append(f'{tag} invalid list {field}')
            elif not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f'{tag} invalid {field}')
        access = item.get('access')
        if not isinstance(access, str) or access not in ALLOWED_ACCESS:
            errors.append(f'{tag} unknown access type')
        for field in ('documentation_url', 'service_url', 'example_url'):
            if field in item:
                value = item[field]
                try:
                    valid_url = (isinstance(value, str)
                                 and value.startswith('https://')
                                 and not any(char.isspace() for char in value)
                                 and bool(urlsplit(value).hostname))
                except ValueError:
                    # Malformed bracketed hosts must be reported, not crash CI.
                    valid_url = False
                if not valid_url:
                    errors.append(f'{tag} {field} must be a valid HTTPS URL')
        ident = item.get('id')
        if not isinstance(ident, str) or not ident.strip():
            errors.append(f'{tag} invalid id')
        elif ident in ids:
            errors.append(f'{tag} duplicate id {ident}')
        else:
            ids.add(ident)
    return errors


if __name__ == '__main__':
    errors=validate_catalog()
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'API catalog valid: {len(json.loads(CATALOG.read_text(encoding="utf-8"))["services"])} services')
