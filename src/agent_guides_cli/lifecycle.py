"""Journaled project-local connection, offline verification and exact recovery.

This module never starts clients or changes host/global configuration. Host
integrity is not evidence of native loading, model behavior or permission guards.
"""

from contextlib import contextmanager

from . import git_source, host, native, preparation as prep, transactions as tx
from .integrity import (GuidanceError, canonical, checked_path, digest, fields,
                        parse_json, regular_bytes)
from .storage import locked, make_directory, save_bytes, verify_snapshot


def project_root(project):
    project = checked_path(project)
    if not project.is_dir():
        raise GuidanceError("project must be an existing directory")
    if not (project / ".git").exists() and any((p / ".git").exists() for p in project.parents):
        raise GuidanceError("select the project or linked-worktree root, not a subdirectory")
    return project


def route_for(value):
    connection = value["connection"]
    return {"route": connection.get("route", "project"),
            "config": connection.get("config", native.CONFIG if "opencode" in connection["clients"] else None),
            "host": connection.get("host")}


def owned_paths(route):
    return [native.AGENTS] if route["route"] == "managed" else [route["config"]]


def config_available(project, route):
    if route["config"]:
        sibling = route["config"] + "c"
        if checked_path(project / sibling).exists():
            raise GuidanceError("competing native JSONC configuration; preserve user bytes and resolve explicitly")


def storage_ignore(project, *, create=False):
    """Ignore retained local storage without editing the project's ignore policy."""
    path = checked_path(project / ".guidance/.gitignore")
    raw = tx.read(project, ".guidance/.gitignore")
    if raw is None and create:
        save_bytes(path, b"*\n", mode=0o444)
    elif raw != b"*\n":
        raise GuidanceError("local storage ignore policy missing or modified; resolve explicitly")


@contextmanager
def mutation(project, cache=None, *, operation="install"):
    project = project_root(project)
    cache = checked_path(cache or project / ".guidance/cache")
    if cache == project / ".guidance":
        raise GuidanceError("cache cannot share the project writer-lock directory")
    with locked(project / ".guidance", operation=operation):
        storage_ignore(project, create=True)
        tx.recover(project)
        with locked(cache, operation=operation):
            yield project, cache


def connection_state(project, value, expected):
    raw = tx.read(project, native.STATE)
    if raw is None:
        return None
    state = parse_json(raw)
    fields(state, ("schema", "selection", "block", "claude_created"),
           ("agents", "agents_created", "host", "claude_via_agents"))
    if (type(state["schema"]) is not int or state["schema"] != 1 or
            state["selection"] != expected or canonical(state) != raw or
            type(state["claude_created"]) is not bool):
        raise GuidanceError("connection ownership/selection mismatch")
    block = tx.decode(state["block"])
    if "claude" in value["connection"]["clients"]:
        if state.get("claude_via_agents"):
            if block is not None or state["claude_created"] or route_for(value)["route"] != "managed":
                raise GuidanceError("invalid existing Claude import ownership")
        elif block not in (native.block(), native.block(b"\r\n")):
            raise GuidanceError("invalid owned Claude block")
    elif block is not None or state["claude_created"]:
        raise GuidanceError("unexpected Claude ownership")
    return state


def surfaces(selected, route):
    return [name for name in tx.SURFACES
            if (name != native.CLAUDE or "claude" in selected) and
               (name != native.AGENTS or route["route"] == "managed") and
               (name not in (native.CONFIG, native.ROOT_CONFIG) or name == route["config"])]


def retain_lock(project, raw):
    parent = checked_path(project / ".guidance/records")
    make_directory(parent)
    path = checked_path(parent / (digest(raw) + ".json"))
    if path.exists():
        if regular_bytes(path) != raw or tx.file_mode(project, path.relative_to(project)) != 0o400:
            raise GuidanceError("retained selection lock modified or unsafe permissions; preserve evidence")
    else:
        save_bytes(path, raw, mode=0o400)
    return path.relative_to(project).as_posix()


