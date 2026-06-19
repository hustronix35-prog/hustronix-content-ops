"""Upload carousel PNGs to Slack."""

from __future__ import annotations

import json
import mimetypes
import urllib.error
import urllib.request
from pathlib import Path

from lib.env_config import load_env, require_env


def _api(method: str, url: str, token: str, data: dict | None = None) -> dict:
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _upload_one(token: str, channel: str, path: Path, comment: str = "") -> dict:
    file_size = path.stat().st_size
    meta = _api(
        "POST",
        "https://slack.com/api/files.getUploadURLExternal",
        token,
        {"filename": path.name, "length": file_size},
    )
    if not meta.get("ok"):
        raise RuntimeError(meta.get("error", "files.getUploadURLExternal failed"))

    upload_url = meta["upload_url"]
    file_id = meta["file_id"]

    with path.open("rb") as fh:
        raw = fh.read()
    put_req = urllib.request.Request(
        upload_url,
        data=raw,
        headers={"Content-Type": mimetypes.guess_type(path.name)[0] or "application/octet-stream"},
        method="POST",
    )
    with urllib.request.urlopen(put_req, timeout=120):
        pass

    complete = _api(
        "POST",
        "https://slack.com/api/files.completeUploadExternal",
        token,
        {
            "files": [{"id": file_id, "title": path.stem}],
            "channel_id": channel,
            "initial_comment": comment,
        },
    )
    if not complete.get("ok"):
        raise RuntimeError(complete.get("error", "files.completeUploadExternal failed"))
    return complete


def upload_carousel_to_slack(
    png_paths: list[str | Path],
    *,
    option_num: int,
    hook: str,
    channel: str | None = None,
) -> dict:
    load_env()
    token = require_env("SLACK_BOT_TOKEN")
    channel = channel or require_env("SLACK_CHANNEL_ID")

    paths = [Path(p) for p in png_paths if Path(p).exists()]
    if not paths:
        raise RuntimeError("No PNG slides found to upload")

    uploaded = []
    for i, path in enumerate(paths):
        comment = ""
        if i == 0:
            comment = (
                f"*Carousel for OPTION {option_num}*\n"
                f"_{hook}_\n\n"
                f"{len(paths)} slides · Review below, then reply *publish* to post on LinkedIn."
            )
        result = _upload_one(token, channel, path, comment=comment)
        uploaded.append({"file": path.name, "ok": result.get("ok", True)})

    return {
        "success": True,
        "uploaded_count": len(uploaded),
        "channel": channel,
        "files": uploaded,
    }


def upload_carousel_optional(
    png_paths: list[str | Path],
    option_num: int,
    hook: str,
) -> dict:
    load_env()
    import os

    if not os.environ.get("SLACK_BOT_TOKEN") or not os.environ.get("SLACK_CHANNEL_ID"):
        return {
            "success": False,
            "skipped": True,
            "reason": "Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID",
            "local_paths": [str(p) for p in png_paths],
        }
    try:
        return upload_carousel_to_slack(png_paths, option_num=option_num, hook=hook)
    except Exception as exc:
        return {"success": False, "error": str(exc), "local_paths": [str(p) for p in png_paths]}
