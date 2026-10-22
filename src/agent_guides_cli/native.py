"""Deterministic short-entry rendition and narrowly owned native surfaces.

No topic selection logic, host mutation or client execution. Registration inspection
uses a bounded JSON/JSONC and Markdown subset, not an exhaustive native loader model.
"""

import json
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


def render_parts(value, snapshot, files, *, root=False):
    """One shared preamble and one exact rendered section per bundle/binding."""
    text = "# Selected guidance\n\n"
    text += ("Use each authored entry only within its declared directory scope. "
             "Native project instructions and local exceptions remain authoritative.\n\n")
    shared, sections = text.encode("utf-8"), []
    for item in value["bundles"]:
        namespace = f"{item['source']}/{item['id']}"
        declaration = bundles.declaration(files[namespace + "/guidance-bundle.json"])
        entry = declaration["entry"]
        prefix = (".guidance/" if root else "") + f"selections/{snapshot}/{namespace}"
        text = f"## {item['id']} — scope `{item['binding']}`\n\n"
        text += f"Source `{item['source']}`; original entry: [{entry}]({prefix}/{entry}).\n\n"
        text += relocate(files[namespace + "/" + entry].decode("utf-8"), entry, prefix).rstrip() + "\n\n"
        sections.append((item, text.encode("utf-8")))
    return shared, sections


def render(value, snapshot, files, *, root=False):
    shared, sections = render_parts(value, snapshot, files, root=root)
    raw = shared + b"".join(raw for _, raw in sections)
    if len(raw) > 1024 * 1024:
        raise GuidanceError("combined short entry exceeds byte limit")
    return raw


def entry_sizes(value, snapshot, files, *, root=False):
    """Exact UTF-8 rendered bytes, including headings/links; not token estimates.

    Repeated bindings count separately, as they do in render(). Shared overhead
    counts only the common preamble; native wrapper/local instruction bytes are
    outside this index measurement. Root rendition has different relocated links.
    """
    shared, sections = render_parts(value, snapshot, files, root=root)
    return {"unit": "utf8_bytes", "root": root, "shared_overhead": len(shared),
            "bundles": [{"source": item["source"], "id": item["id"],
                         "binding": item["binding"], "rendered_bytes": len(raw)}
                        for item, raw in sections],
            "total": len(shared) + sum(len(raw) for _, raw in sections),
            "token_count": "not_measured"}


def configuration():
    return canonical({"$schema": "https://opencode.ai/config.json",
                      "instructions": [".guidance/entry.md"]})


def block(newline=b"\n"):
    return newline + newline.join((BEGIN, IMPORT, END, b""))


def edit_block(raw, old, new):
    """Only replace exact owned bytes; preserve every unrelated byte."""
    if old is None:
        if BEGIN in raw or END in raw or any(entry_registration(p) for p in markdown_imports(raw)):
            raise GuidanceError("competing or unowned Claude instruction registration")
        return raw + new
    if raw.count(old) != 1 or raw.count(BEGIN) != 1 or raw.count(END) != 1:
        raise GuidanceError("modified owned CLAUDE.md block; resolve explicitly")
    if any(entry_registration(p) for p in markdown_imports(raw.replace(old, b"", 1))):
        raise GuidanceError("competing Claude import outside owned block")
    return raw.replace(old, new, 1)


def agents_block(entry, newline=b"\n"):
    if BEGIN in entry or END in entry:
        raise GuidanceError("authored entry conflicts with native ownership markers")
    return newline + BEGIN + newline + entry.replace(b"\r\n", b"\n").replace(b"\n", newline) + END + newline


def edit_agents(raw, old, new):
    if old is None:
        if BEGIN in raw or END in raw or any(entry_registration(p) for p in markdown_imports(raw)):
            raise GuidanceError("competing or unowned AGENTS.md registration")
        return raw + new
    if raw.count(old) != 1 or raw.count(BEGIN) != 1 or raw.count(END) != 1:
        raise GuidanceError("modified owned AGENTS.md block; resolve explicitly")
    if any(entry_registration(p) for p in markdown_imports(raw.replace(old, b"", 1))):
        raise GuidanceError("competing AGENTS.md import outside owned block")
    return raw.replace(old, new, 1)