def rendition(project, value, result, *, root=False):
    _, files = verify_snapshot(project / ".guidance/selections" / result["snapshot"], result["snapshot"])
    return native.render(value, result["snapshot"], files, root=root)


def index_sizes(project, value, result, route):
    _, files = verify_snapshot(project / ".guidance/selections" / result["snapshot"], result["snapshot"])
    sizes = native.entry_sizes(value, result["snapshot"], files)
    if route["route"] == "managed":
        sizes["managed_root"] = native.entry_sizes(value, result["snapshot"], files, root=True)
    return sizes


def verify(project, expected, *, fixtures=None, _transaction=False):
    project = project_root(project)
    if not _transaction and tx.read(project, tx.JOURNAL) is not None:
        raise GuidanceError("interrupted transaction; recover before starting clients or verifying")
    value = prep.read_lock(regular_bytes(project / prep.LOCK), expected, fixtures)
    result = prep.verify_prepared(project, expected, fixtures=fixtures)
    if "connection" not in value:
        if tx.read(project, native.STATE) is not None:
            raise GuidanceError("unexpected native ownership for prepared-only selection")
        return dict(result, status="prepared", clients=[])
    storage_ignore(project)
    entry = rendition(project, value, result)
    if digest(entry) != value["connection"]["entry"]:
        raise GuidanceError("generated entry differs from recorded connection identity")
    selected = value["connection"]["clients"]
    route = route_for(value)
    state = connection_state(project, value, expected)
    if state is None:
        if tx.read(project, native.ENTRY) is not None:
            raise GuidanceError("unowned generated entry; inspect ownership")
        if "claude" in selected:
            raw = tx.read(project, native.CLAUDE) or b""
            if native.BEGIN in raw or native.IMPORT in raw:
                raise GuidanceError("unowned Claude registration")
        if route["route"] == "managed":
            if native.BEGIN in (tx.read(project, native.AGENTS) or b""):
                raise GuidanceError("unowned managed AGENTS.md registration")
        elif route["config"] and tx.read(project, route["config"]) == native.configuration():
            raise GuidanceError("unowned OpenCode registration")
        return dict(result, status="removed", clients=selected)
    if tx.read(project, native.ENTRY) != entry:
        raise GuidanceError("generated short entry modified or missing")
    if "claude" in selected:
        block = tx.decode(state["block"])
        if state.get("claude_via_agents"):
            if not native.imports_agents(tx.read(project, native.CLAUDE) or b""):
                raise GuidanceError("existing Claude AGENTS.md import is missing")
        else:
            native.edit_block(tx.read(project, native.CLAUDE) or b"", block, block)
    if route["route"] == "managed":
        root_entry = rendition(project, value, result, root=True)
        block = tx.decode(state.get("agents"))
        if block not in (native.agents_block(root_entry), native.agents_block(root_entry, b"\r\n")):
            raise GuidanceError("managed short entry differs from expected identity")
        native.edit_agents(tx.read(project, native.AGENTS) or b"", block, block)
        if type(state.get("agents_created")) is not bool:
            raise GuidanceError("invalid managed AGENTS.md ownership")
        registration = state.get("host")
        fields(registration, ("path", "identity"))
        if registration["identity"] != route["host"]:
            raise GuidanceError("managed host identity mismatch")
        host.configuration(project, registration["path"], route["host"])
    elif route["config"]:
        if tx.read(project, route["config"]) != native.configuration():
            raise GuidanceError("modified owned OpenCode configuration; resolve explicitly")
        config_available(project, route)
    native.inspect(project, selected, owned=owned_paths(route))
    return dict(result, status="installed", clients=selected)


