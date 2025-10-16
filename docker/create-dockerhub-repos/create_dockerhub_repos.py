#!/usr/bin/env python3
"""
Create Docker Hub repositories (private or public) from a list of names,
using the Docker Hub v2 API (modern / recommended endpoints).
"""

import argparse
import json
import requests
import sys
from typing import Tuple, Optional

# Base URL for Docker Hub API
BASE = "https://hub.docker.com/v2"

def get_jwt_token(username: str, token: str) -> Optional[str]:
    """
    Get JWT token by logging in (if PAT not directly usable in Authorization).
    Some Docker Hub APIs expect `Authorization: JWT <token>`.
    """
    login_url = f"{BASE}/users/login/"
    payload = {"username": username, "password": token}
    resp = requests.post(login_url, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        jwt = data.get("token")
        return jwt
    else:
        print(f"❌ Failed to login for JWT: HTTP {resp.status_code} — {resp.text}")
        return None

def create_repo_v2(namespace: str, repo_name: str, is_private: bool,
                   description: Optional[str], full_description: Optional[str],
                   auth_header: dict) -> Tuple[int, str]:
    """
    Try the modern endpoint POST /v2/repositories/
    """
    url = f"{BASE}/repositories/"
    payload = {
        "namespace": namespace,
        "name": repo_name,
        "is_private": is_private
    }
    if description is not None:
        payload["description"] = description
    if full_description is not None:
        payload["full_description"] = full_description

    resp = requests.post(url, headers=auth_header, json=payload)
    return resp.status_code, resp.text

def create_repo_namespace_endpoint(namespace: str, repo_name: str, is_private: bool,
                                   description: Optional[str], full_description: Optional[str],
                                   auth_header: dict) -> Tuple[int, str]:
    """
    Try alternate legacy endpoint POST /v2/repositories/{namespace}/
    """
    url = f"{BASE}/repositories/{namespace}/"
    payload = {
        "name": repo_name,
        "is_private": is_private
    }
    if description is not None:
        payload["description"] = description
    if full_description is not None:
        payload["full_description"] = full_description

    resp = requests.post(url, headers=auth_header, json=payload)
    return resp.status_code, resp.text

def main():
    parser = argparse.ArgumentParser(description="Create Docker Hub repositories from a names file, using newer API endpoints.")
    parser.add_argument("--user", required=True, help="Docker Hub username")
    parser.add_argument("--token", required=True, help="Docker Hub access token or password")
    parser.add_argument("--file", required=True, help="File with repo names (one per line)")
    parser.add_argument("--org", help="Organization or namespace to create repos under; defaults to username")
    parser.add_argument("--public", action="store_true", help="Make repositories public (default is private)")
    parser.add_argument("--desc", help="Short description (up to 100 chars) for all repos")
    parser.add_argument("--full-desc", help="Full description / long form description for all repos")

    args = parser.parse_args()

    namespace = args.org if args.org else args.user
    is_private = not args.public

    # Read repo names
    try:
        with open(args.file, "r") as f:
            repos = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    if not repos:
        print("⚠️ No repositories to create.")
        sys.exit(0)

    # Authenticate / get JWT
    jwt = get_jwt_token(args.user, args.token)
    if jwt is None:
        print("❌ Could not obtain JWT token; aborting.")
        sys.exit(1)

    auth_header = {"Authorization": f"JWT {jwt}", "Content-Type": "application/json"}

    for repo in repos:
        print(f"🔧 Creating {namespace}/{repo} ...", end=" ")
        status, text = create_repo_v2(namespace, repo, is_private, args.desc, args.full_desc, auth_header)
        if status in (201, 202):
            print("✅ Created via /repositories/")
        else:
            # Try fallback
            status2, text2 = create_repo_namespace_endpoint(namespace, repo, is_private, args.desc, args.full_desc, auth_header)
            if status2 in (201, 202):
                print("✅ Created via /repositories/{namespace}/ fallback")
            else:
                print(f"❌ Failed (primary HTTP {status} / fallback HTTP {status2}) — primary: {text} | fallback: {text2}")

if __name__ == "__main__":
    main()
