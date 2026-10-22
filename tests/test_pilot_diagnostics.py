"""Neutral diagnostics and bounded native registration inspection."""

from unittest.mock import patch

from agent_guides_cli import git_source, lifecycle, native, preparation
from agent_guides_cli.integrity import GuidanceError, canonical
from fixtures import GitFixture


class PilotDiagnosticsTests(GitFixture):
    def candidate(self):
        return preparation.candidate(self.request, self.cache, fixtures=self.fixtures)

    def test_lifecycle_diagnostics_and_noop_install_never_resolve(self):
        result = lifecycle.install(self.project, self.request, ["claude"], self.cache, fixtures=self.fixtures)
        self.assertTrue(all(s["change"] == "new" for s in result["sources"]))
        self.assertEqual(result["index_size"]["total"], len((self.project / native.ENTRY).read_bytes()))
        with patch.object(git_source, "resolve", side_effect=AssertionError("no-op resolved")):
            again = lifecycle.install(self.project, self.request, ["claude"], self.cache,
                                      expected=result["selection"], fixtures=self.fixtures)
        self.assertFalse(again["changed"])
        self.assertEqual(again["index_size"], result["index_size"])
        self.assertTrue(all(s["resolution"] == "retained_not_resolved" for s in again["sources"]))
        updated = lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.fixtures)
        self.assertTrue(all(s["change"] == "unchanged" for s in updated["sources"]))
        self.assertEqual(updated["index_size"], result["index_size"])

    def test_path_aliases_are_real_competing_registrations(self):
        paths = ("./.guidance/./entry.md", ".guidance//entry.md", ".GUIDANCE/ENTRY.md",
                 str(self.project / ".guidance/entry.md"))
        for path in paths:
            with self.subTest(path=path):
                with self.assertRaises(GuidanceError):
                    self.inspect_file("AGENTS.md", ("@" + path).encode(), ["opencode"])
                with self.assertRaises(GuidanceError):
                    self.inspect_file("opencode.jsonc", canonical({"instructions": [path]}), ["opencode"])
        raw = b"@./.guidance/./entry.md\n"
        with self.assertRaises(GuidanceError):
            native.edit_block(raw, None, native.block())
        with self.assertRaises(GuidanceError):
            native.edit_agents(raw, None, b"")
        with self.assertRaises(GuidanceError):
            native.edit_block(native.block() + raw, native.block(), native.block())

    def test_source_observations_never_resolve_or_change_identity(self):
        old = self.candidate()
        self.write("alpha", "one/NOTICE", b"changed\n")
        moved = self.commit("alpha")
        new = self.candidate()
        before = canonical(new)
        with patch.object(git_source, "resolve", side_effect=AssertionError("diagnostic resolved")):
            rows = git_source.source_diagnostics(old, new, revisions={"beta": self.commits["beta"]})
        self.assertEqual([r["change"] for r in rows], ["changed", "unchanged"])
        self.assertEqual(rows[0]["old_commit"], self.commits["alpha"])
        self.assertEqual(rows[0]["new_commit"], moved)
        self.assertFalse(rows[0]["pinned"])
        self.assertTrue(rows[1]["pinned"])
        self.assertEqual(rows[0]["transport"], "fixture")
        self.assertIsNone(rows[0]["mirror_refresh"])
        self.assertEqual(canonical(new), before)
        self.assertTrue(all(r["change"] == "new" for r in git_source.source_diagnostics(None, new)))

    def test_exact_rendered_sizes_reconcile_unicode_links_and_repeated_scopes(self):
        self.write("alpha", "one/README.md", "# Résumé 🧪\n\n[Topic](detail/topic.md)\n".encode())
        self.commit("alpha")
        self.request["bundles"].append({"source": "alpha", "path": "one", "binding": "other"})
        value = self.candidate()
        files = preparation.selection_files(value, self.cache / "bundles")
        for root in (False, True):
            with self.subTest(root=root):
                report = native.entry_sizes(value, "a" * 64, files, root=root)
                raw = native.render(value, "a" * 64, files, root=root)
                self.assertEqual(report["total"], len(raw))
                self.assertEqual(report["total"], report["shared_overhead"] +
                                 sum(b["rendered_bytes"] for b in report["bundles"]))
                self.assertEqual(len(report["bundles"]), 4)
                shared, sections = native.render_parts(value, "a" * 64, files, root=root)
                self.assertEqual(shared + b"".join(raw for _, raw in sections), raw)
                self.assertEqual(report["token_count"], "not_measured")
        self.assertGreater(native.entry_sizes(value, "a" * 64, files, root=True)["total"],
                           native.entry_sizes(value, "a" * 64, files)["total"])

    def inspect_file(self, name, raw, selected=("claude", "opencode")):
        path = self.project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        native.inspect(self.project, selected)

    def test_markdown_prose_and_examples_are_not_registrations(self):
        raw = (b"Old flutter-agent-guidelines delivery used .guidance/entry.md.\n"
               b"`@./flutter-agent-guidelines/README.md` is an example.\n"
               b"```markdown\n@./flutter-agent-guidelines/README.md\n```\n"
               b"[Documentation](flutter-agent-guidelines/README.md)\n")
        for name in ("AGENTS.md", "CLAUDE.md"):
            self.inspect_file(name, raw)
        native.edit_block(raw, None, native.block())
        native.edit_agents(raw, None, b"")

    def test_real_markdown_imports_rejected_for_each_selected_client(self):
        for name, selected in (("AGENTS.md", ["claude"]), ("CLAUDE.md", ["claude"]),
                               ("AGENTS.md", ["opencode"])):
            for raw in (b"@./flutter-agent-guidelines/README.md\n",
                        b'Follow @"./flutter_agent_guidelines/README.md" now.\n',
                        b"@./.guidance/entry.md\n"):
                with self.subTest(name=name, raw=raw), self.assertRaises(GuidanceError):
                    self.inspect_file(name, raw, selected)

    def test_jsonc_registration_fields_not_comments_or_descriptions(self):
        raw = b'''{
          // flutter-agent-guidelines and .guidance/entry.md are historical
          "description": "flutter-agent-guidelines",
          "plugin": ["unrelated-guard"],
          "enabledPlugins": {"flutter-agent-guidelines@legacy": false},
          "instructions": ["local-policy.md"],
          "hooks": {"PreToolUse": [{"matcher": "flutter-agent-guidelines", "hooks": [{"type": "command", "command": "guard"}]}]},
        }'''
        self.inspect_file("opencode.jsonc", raw)
        for field, payload in (("plugin", ["flutter-agent-guidelines"]),
                               ("instructions", [".guidance/entry.md"]),
                               ("hooks", {"PreToolUse": [{"command": "python -m flutter_agent_guidelines"}]}),
                               ("enabledPlugins", {"flutter-agent-guidelines@legacy": True})):
            with self.subTest(field=field), self.assertRaises(GuidanceError):
                self.inspect_file("opencode.jsonc", canonical({field: payload}))
        (self.project / "opencode.jsonc").unlink()
        with self.assertRaises(GuidanceError):
            self.inspect_file(".claude/settings.json", canonical({"hooks": {
                "PreToolUse": [{"command": "flutter_agent_guidelines"}]}}), ["claude"])

    def test_jsonc_preserves_strings_and_fails_closed(self):
        self.assertEqual(native.registration_strings(
            b'{/* note */ "instructions": ["https://example.org/a,}",],}'),
            ["https://example.org/a,}"])
        for raw in (b"{broken}", b"[]"):
            with self.assertRaises(GuidanceError):
                native.registration_strings(raw)

    def test_managed_import_reuse_and_ambiguity(self):
        self.assertTrue(native.imports_agents(b"@./AGENTS.md\n"))
        self.assertTrue(native.imports_agents(b"Follow @AGENTS.md now.\n"))
        for raw in (b"@AGENTS.md\n@./AGENTS.md\n", b"@./nested/AGENTS.md\n"):
            self.assertTrue(native.has_agents_import(raw))
            self.assertFalse(native.imports_agents(raw))
        for raw in (b"AGENTS.md and @ are prose", b"`@AGENTS.md`", b"```\n@AGENTS.md\n```"):
            self.assertFalse(native.has_agents_import(raw))
            self.assertFalse(native.imports_agents(raw))

    def test_ownership_markers_and_unselected_settings_stay_protected(self):
        with self.assertRaises(GuidanceError):
            self.inspect_file("AGENTS.md", native.BEGIN, ["claude"])
        (self.project / "AGENTS.md").unlink()
        self.inspect_file(".claude/settings.json", b"not JSON", ["opencode"])
        with self.assertRaises(GuidanceError):
            native.edit_agents(native.BEGIN, None, b"")
        with self.assertRaises(GuidanceError):
            native.edit_block(b"@./.guidance/entry.md", None, native.block())