def preflight(project, selected, expected, fixtures, *, route=None, host_config=None):
    if host_config and "opencode" not in selected:
        raise GuidanceError("--host-config requires selected OpenCode")
    lock_raw = tx.read(project, prep.LOCK)
    old = None
    state = None
    if lock_raw is not None:
        if expected is None:
            raise GuidanceError("existing selection requires independently retained --expected")
        old = prep.read_lock(lock_raw, expected, fixtures)
        verify(project, expected, fixtures=fixtures)
        if "connection" in old:
            state = connection_state(project, old, expected)
            if state is not None and selected != old["connection"]["clients"]:
                raise GuidanceError("client selection change requires explicit removal first")
    elif expected is not None:
        raise GuidanceError("expected selection is missing")
    elif tx.read(project, native.STATE) is not None:
        raise GuidanceError("orphan ownership without selection lock")
    if state is not None and route is not None and route != route_for(old):
        raise GuidanceError("native route change requires explicit removal first")
    if state is not None and host_config and route_for(old)["route"] != "managed":
        raise GuidanceError("native route change requires explicit removal first")
    if route is None:
        route = route_for(old) if state else {"route": "managed" if host_config else "project",
                                             "config": None, "host": None}
        if route["route"] == "project" and "opencode" in selected and not state:
            route["config"] = native.config_slot(project)
    registration = None
    if route["route"] == "managed":
        path = host_config or (state or {}).get("host", {}).get("path")
        registration = host.configuration(project, path, route["host"], launch=True)
        route = dict(route, host=registration["identity"])
    elif "opencode" in selected and host.disabled():
        raise GuidanceError("managed OpenCode requires approved host-controlled --host-config; host settings were not changed")
    native.inspect(project, selected, owned=owned_paths(route))
    before = tx.Preimages(project, surfaces(selected, route))
    if route["route"] == "managed" and "claude" in selected:
        raw = before[native.CLAUDE] or b""
        if native.has_agents_import(raw) and not native.imports_agents(raw) and (state or {}).get("block") is None:
            raise GuidanceError("ambiguous existing Claude AGENTS.md import; resolve explicitly to avoid duplication")
    if state is None:
        if before[native.ENTRY] is not None:
            raise GuidanceError("unowned generated entry collision")
        if "claude" in selected and not (route["route"] == "managed" and native.imports_agents(before[native.CLAUDE] or b"")):
            native.edit_block(before[native.CLAUDE] or b"", None, native.block())
        if route["route"] == "managed":
            native.edit_agents(before[native.AGENTS] or b"", None, b"")
        elif route["config"]:
            if before[route["config"]] is not None:
                raise GuidanceError("owned config slot is occupied; preserve user configuration")
            config_available(project, route)
    if old is not None:
        # A concurrent edit between initial verification and preimage capture
        # must not become an implicitly approved before-image.
        verify(project, expected, fixtures=fixtures)
        if before[prep.LOCK] != canonical(old) or (state is not None and before[native.STATE] != canonical(state)):
            raise GuidanceError("selection/ownership changed during preimage capture; preserve edits")
    return old, state, before, route, registration