def entry_registration(path, project=None):
    """Canonicalize direct local path aliases; do not interpret shell commands."""
    normalized = posixpath.normpath(path).casefold()
    if normalized == ".guidance/entry.md":
        return True
    return project is not None and posixpath.normpath(posixpath.join(str(project), path)).casefold() == str(project / ENTRY).casefold()


def imports_agents(raw):
    paths = [p for p in markdown_imports(raw) if posixpath.basename(p).lower() == "agents.md"]
    return len(paths) == 1 and paths[0] in ("AGENTS.md", "./AGENTS.md")


def has_agents_import(raw):
    """Keep ambiguous real imports distinguishable from prose for managed reuse."""
    return any(posixpath.basename(p).lower() == "agents.md" for p in markdown_imports(raw))


def markdown_imports(raw):
    """Recognize @path imports outside fenced/inline code; do not follow them.

    This bounded inventory supports unquoted paths and quoted paths. It does not
    interpret all Markdown or discover indirect imports/native settings globally.
    """
    text = raw.decode("utf-8")
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(re.sub(r"(`+).*?\1", "", line))
    text = "\n".join(lines)
    return [next(p for p in match.groups() if p) for match in re.finditer(
        r'''(?<![\w@\\])@(?:"([^"\n]+)"|'([^'\n]+)'|([^\s`<>"'(),;]+))''', text)]


def registration_strings(raw):
    """Read executable registration fields, ignoring comments and prose fields.

    JSONC supports comments/trailing commas here. Invalid/unsupported documents
    fail closed rather than silently declaring their registrations absent.
    User documents are never rewritten or executed.
    """
    text = raw.decode("utf-8")
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/|[^"/]+|/', text)
    text = "".join(" " if t.startswith(("//", "/*")) else t for t in tokens)
    # Preserve string tokens verbatim while removing only structural trailing commas.
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\s+|.', text)
    for index, token in enumerate(tokens):
        if token == "," and next((t for t in tokens[index + 1:] if not t.isspace()), "") in ("}", "]"):
            tokens[index] = ""
    try:
        value = json.loads("".join(tokens))
    except ValueError as error:
        raise GuidanceError("cannot inspect native JSON/JSONC registrations; resolve explicitly") from error
    if not isinstance(value, dict):
        raise GuidanceError("native JSON/JSONC configuration must be an object")

    def strings(item):
        if isinstance(item, str):
            yield item
        elif isinstance(item, list):
            for child in item:
                yield from strings(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                if key not in ("description", "title", "$schema"):
                    yield from strings(child)

    def hook_commands(item):
        if isinstance(item, list):
            for child in item:
                yield from hook_commands(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                if key in ("command", "prompt"):
                    yield from strings(child)
                elif isinstance(child, (dict, list)):
                    yield from hook_commands(child)

    result = [text for key in ("plugin", "plugins", "instructions", "imports")
              for text in strings(value.get(key))]
    enabled = value.get("enabledPlugins", {})
    if isinstance(enabled, dict):
        result.extend(key for key, active in enabled.items() if active is True)
    result.extend(hook_commands(value.get("hooks")))
    return result


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
        names += ["CLAUDE.md", "AGENTS.md", ".claude/settings.json", ".claude/settings.local.json"]
    if "opencode" in selected:
        names += ["AGENTS.md", "opencode.json", "opencode.jsonc",
                  CONFIG, ".opencode/opencode.jsonc"]
    for name in dict.fromkeys(names):
        path = project / name
        if path.exists() or path.is_symlink():
            raw = regular_bytes(path)
            registrations = registration_strings(raw) if name.endswith((".json", ".jsonc")) else markdown_imports(raw)
            legacy = any(token in text.lower() for text in registrations
                          for token in ("flutter-agent-guidelines", "flutter_agent_guidelines"))
            competing = any(entry_registration(text, project) for text in registrations)
            markers = BEGIN in raw or END in raw
            if name == CLAUDE:
                outside = raw.replace(block(), b"").replace(block(b"\r\n"), b"")
                if any(entry_registration(p, project) for p in markdown_imports(outside)):
                    raise GuidanceError("competing Claude import outside owned block")
            elif name == AGENTS and competing:
                raise GuidanceError("competing AGENTS.md import")
            if legacy or competing or markers:
                # Owned surfaces are separately validated against the retained lock.
                if name not in (CLAUDE, *owned):
                    raise GuidanceError(f"competing guidance registration: {name}")
                if legacy:
                    raise GuidanceError(f"legacy guidance registration: {name}; migrate explicitly")
