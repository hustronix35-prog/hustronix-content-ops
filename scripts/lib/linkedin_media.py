"""LinkedIn text + multi-image posts."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

from lib.env_config import load_env, require_env


def _request(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method=method,
    )
    with urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
        headers = dict(resp.headers)
        if body:
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                parsed = {"raw": body}
        else:
            parsed = {}
        parsed["_headers"] = headers
        return parsed


def register_image_upload(token: str, author: str) -> tuple[str, str]:
    resp = _request(
        "POST",
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        token,
        {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": author,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        },
    )
    value = resp.get("value", resp)
    upload_mechanism = value["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]
    upload_url = upload_mechanism["uploadUrl"]
    asset = value["asset"]
    return upload_url, asset


def upload_image_binary(upload_url: str, token: str, path: Path) -> None:
    raw = path.read_bytes()
    req = Request(
        upload_url,
        data=raw,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
        },
        method="PUT",
    )
    with urlopen(req, timeout=120):
        pass


def post_to_linkedin(text: str, image_paths: list[str | Path] | None = None) -> dict:
    load_env()
    token = require_env("LINKEDIN_ACCESS_TOKEN")
    author = require_env("LINKEDIN_AUTHOR_URN")

    media_entries = []
    if image_paths:
        for i, img_path in enumerate(image_paths[:9], 1):
            path = Path(img_path)
            if not path.exists():
                continue
            upload_url, asset = register_image_upload(token, author)
            upload_image_binary(upload_url, token, path)
            media_entries.append(
                {
                    "status": "READY",
                    "description": {"text": f"Slide {i}"},
                    "media": asset,
                    "title": {"text": path.stem},
                }
            )

    if media_entries:
        share_content = {
            "shareCommentary": {"text": text},
            "shareMediaCategory": "IMAGE",
            "media": media_entries,
        }
    else:
        share_content = {
            "shareCommentary": {"text": text},
            "shareMediaCategory": "NONE",
        }

    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {"com.linkedin.ugc.ShareContent": share_content},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    resp = _request("POST", "https://api.linkedin.com/v2/ugcPosts", token, payload)
    headers = resp.get("_headers", {})
    post_id = headers.get("X-RestLi-Id") or headers.get("x-restli-id") or "published"
    return {
        "success": True,
        "post_id": post_id,
        "chars": len(text),
        "images": len(media_entries),
    }