def activate(project, value, cache, selected, state, before, fixtures, route, registration, revisions=None):
    result = prep.stage(project, value, cache)
    entry = rendition(project, value, result)
    revisions = value.get("connection", {}).get("revisions", {}) if revisions is None else revisions
    connection = dict(route, schema=1, clients=selected, entry=digest(entry), revisions=revisions)
    if "connection" in value and value["connection"] != connection:
        raise GuidanceError("restored connection differs from independently recorded identity")
    value = dict(value, connection=connection)
    prep.validate_lock(value, fixtures)
    native.inspect(project, selected, owned=owned_paths(route))
    config_available(project, route)
    if registration:
        host.configuration(project, registration["path"], route["host"], launch=True)
    expected = digest(canonical(value))
    new_state = {"schema": 1, "selection": expected, "block": None, "claude_created": False,
                 "agents": None, "agents_created": False, "host": registration, "claude_via_agents": False}
    after = dict(before)
    after[native.ENTRY] = entry
    if route["route"] == "managed":
        raw = before[native.AGENTS] or b""
        old_block = tx.decode(state.get("agents")) if state else None
        newline = b"\r\n" if b"\r\n" in raw else b"\n"
        block = native.agents_block(rendition(project, value, result, root=True), newline)
        after[native.AGENTS] = native.edit_agents(raw, old_block, block)
        new_state["agents"] = tx.encode(block)
        new_state["agents_created"] = state["agents_created"] if state else before[native.AGENTS] is None
    if "claude" in selected:
        raw = before[native.CLAUDE] or b""
        if route["route"] == "managed" and (state or {}).get("claude_via_agents", native.imports_agents(raw)):
            new_state["claude_via_agents"] = True
        else:
            old_block = tx.decode(state["block"]) if state else None
            block = old_block or native.block(b"\r\n" if b"\r\n" in raw else b"\n")
            after[native.CLAUDE] = native.edit_block(raw, old_block, block)
            new_state["block"] = tx.encode(block)
            new_state["claude_created"] = state["claude_created"] if state else before[native.CLAUDE] is None
    if route["config"]:
        after[route["config"]] = native.configuration()
    after[native.STATE] = canonical(new_state)
    after[prep.LOCK] = canonical(value)
    if before[prep.LOCK] is not None:
        retain_lock(project, before[prep.LOCK])
    record = retain_lock(project, after[prep.LOCK])
    # Recheck all preimages, including unchanged surfaces. Lock publication is last.
    changed = tx.apply(project, before.plan(after),
                       lambda: verify(project, expected, fixtures=fixtures, _transaction=True))
    return dict(verify(project, expected, fixtures=fixtures), changed=changed,
                index_size=index_sizes(project, value, result, route),
                restart=selected if changed else [],
                launcher_binding="operation_cwd_pwd_checked" if registration else "not_verified",
                client_loading="not_checked", record=record)


def install(project, request, selected, cache=None, *, expected=None, host_config=None, fixtures=None):
    selected = native.clients(selected)
    # Validate before creating storage or resolving anything.
    prep.request(request, fixtures)
    revisions = {s["id"]: s["revision"] for s in request["sources"] if "revision" in s}
    with mutation(project, cache) as (project, cache):
        old, state, before, route, registration = preflight(project, selected, expected, fixtures, host_config=host_config)
        if state is not None:
            if host_config and route["route"] == "managed" and str(checked_path(host_config)) != state["host"]["path"]:
                raise GuidanceError("host path change requires explicit exact restore, not a no-op install")
            sources = [{k: s[k] for k in ("id", "url", "ref")} for s in old["sources"]]
            bundles = [{k: b[k] for k in ("source", "path", "binding")} for b in old["bundles"]]
            normalized_sources, normalized_bundles = prep.request(request, fixtures)
            normalized_sources = [{k: s[k] for k in ("id", "url", "ref")} for s in normalized_sources]
            order = lambda items: sorted(items, key=lambda item: canonical(item))
            if (order(normalized_sources) != order(sources) or order(normalized_bundles) != order(bundles) or
                    revisions != old["connection"]["revisions"]):
                raise GuidanceError("installed selection differs; use explicit update or remove first")
            result = verify(project, expected, fixtures=fixtures)
            diagnostics = git_source.source_diagnostics(old, old, revisions=revisions, fixtures=fixtures)
            for source in diagnostics:
                source["resolution"] = "retained_not_resolved"
            return dict(result, changed=False, restart=[], sources=diagnostics,
                        index_size=index_sizes(project, old, result, route))
        value = prep.candidate(request, cache, fixtures=fixtures)
        diagnostics = git_source.source_diagnostics(old, value, revisions=revisions, fixtures=fixtures)
        return dict(activate(project, value, cache, selected, state, before, fixtures, route, registration, revisions),
                    sources=diagnostics)


