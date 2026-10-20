"""Non-activating prepare/restore/verify against one portable exact selection."""

from importlib.metadata import version
from pathlib import Path

from . import bundles, git_source
from .integrity import (GuidanceError, MAX_TOTAL, canonical, checked_path, digest,
                        fields, identifier, inventory, parse_json, regular_bytes,
                        relative_name, require_digest)
from .storage import locked, save_bytes, verify_snapshot, write_snapshot

LOCK = "guidance.lock.json"


def engine_identity():
    root = Path(__file__).parent
    files = {p.name: digest(regular_bytes(p)) for p in sorted(root.glob("*.py"))}
    return {"version": version("agent-guides"), "digest": digest(canonical(files))}


def request(value, fixtures=None):
    fields(value, ("schema", "sources", "bundles"))
    if type(value["schema"]) is not int or value["schema"] != 1:
        raise GuidanceError("unsupported request schema")
    if not isinstance(value["sources"], list) or not 1 <= len(value["sources"]) <= 16:
        raise GuidanceError("select 1–16 sources")
    if not isinstance(value["bundles"], list) or not 1 <= len(value["bundles"]) <= 64:
        raise GuidanceError("select 1–64 bundles")
    sources = [git_source.source(s, fixtures) for s in value["sources"]]
    ids, urls = [s["id"] for s in sources], [s["url"] for s in sources]
    if len(set(ids)) != len(ids) or len(set(urls)) != len(urls):
        raise GuidanceError("duplicate source identity/locator")
    selections = []
    for item in value["bundles"]:
        fields(item, ("source", "path", "binding"))
        identifier(item["source"])
        if item["source"] not in ids:
            raise GuidanceError("unknown selected source")
        relative_name(item["path"], root=True)
        relative_name(item["binding"], root=True)
        selections.append(dict(item))
    keys = [(s["source"], s["path"], s["binding"]) for s in selections]
    if len(set(keys)) != len(keys):
        raise GuidanceError("duplicate bundle/binding pair")
    bindings = sorted({s["binding"] for s in selections if s["binding"] != "."})
    if bindings:
        inventory(bindings, directories=True)
    return sources, selections


def validate_lock(value, fixtures=None):
    fields(value, ("schema", "sources", "bundles", "engine"), ("connection",))
    if type(value["schema"]) is not int or value["schema"] != 1:
        raise GuidanceError("unsupported selection schema")
    if value["engine"] != engine_identity():
        raise GuidanceError("engine identity mismatch; restore needs recorded engine")
    if not isinstance(value["sources"], list) or not isinstance(value["bundles"], list):
        raise GuidanceError("invalid selection lists")
    for item in value["sources"]:
        git_source.source(item, fixtures, recorded=True)
    simplified_sources = [{k: s[k] for k in ("id", "url", "ref")} for s in value["sources"]]
    simplified_bundles = []
    ids = {}
    for item in value["bundles"]:
        fields(item, ("source", "path", "binding", "id", "snapshot"))
        identifier(item["id"])
        require_digest(item["snapshot"])
        key = (item["source"], item["path"])
        if item["id"] in ids and ids[item["id"]] != key:
            raise GuidanceError("duplicate bundle ID across different bundles")
        ids[item["id"]] = key
        simplified_bundles.append({k: item[k] for k in ("source", "path", "binding")})
    request({"schema": 1, "sources": simplified_sources, "bundles": simplified_bundles}, fixtures)
    if "connection" in value:
        from .native import validate_connection
        validate_connection(value["connection"])
        sources = {s["id"]: s for s in value["sources"]}
        for name, revision in value["connection"]["revisions"].items():
            if name not in sources or sources[name]["commit"] != revision:
                raise GuidanceError("exact-revision policy differs from recorded source")
    return value


def metadata(source, selection, declaration):
    return {"source": source["id"], "url": source["url"], "commit": source["commit"],
            "path": selection["path"], "id": declaration["id"],
            "entry": declaration["entry"], "notices": declaration["notices"]}


