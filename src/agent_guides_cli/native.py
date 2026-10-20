"""Deterministic short-entry rendition and narrowly owned native surfaces.

No topic selection logic, settings parser, host mutation or client execution.
"""

import posixpath
import re
from urllib.parse import unquote, urlsplit

from . import bundles, git_source
from .integrity import (GuidanceError, canonical, fields, identifier, regular_bytes,
                        require_digest)

ENTRY = ".guidance/entry.md"
CONFIG = ".opencode/opencode.json"
ROOT_CONFIG = "opencode.json"
AGENTS = "AGENTS.md"
STATE = ".guidance/connection.json"
CLAUDE = "CLAUDE.md"
BEGIN = b"<!-- agent-guides-cli:begin -->"
END = b"<!-- agent-guides-cli:end -->"
IMPORT = b"@./.guidance/entry.md"


def clients(value):
    if (not isinstance(value, list) or not value or
            any(v not in ("claude", "opencode") for v in value) or
            len(set(value)) != len(value)):
        raise GuidanceError("select unique clients: claude, opencode")
    return sorted(value)


def validate_connection(value):
    fields(value, ("schema", "clients", "entry", "revisions"), ("route", "config", "host"))
    if type(value["schema"]) is not int or value["schema"] != 1:
        raise GuidanceError("unsupported connection schema")
    if clients(value["clients"]) != value["clients"]:
        raise GuidanceError("noncanonical client selection")
    require_digest(value["entry"])
    if not isinstance(value["revisions"], dict):
        raise GuidanceError("invalid exact-revision policy")
    for name, revision in value["revisions"].items():
        identifier(name)
        git_source.commit(revision)
    route = value.get("route", "project")
    if route not in ("project", "managed"):
        raise GuidanceError("unsupported OpenCode connection route")
    if route == "managed":
        if "opencode" not in value["clients"] or value.get("config") is not None:
            raise GuidanceError("invalid managed client/config selection")
        require_digest(value.get("host"))
    elif "opencode" not in value["clients"] and value.get("config") is not None:
        raise GuidanceError("unselected OpenCode cannot own project configuration")
    elif "opencode" in value["clients"] and value.get("config", CONFIG) not in (CONFIG, ROOT_CONFIG):
        raise GuidanceError("unsupported owned project config path")
    elif value.get("host") is not None:
        raise GuidanceError("project route cannot claim managed configuration")


def relocate(text, entry, prefix):
    """Relocate only the conservative Markdown subset already validated by T02."""
    def target(match):
        raw = match.group(1)
        angled = raw.startswith("<") and raw.endswith(">")
        value = unquote(raw[1:-1] if angled else raw)
        parsed = urlsplit(value)
        if parsed.scheme:
            return match.group(0)
        path = posixpath.normpath(posixpath.join(posixpath.dirname(entry), parsed.path)) if parsed.path else entry
        rewritten = prefix + "/" + path
        if parsed.fragment:
            rewritten += "#" + parsed.fragment
        if angled:
            rewritten = "<" + rewritten + ">"
        start, end = match.span(1)
        return match.group(0)[:start - match.start()] + rewritten + match.group(0)[end - match.start():]

    text = re.sub(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]*>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", target, text)
    text = re.sub(r"(?m)^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]*>|\S+)", target, text)
    # A root index combines several entries. Namespace reference labels rather
    # than letting one bundle's reference definition shadow another's.
    namespace = prefix.replace("/", "-") + "-"
    normalize = lambda label: " ".join(label.split()).casefold()
    labels = {normalize(label): namespace + str(index) for index, label in
              enumerate(re.findall(r"(?m)^ {0,3}\[([^\]\n]+)\]:", text))}

    def reference(match):
        if text[match.end():].startswith(("(", ":")):
            return match.group(0)
        label = match.group(3) or match.group(2)
        replacement = labels.get(normalize(label))
        return match.group(1) + "[" + replacement + "]" if replacement else match.group(0)

    text = re.sub(r"(!?\[([^\]\n]+)\])(?:\[([^\]\n]*)\])?", reference, text)
    return re.sub(r"(?m)^( {0,3})\[([^\]\n]+)\]:",
                  lambda match: match.group(1) + "[" + labels[normalize(match.group(2))] + "]:", text)


