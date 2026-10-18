"""Small self-contained Markdown declaration; no execution or semantic retrieval."""

import posixpath
import re
from urllib.parse import unquote, urlsplit

from . import git_source
from .integrity import (GuidanceError, MAX_TOTAL, fields, identifier, inventory,
                        parse_json, relative_name)

DECLARATION = "guidance-bundle.json"
MAX_MANIFEST = 64 * 1024


def declaration(raw):
    value = parse_json(raw, MAX_MANIFEST)
    fields(value, ("schema", "id", "entry", "files", "notices"))
    if type(value["schema"]) is not int or value["schema"] != 1:
        raise GuidanceError("unsupported bundle schema")
    identifier(value["id"])
    if not isinstance(value["files"], list) or not isinstance(value["notices"], list):
        raise GuidanceError("bundle files/notices must be lists")
    if not all(isinstance(n, str) for n in value["files"] + value["notices"]):
        raise GuidanceError("bundle paths must be strings")
    inventory(value["files"] + [DECLARATION, "manifest.json"])
    if (value["entry"] not in value["files"] or not value["entry"].endswith(".md") or
            not value["notices"] or len(set(value["notices"])) != len(value["notices"]) or
            not set(value["notices"]) <= set(value["files"])):
        raise GuidanceError("entry/notices must be declared files; at least one notice required")
    return value


def link_target(document, target, names):
    # Decode repeatedly to prevent hidden traversal or platform-specific ambiguity.
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    for _ in range(4):
        decoded = unquote(target)
        if decoded == target:
            break
        target = decoded
    if "%" in target or "\\" in target or any(ord(c) < 32 for c in target):
        raise GuidanceError("ambiguous/encoded Markdown link")
    try:
        parsed = urlsplit(target)
    except ValueError as error:
        raise GuidanceError("invalid Markdown link") from error
    if parsed.scheme:
        if parsed.scheme in ("https", "http") and parsed.netloc:
            return
        if parsed.scheme == "mailto" and parsed.path:
            return
        raise GuidanceError("unsupported Markdown link scheme")
    if parsed.netloc or parsed.path.startswith("/") or parsed.query:
        raise GuidanceError("absolute/ambiguous local Markdown link")
    if not parsed.path:
        return
    destination = posixpath.normpath(posixpath.join(posixpath.dirname(document), parsed.path))
    relative_name(destination)
    if destination not in names:
        raise GuidanceError(f"undeclared/missing local link: {document} -> {target}")


def links(files):
    for name, raw in files.items():
        if not name.endswith(".md"):
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeError as error:
            raise GuidanceError("Markdown must be UTF-8") from error
        # Inline links/images, reference definitions and URI autolinks. Optional
        # quoted titles are not destinations. This is validation, not rendering.
        if re.search(r"(?i)<[a-z][^>]*\b(?:href|src)\s*=", text):
            raise GuidanceError("HTML navigation is outside the declared Markdown link subset")
        inline = list(re.finditer(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]*>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", text))
        # Account for every destination opener, including labels outside this
        # subset (nested/escaped brackets). Reusing the label regex here would
        # silently omit those same unsupported labels from the rejection check.
        starts = {text.index("](", match.start(), match.end()) for match in inline}
        if any(match.start() not in starts for match in re.finditer(r"\]\(", text)):
            raise GuidanceError("unsupported inline Markdown link syntax")
        targets = [match.group(1) for match in inline]
        targets += re.findall(r"(?m)^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]*>|\S+)", text)
        targets += re.findall(r"<([A-Za-z][A-Za-z0-9+.-]*:[^>\n]+)>", text)
        for target in targets:
            link_target(name, target, files)


def validate_files(files):
    if sum(map(len, files.values())) > MAX_TOTAL:
        raise GuidanceError("bundle total byte limit")
    value = declaration(files.get(DECLARATION, b""))
    if set(files) != set(value["files"]) | {DECLARATION}:
        raise GuidanceError("undeclared/missing bundle files")
    links(files)
    return value


def materialize(objects, revision, path):
    entries = git_source.tree(objects, revision, path)
    inventory(list(entries))
    if DECLARATION not in entries:
        raise GuidanceError("bundle declaration missing")
    raw = git_source.blob(objects, entries[DECLARATION], MAX_MANIFEST)
    value = declaration(raw)
    if set(entries) != set(value["files"]) | {DECLARATION}:
        raise GuidanceError("undeclared/missing Git bundle files")
    files, total = {DECLARATION: raw}, len(raw)
    for name in value["files"]:
        content = git_source.blob(objects, entries[name])
        total += len(content)
        if total > MAX_TOTAL:
            raise GuidanceError("bundle total byte limit")
        files[name] = content
    validate_files(files)
    return value, files