def snapshot_bundle(path, expected, source, selection):
    recorded, files = verify_snapshot(path, expected)
    declaration = bundles.validate_files(files)
    if recorded != metadata(source, selection, declaration) or declaration["id"] != selection["id"]:
        raise GuidanceError("bundle/source selection identity mismatch")
    return files


def selection_files(value, snapshot_root):
    files, total = {}, 0
    sources = {s["id"]: s for s in value["sources"]}
    for item in value["bundles"]:
        content = snapshot_bundle(snapshot_root / item["snapshot"], item["snapshot"],
                                  sources[item["source"]], item)
        for name, raw in content.items():
            total += len(raw)
            if total > MAX_TOTAL:
                raise GuidanceError("selection total byte limit")
            files[f"{item['source']}/{item['id']}/{name}"] = raw
    inventory(list(files) + ["manifest.json"])
    return files


def lock_preimage(project, fixtures):
    path = checked_path(project / LOCK)
    if not path.exists():
        return None
    raw = regular_bytes(path)
    read_lock(raw, digest(raw), fixtures)
    return raw


def content_lock(value):
    return {k: v for k, v in value.items() if k != "connection"}


def stage(project, value, cache):
    """Retain immutable content without publishing the portable lock."""
    files = selection_files(value, cache / "bundles")
    identity = digest(canonical(value))
    snapshots = checked_path(project / ".guidance/selections")
    stored = write_snapshot(snapshots, files, {"selection": content_lock(value)})
    return {"selection": identity, "snapshot": stored}


def publish(project, value, cache, preimage):
    """Only one portable lock is replaced, after complete candidate verification."""
    result = stage(project, value, cache)
    # Storage identity and portable selection identity are distinct and derivable.
    lock_path = checked_path(project / LOCK)
    current = regular_bytes(lock_path) if lock_path.exists() else None
    if current != preimage:
        raise GuidanceError("selection lock changed during preparation; preserve concurrent edits")
    save_bytes(lock_path, canonical(value))
    return result


def prepare(project, value, cache=None, *, fixtures=None):
    project = checked_path(project)
    if not project.is_dir():
        raise GuidanceError("project must be an existing directory")
    cache = checked_path(cache or project / ".guidance/cache")
    with locked(project / ".guidance"), locked(cache):
        require_unconnected(project)
        preimage = lock_preimage(project, fixtures)
        result = candidate(value, cache, fixtures=fixtures)
        return publish(project, result, cache, preimage)


def require_unconnected(project):
    if any((project / name).exists() for name in
           (".guidance/connection.json", ".guidance/transaction.json")):
        raise GuidanceError("native connection or recovery exists; use lifecycle commands")
    path = project / LOCK
    if path.exists() and "connection" in parse_json(regular_bytes(path)):
        raise GuidanceError("recorded connection exists; use lifecycle restore")


def candidate(value, cache, *, fixtures=None):
    """Resolve once per source; caller owns project/cache locks and activation."""
    sources, selections = request(value, fixtures)
    recorded = [{"id": s["id"], "url": s["url"], "ref": s["ref"],
                 "commit": git_source.resolve(s, fixtures)} for s in sources]
    by_id = {s["id"]: s for s in recorded}
    objects = {s["id"]: git_source.acquire(s, cache, fixtures) for s in recorded}
    chosen, ids = [], {}
    for item in selections:
        selected_source = by_id[item["source"]]
        declaration, files = bundles.materialize(objects[item["source"]],
                                                  selected_source["commit"], item["path"])
        key = (item["source"], item["path"])
        if declaration["id"] in ids and ids[declaration["id"]] != key:
            raise GuidanceError("duplicate bundle ID")
        ids[declaration["id"]] = key
        snapshot = write_snapshot(cache / "bundles", files,
                                  metadata(selected_source, item, declaration))
        chosen.append(dict(item, id=declaration["id"], snapshot=snapshot))
    result = {"schema": 1, "sources": sorted(recorded, key=lambda s: s["id"]),
              "bundles": sorted(chosen, key=lambda b: (b["source"], b["id"], b["binding"])),
              "engine": engine_identity()}
    return validate_lock(result, fixtures)