def update(project, expected, cache=None, *, fixtures=None):
    with mutation(project, cache, operation="update") as (project, cache):
        old = prep.read_lock(regular_bytes(project / prep.LOCK), expected, fixtures)
        if "connection" not in old:
            raise GuidanceError("update requires an installed lifecycle selection")
        selected = old["connection"]["clients"]
        _, state, before, route, registration = preflight(project, selected, expected, fixtures)
        if state is None:
            raise GuidanceError("connection removed; restore explicitly before updating")
        request = {"schema": 1,
                   "sources": [{k: s[k] for k in ("id", "url", "ref")} for s in old["sources"]],
                   "bundles": [{k: b[k] for k in ("source", "path", "binding")} for b in old["bundles"]]}
        revisions = old["connection"]["revisions"]
        for source in request["sources"]:
            if source["id"] in revisions:
                source["revision"] = revisions[source["id"]]
        value = prep.candidate(request, cache, fixtures=fixtures)
        diagnostics = git_source.source_diagnostics(old, value, revisions=revisions, fixtures=fixtures)
        return dict(activate(project, value, cache, selected, state, before, fixtures, route, registration, revisions),
                    sources=diagnostics)


def restore(project, raw, expected, cache=None, *, current=None, host_config=None, fixtures=None):
    value = prep.read_lock(raw, expected, fixtures)
    if "connection" not in value:
        raise GuidanceError("prepared-only lock needs the preparation restore command")
    selected = value["connection"]["clients"]
    with mutation(project, cache, operation="restore") as (project, cache):
        if current is None and tx.read(project, prep.LOCK) is not None:
            current = expected
        _, state, before, route, registration = preflight(project, selected, current, fixtures,
                                                          route=route_for(value), host_config=host_config)
        prep.cached(value, cache, fixtures=fixtures)
        return activate(project, value, cache, selected, state, before, fixtures, route, registration)


def remove(project, expected, *, fixtures=None):
    project = project_root(project)
    with locked(project / ".guidance", operation="remove"):
        tx.recover(project)
        result = verify(project, expected, fixtures=fixtures)
        if result["status"] != "installed":
            return dict(result, changed=False, restart=[])
        value = prep.read_lock(regular_bytes(project / prep.LOCK), expected, fixtures)
        state = connection_state(project, value, expected)
        selected = value["connection"]["clients"]
        route = route_for(value)
        before = tx.Preimages(project, surfaces(selected, route))
        # Never adopt a concurrent owned edit as an approved removal preimage.
        verify(project, expected, fixtures=fixtures)
        if before[prep.LOCK] != canonical(value) or before[native.STATE] != canonical(state):
            raise GuidanceError("selection/ownership changed during removal capture; preserve edits")
        after = dict(before)
        after[native.ENTRY] = after[native.STATE] = None
        if route["route"] == "managed":
            raw = native.edit_agents(before[native.AGENTS], tx.decode(state["agents"]), b"")
            after[native.AGENTS] = None if state["agents_created"] and not raw else raw
        if "claude" in selected and not state.get("claude_via_agents"):
            raw = native.edit_block(before[native.CLAUDE], tx.decode(state["block"]), b"")
            after[native.CLAUDE] = None if state["claude_created"] and not raw else raw
        if route["config"]:
            after[route["config"]] = None
        tx.apply(project, before.plan(after),
                 lambda: verify(project, expected, fixtures=fixtures, _transaction=True))
        return dict(verify(project, expected, fixtures=fixtures), changed=True, restart=selected)


def recover(project, cache=None):
    project = project_root(project)
    cache = checked_path(cache or project / ".guidance/cache")
    if cache == project / ".guidance":
        raise GuidanceError("cache cannot share the project writer-lock directory")
    with locked(project / ".guidance", operation="recover", reclaim=True):
        with locked(cache, operation="recover", reclaim=True):
            return {"recovered": tx.recover(project), "restart": "restart selected clients after recovery"}
