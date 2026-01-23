import os
import subprocess
import requests
import json
import sys

DOMAIN = os.environ["R2_CUSTOM_DOMAIN"]
ZONE_ID = os.environ["CF_ZONE_ID"]
TOKEN = os.environ["CF_PURGE_API_TOKEN"]
GITHUB_BEFORE = os.environ.get("GITHUB_BEFORE", "")
GITHUB_AFTER = os.environ.get("GITHUB_AFTER", "")

ORIGINS = [
    "https://limbus-teams.eldritchtools.com",
    "https://limbus-md.eldritchtools.com",
    "http://localhost:3000"
]


def get_changed_json_files(before, after):
    """Return list of changed JSON files in data/ between commits."""
    if not before or not after:
        return []
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", before, after],
            capture_output=True,
            text=True,
            check=True,
        )
        files = result.stdout.splitlines()
        return [f for f in files if f.startswith("data/") and f.endswith(".json")]
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        return []


def build_purge_payload(files, origins):
    """Return a single payload with all files for all origins."""
    payload_files = []
    for origin in origins:
        for f in files:
            full_url = f"{DOMAIN}/{f}"
            payload_files.append({"url": full_url, "headers": {"Origin": origin}})
    return {"files": payload_files}


def main():
    changed_files = get_changed_json_files(GITHUB_BEFORE, GITHUB_AFTER)
    all_files = ["meta.json"] + changed_files

    print("Purging the following files:")
    for f in all_files:
        print(f" - {DOMAIN}/{f}")

    payload = build_purge_payload(all_files, ORIGINS)

    # Send single purge request
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/purge_cache",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
    )

    if response.status_code == 200:
        print(
            f"Successfully purged {len(all_files)} file(s) for {len(ORIGINS)} origin(s)."
        )
    else:
        print("Failed to purge cache.")
        print(response.status_code, response.text)


if __name__ == "__main__":
    main()