def read_lock(raw, expected, fixtures=None):
    require_digest(expected)
    if digest(raw) != expected:
        raise GuidanceError("expected selection identity mismatch")
    value = validate_lock(parse_json(raw), fixtures)
    if canonical(value) != raw:
        raise GuidanceError("selection must use canonical encoding")
    return value


def restore(project, raw, expected, cache=None, *, fixtures=None):
    value = read_lock(raw, expected, fixtures)
    project = checked_path(project)
    if not project.is_dir():
        raise GuidanceError("project must be an existing directory")
    cache = checked_path(cache or project / ".guidance/cache")
    with locked(project / ".guidance"), locked(cache):
        require_unconnected(project)
        if "connection" in value:
            raise GuidanceError("connected lock needs lifecycle restore")
        preimage = lock_preimage(project, fixtures)
        cached(value, cache, fixtures=fixtures)
        return publish(project, value, cache, preimage)


def cached(value, cache, *, fixtures=None):
    """Acquire recorded bundles offline; never resolve selectors."""
    sources = {s["id"]: s for s in value["sources"]}
    for item in value["bundles"]:
        target = checked_path(cache / "bundles" / item["snapshot"])
        if target.exists():
            snapshot_bundle(target, item["snapshot"], sources[item["source"]], item)
            continue
        selected_source = sources[item["source"]]
        objects = git_source.acquire(selected_source, cache, fixtures, offline=True)
        declaration, files = bundles.materialize(objects, selected_source["commit"], item["path"])
        actual = write_snapshot(cache / "bundles", files, metadata(selected_source, item, declaration))
        if actual != item["snapshot"]:
            raise GuidanceError("cached bundle differs from expected identity")


def verify(project, expected, *, fixtures=None):
    project = checked_path(project)
    value = read_lock(regular_bytes(project / LOCK), expected, fixtures)
    if "connection" in value or (project / ".guidance/transaction.json").exists():
        from .lifecycle import verify as verify_connection
        return verify_connection(project, expected, fixtures=fixtures)
    return verify_prepared(project, expected, fixtures=fixtures)


def verify_prepared(project, expected, *, fixtures=None):
    project = checked_path(project)
    value = read_lock(regular_bytes(project / LOCK), expected, fixtures)
    # Derive the storage manifest from the lock and recorded bundle manifests,
    # without needing the acquisition cache or resolving any source.
    # Find the single exact local snapshot by its metadata, then fully verify it.
    # Its ID is derived from lock + per-file hashes retained in bundle snapshots.
    matches = []
    parent = checked_path(project / ".guidance/selections")
    for path in parent.iterdir():
        if path.name.startswith(".candidate-"):
            continue
        require_digest(path.name)
        raw = regular_bytes(path / "manifest.json")
        candidate = parse_json(raw)
        if not isinstance(candidate, dict):
            raise GuidanceError("invalid prepared snapshot manifest")
        if candidate.get("metadata") == {"selection": content_lock(value)}:
            matches.append(path)
    if len(matches) != 1:
        raise GuidanceError("missing or ambiguous prepared selection snapshot")
    path = matches[0]
    _, files = verify_snapshot(path, path.name)
    sources = {s["id"]: s for s in value["sources"]}
    expected_files = set()
    for item in value["bundles"]:
        prefix = f"{item['source']}/{item['id']}/"
        bundle_files = {n.removeprefix(prefix): data for n, data in files.items() if n.startswith(prefix)}
        declaration = bundles.validate_files(bundle_files)
        manifest = {"schema": 1, "metadata": metadata(sources[item["source"]], item, declaration),
                    "files": {n: digest(data) for n, data in sorted(bundle_files.items())}}
        if declaration["id"] != item["id"] or digest(canonical(manifest)) != item["snapshot"]:
            raise GuidanceError("prepared bundle identity mismatch")
        expected_files.update(prefix + n for n in bundle_files)
    if set(files) != expected_files:
        raise GuidanceError("unexpected prepared bundle namespace")
    return {"selection": expected, "snapshot": path.name}