def render(value, snapshot, files, *, root=False):
    text = "# Selected guidance\n\n"
    text += ("Use each authored entry only within its declared directory scope. "
             "Native project instructions and local exceptions remain authoritative.\n\n")
    for item in value["bundles"]:
        namespace = f"{item['source']}/{item['id']}"
        declaration = bundles.declaration(files[namespace + "/guidance-bundle.json"])
        entry = declaration["entry"]
        prefix = (".guidance/" if root else "") + f"selections/{snapshot}/{namespace}"
        text += f"## {item['id']} — scope `{item['binding']}`\n\n"
        text += f"Source `{item['source']}`; original entry: [{entry}]({prefix}/{entry}).\n\n"
        text += relocate(files[namespace + "/" + entry].decode("utf-8"), entry, prefix).rstrip() + "\n\n"
    raw = text.encode("utf-8")
    if len(raw) > 1024 * 1024:
        raise GuidanceError("combined short entry exceeds byte limit")
    return raw


def configuration():
    return canonical({"$schema": "https://opencode.ai/config.json",
                      "instructions": [".guidance/entry.md"]})


def block(newline=b"\n"):
    return newline + newline.join((BEGIN, IMPORT, END, b""))


def edit_block(raw, old, new):
    """Only replace exact owned bytes; preserve every unrelated byte."""
    if old is None:
        if BEGIN in raw or END in raw or IMPORT in raw:
            raise GuidanceError("competing or unowned Claude instruction registration")
        return raw + new
    if raw.count(old) != 1 or raw.count(BEGIN) != 1 or raw.count(END) != 1:
        raise GuidanceError("modified owned CLAUDE.md block; resolve explicitly")
    return raw.replace(old, new, 1)


def agents_block(entry, newline=b"\n"):
    if BEGIN in entry or END in entry:
        raise GuidanceError("authored entry conflicts with native ownership markers")
    return newline + BEGIN + newline + entry.replace(b"\r\n", b"\n").replace(b"\n", newline) + END + newline


def edit_agents(raw, old, new):
    if old is None:
        if BEGIN in raw or END in raw or b".guidance/entry.md" in raw:
            raise GuidanceError("competing or unowned AGENTS.md registration")
        return raw + new
    if raw.count(old) != 1 or raw.count(BEGIN) != 1 or raw.count(END) != 1:
        raise GuidanceError("modified owned AGENTS.md block; resolve explicitly")
    return raw.replace(old, new, 1)


def imports_agents(raw):
    return len(re.findall(rb"(?m)^@(?:\./)?AGENTS\.md[ \t]*\r?$", raw)) == 1


def config_slot(project):
    # Config documents combine their instructions natively. Use an empty slot,
    # never parse, reserialize or claim ownership of existing JSON/JSONC bytes.
    for name, sibling in ((CONFIG, ".opencode/opencode.jsonc"), (ROOT_CONFIG, "opencode.jsonc")):
        if not any((project / n).exists() or (project / n).is_symlink() for n in (name, sibling)):
            return name
    raise GuidanceError("both native config slots are occupied; preserve user files and resolve registration explicitly")


def inspect(project, selected, *, owned=()):
    """Bounded competing-loader inventory for selected clients only.

    This does not claim exhaustive indirect-import/plugin detection.
    """
    names = []
    if "claude" in selected:
        names += ["CLAUDE.md", ".claude/settings.json", ".claude/settings.local.json"]
    if "opencode" in selected:
        names += ["AGENTS.md", "opencode.json", "opencode.jsonc",
                  CONFIG, ".opencode/opencode.jsonc"]
    for name in names:
        path = project / name
        if path.exists() or path.is_symlink():
            raw = regular_bytes(path).lower()
            if any(token in raw for token in (b"flutter-agent-guidelines", b"flutter_agent_guidelines",
                                               b"agent-guides-cli:begin", b".guidance/entry.md")):
                # Owned surfaces are separately validated against the retained lock.
                if name not in (CLAUDE, *owned):
                    raise GuidanceError(f"competing guidance registration: {name}")
                if b"flutter-agent-guidelines" in raw or b"flutter_agent_guidelines" in raw:
                    raise GuidanceError(f"legacy guidance registration: {name}; migrate explicitly")
