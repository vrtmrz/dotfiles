"""Exercise installation in isolated home and configuration directories."""

import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='dotfiles-install-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repository = self.root / 'repository'
        self.home_directory = self.root / 'home'
        self.configuration = self.root / 'configuration'
        self.home_directory.mkdir()
        self.configuration.mkdir()
        (self.repository / 'codex' / 'agents').mkdir(parents=True)
        shutil.copy2(Path(__file__).resolve().parents[1] / 'install.sh', self.repository / 'install.sh')
        shutil.copy2(Path(__file__).resolve().parents[1] / 'install4agy.sh', self.repository / 'install4agy.sh')
        self.guidance = self.repository / 'codex' / 'AGENTS.md'
        self.guidance.write_text('# Public guidance\n')
        self.agent = self.repository / 'codex' / 'agents' / 'luna_lookup.toml'
        self.agent.write_text('name = "luna_lookup"\nmodel_reasoning_effort = "medium"\n')
        self.environment = dict(os.environ)
        self.environment.update(HOME=str(self.home_directory), CODEX_HOME=str(self.configuration))

    def install(self, script='install.sh', extra_env=None):
        environment = dict(self.environment)
        if extra_env:
            environment.update(extra_env)
        result = subprocess.run(['bash', str(self.repository / script)], env=environment,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def add_public_detail(self, name='architecture.md', content='# Public detail\n'):
        detail = self.repository / 'codex' / 'guidance' / name
        detail.parent.mkdir(parents=True, exist_ok=True)
        detail.write_text(content)
        return detail

    def test_installs_regular_agent_files_and_links_public_guidance(self):
        self.install()
        target = self.configuration / 'agents' / self.agent.name
        self.assertTrue(target.is_file(), 'The public agent definition was not installed')
        self.assertFalse(target.is_symlink())
        self.assertEqual(target.read_bytes(), self.agent.read_bytes())
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
        self.assertEqual((self.configuration / 'AGENTS.md').resolve(), self.guidance)

    def test_existing_identical_agent_receives_private_permissions(self):
        target = self.configuration / 'agents' / self.agent.name
        target.parent.mkdir()
        target.write_bytes(self.agent.read_bytes())
        target.chmod(0o644)

        self.install()

        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
        self.assertEqual(target.read_bytes(), self.agent.read_bytes())
        self.assertEqual(list(target.parent.glob('*.backup.*')), [])

    def test_combines_the_explicit_device_supplement_after_private_guidance(self):
        private = self.configuration / 'AGENTS.private.md'
        private.write_text('# Private guidance\n')
        device = self.configuration / 'AGENTS.device.md'
        device.write_text('# Explicit device guidance\n')

        self.install()

        combined = (self.configuration / 'AGENTS.md').read_text()
        self.assertTrue(combined.endswith(private.read_text() + '\n\n' + device.read_text()))

    def test_preserves_a_different_definition_and_unrelated_agent(self):
        agents = self.configuration / 'agents'
        agents.mkdir()
        target = agents / self.agent.name
        target.write_text('original definition\n')
        unrelated = agents / 'personal.toml'
        unrelated.write_text('personal definition\n')
        self.install()
        backups = list(agents.glob(self.agent.name + '.backup.*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'original definition\n')
        self.assertEqual(target.read_bytes(), self.agent.read_bytes())
        self.assertEqual(unrelated.read_text(), 'personal definition\n')

    def test_preserves_a_legacy_symlink_and_its_source(self):
        agents = self.configuration / 'agents'
        agents.mkdir()
        legacy = self.root / 'legacy.toml'
        legacy.write_text('legacy definition\n')
        target = agents / self.agent.name
        target.symlink_to(legacy)
        self.install()
        self.assertFalse(target.is_symlink())
        self.assertEqual(target.read_bytes(), self.agent.read_bytes())
        self.assertEqual(legacy.read_text(), 'legacy definition\n')
        backups = list(agents.glob(self.agent.name + '.backup.*'))
        self.assertEqual(len(backups), 1)
        self.assertTrue(backups[0].is_symlink())
        self.assertEqual(backups[0].resolve(), legacy)

    def test_repeated_installation_does_not_replace_identical_files(self):
        self.install()
        target = self.configuration / 'agents' / self.agent.name
        self.assertTrue(target.exists(), 'The public agent definition was not installed')
        before = target.stat()
        self.install()
        after = target.stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.assertEqual(list(target.parent.glob('*.backup.*')), [])

    def test_installs_agents_even_when_combined_guidance_is_unchanged(self):
        private = self.configuration / 'AGENTS.private.md'
        private.write_text('# Private guidance\n')
        self.install()
        combined = self.configuration / 'AGENTS.md'
        expected = ('<!-- Generated by dotfiles/install.sh from public and private guidance. -->\n\n'
                    + self.guidance.read_text() + '\n\n' + private.read_text())
        self.assertEqual(combined.read_text(), expected)
        before = combined.stat()
        target = self.configuration / 'agents' / self.agent.name
        if target.exists():
            target.unlink()
        self.install()
        self.assertTrue(target.is_file(), 'The unchanged-guidance path skipped agent installation')
        self.assertEqual(combined.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(combined.read_text(), expected)

    def test_preserves_existing_guidance_and_installs_skills(self):
        target = self.configuration / 'AGENTS.md'
        target.write_text('# Existing guidance\n')
        skill = self.repository / 'codex' / 'skills' / 'example'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('# Example\n')
        self.install()
        backups = list(self.configuration.glob('AGENTS.md.backup.*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), '# Existing guidance\n')
        self.assertEqual(target.resolve(), self.guidance)
        self.assertEqual((self.home_directory / '.agents' / 'skills' / 'example').resolve(), skill)

    def test_installs_public_detail_as_a_regular_file(self):
        detail = self.add_public_detail(content='# Public detail only\n')

        self.install()

        target = self.configuration / 'guidance' / 'public' / detail.name
        self.assertTrue(target.is_file(), 'The public detail file was not installed')
        self.assertFalse(target.is_symlink())
        self.assertEqual(target.read_bytes(), detail.read_bytes())
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
        self.assertNotIn('Public detail only', (self.configuration / 'AGENTS.md').read_text())

    def test_preserves_public_detail_replacement_and_other_namespace_files(self):
        detail = self.add_public_detail(content='# Current public detail\n')
        public_guidance = self.configuration / 'guidance' / 'public'
        private_guidance = self.configuration / 'guidance' / 'private'
        public_guidance.mkdir(parents=True)
        old_target = public_guidance / detail.name
        old_target.write_text('# Previous public detail\n')
        unrelated = public_guidance / 'personal.md'
        unrelated.write_text('# Personal detail\n')
        private_detail = private_guidance / 'local.md'
        private_detail.parent.mkdir(parents=True)
        private_detail.write_text('# Private detail\n')

        self.install()

        backups = list(public_guidance.glob(detail.name + '.backup.*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), '# Previous public detail\n')
        self.assertEqual(old_target.read_bytes(), detail.read_bytes())
        self.assertFalse(old_target.is_symlink())
        self.assertEqual(stat.S_IMODE(old_target.stat().st_mode), 0o600)
        self.assertEqual(unrelated.read_text(), '# Personal detail\n')
        self.assertEqual(private_detail.read_text(), '# Private detail\n')

    def test_repeated_installation_keeps_identical_public_detail(self):
        detail = self.add_public_detail()
        self.install()
        target = self.configuration / 'guidance' / 'public' / detail.name
        self.assertTrue(target.is_file(), 'The public detail file was not installed')
        before = target.stat()

        self.install()

        after = target.stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.assertEqual(list(target.parent.glob('*.backup.*')), [])

    def test_updates_public_details_when_combined_guidance_is_unchanged(self):
        detail = self.add_public_detail(content='# First detail version\n')
        initial_content = '# First detail version\n'
        (self.configuration / 'AGENTS.private.md').write_text('# Private guidance\n')
        self.install()
        target = self.configuration / 'guidance' / 'public' / detail.name
        combined = self.configuration / 'AGENTS.md'
        combined_before = combined.stat()
        detail.write_text('# Updated detail version\n')

        self.install()

        self.assertTrue(target.is_file(), 'The public detail file was not installed')
        self.assertEqual(target.read_text(), '# Updated detail version\n')
        self.assertEqual(combined.stat().st_mtime_ns, combined_before.st_mtime_ns)
        backups = list(target.parent.glob(detail.name + '.backup.*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), initial_content)

    def test_install4agy_filters_sections_expands_placeholders_and_skips_toml_agents(self):
        self.guidance.write_text(
            'Root: {{GUIDANCE_ROOT}}\n'
            '<!-- @only: codex -->\nCodex only section\n<!-- @end -->\n'
            '<!-- @only: agy -->\nAgy only section\n<!-- @end -->\n'
            'Shared line\n'
        )
        self.add_public_detail('codex_only.md', '<!-- @targets: codex -->\n# Codex only\n')
        self.add_public_detail('shared.md', '# Shared\nSkills: {{SKILLS_ROOT}}\n')
        codex_skill = self.repository / 'codex' / 'skills' / 'codex-only'
        codex_skill.mkdir(parents=True)
        (codex_skill / 'SKILL.md').write_text('---\nname: codex-only\n---\n<!-- @targets: codex -->\n')
        shared_skill = self.repository / 'codex' / 'skills' / 'shared-skill'
        shared_skill.mkdir(parents=True)
        (shared_skill / 'SKILL.md').write_text('---\nname: shared-skill\n---\n')

        agy_config = self.home_directory / '.gemini' / 'config'
        agy_config.mkdir(parents=True)
        legacy_link = agy_config / 'AGENTS.md'
        legacy_link.symlink_to(self.configuration / 'AGENTS.md')
        (agy_config / 'AGENTS.private.md').write_text('# Agy private\n')

        self.install('install4agy.sh')

        installed = (agy_config / 'AGENTS.md').read_text()
        self.assertFalse((agy_config / 'AGENTS.md').is_symlink())
        self.assertEqual(len(list(agy_config.glob('AGENTS.md.backup.*'))), 1)
        self.assertIn('Root: ~/.gemini/config/guidance', installed)
        self.assertIn('Agy only section', installed)
        self.assertNotIn('Codex only section', installed)
        self.assertNotIn('<!-- @only:', installed)
        self.assertFalse((agy_config / 'agents').exists())
        public_guidance = agy_config / 'guidance' / 'public'
        self.assertFalse((public_guidance / 'codex_only.md').exists())
        self.assertEqual((public_guidance / 'shared.md').read_text(), '# Shared\nSkills: ~/.gemini/skills\n')
        skills_dir = self.home_directory / '.gemini' / 'skills'
        self.assertFalse((skills_dir / 'codex-only').exists())
        self.assertEqual((skills_dir / 'shared-skill').resolve(), shared_skill)

    def test_codex_install_renders_directives_and_rejects_unclosed_blocks(self):
        self.guidance.write_text(
            'Root: {{GUIDANCE_ROOT}}\n'
            '<!-- @only: codex -->\nCodex section\n<!-- @end -->\n'
            '<!-- @only: agy -->\nAgy section\n<!-- @end -->\n'
        )
        self.install()
        target = self.configuration / 'AGENTS.md'
        self.assertFalse(target.is_symlink())
        self.assertEqual(target.read_text(), 'Root: ${CODEX_HOME:-$HOME/.codex}/guidance\nCodex section\n')

        self.guidance.write_text('<!-- @only: codex -->\nUnclosed\n')
        failed = subprocess.run(['bash', str(self.repository / 'install.sh')], env=self.environment,
                                text=True, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(target.read_text(), 'Root: ${CODEX_HOME:-$HOME/.codex}/guidance\nCodex section\n')

    def test_renders_templated_skills_per_target_idempotently(self):
        templated = self.repository / 'codex' / 'skills' / 'templated-skill'
        (templated / 'scripts').mkdir(parents=True)
        (templated / 'agents').mkdir()
        (templated / 'references').mkdir()
        (templated / 'SKILL.md').write_text(
            '---\nname: templated-skill\ndescription: Baked skill.\n---\n'
            'Dir: {{SKILLS_ROOT}}/templated-skill\n'
            'Exec: python3 {{SKILLS_SHELL_ROOT}}/templated-skill/scripts/run.py\n'
            '<!-- @only: codex -->\nCodex tip\n<!-- @end -->\n'
            '<!-- @only: agy -->\nAgy tip\n<!-- @end -->\n'
        )
        (templated / 'references' / 'guide.md').write_text('Guidance: {{GUIDANCE_ROOT}}\n')
        (templated / 'agents' / 'openai.yaml').write_text('interface:\n  display_name: "Templated"\n')
        runner = templated / 'scripts' / 'run.py'
        runner.write_text('#!/usr/bin/env python3\nprint("ok")\n')
        runner.chmod(0o755)

        legacy_codex = self.home_directory / '.agents' / 'skills'
        legacy_codex.mkdir(parents=True)
        (legacy_codex / 'templated-skill').symlink_to(templated)

        self.install('install.sh')
        codex_installed = legacy_codex / 'templated-skill'
        self.assertFalse(codex_installed.is_symlink())
        self.assertEqual(list(legacy_codex.glob('*.backup.*')), [])
        codex_backups = list((self.configuration / 'backups' / 'skills').glob('templated-skill.backup.*'))
        self.assertEqual(len(codex_backups), 1)
        self.assertTrue(codex_backups[0].is_symlink())
        self.assertEqual(codex_backups[0].resolve(), templated)
        self.assertEqual(
            (codex_installed / 'SKILL.md').read_text(),
            '---\nname: templated-skill\ndescription: Baked skill.\n---\n'
            'Dir: ~/.agents/skills/templated-skill\n'
            'Exec: python3 $HOME/.agents/skills/templated-skill/scripts/run.py\n'
            'Codex tip\n'
        )
        self.assertEqual((codex_installed / 'references' / 'guide.md').read_text(),
                         'Guidance: ${CODEX_HOME:-$HOME/.codex}/guidance\n')
        self.assertTrue((codex_installed / 'agents' / 'openai.yaml').is_file())
        self.assertTrue(os.access(codex_installed / 'scripts' / 'run.py', os.X_OK))

        self.install('install.sh')
        self.assertEqual(len(list((self.configuration / 'backups' / 'skills').glob('templated-skill.backup.*'))), 1)

        legacy_agy = self.home_directory / '.gemini' / 'skills'
        legacy_agy.mkdir(parents=True)
        (legacy_agy / 'templated-skill').symlink_to(templated)

        self.install('install4agy.sh')
        agy_installed = legacy_agy / 'templated-skill'
        self.assertFalse(agy_installed.is_symlink())
        self.assertEqual(list(legacy_agy.glob('*.backup.*')), [])
        agy_backups = list((self.home_directory / '.gemini' / 'config' / 'backups' / 'skills').glob(
            'templated-skill.backup.*'
        ))
        self.assertEqual(len(agy_backups), 1)
        self.assertEqual(
            (agy_installed / 'SKILL.md').read_text(),
            '---\nname: templated-skill\ndescription: Baked skill.\n---\n'
            'Dir: ~/.gemini/skills/templated-skill\n'
            'Exec: python3 $HOME/.gemini/skills/templated-skill/scripts/run.py\n'
            'Agy tip\n'
        )
        self.assertEqual((agy_installed / 'references' / 'guide.md').read_text(),
                         'Guidance: ~/.gemini/config/guidance\n')
        self.assertFalse((agy_installed / 'agents').exists())
        self.assertTrue(os.access(agy_installed / 'scripts' / 'run.py', os.X_OK))

        self.install('install4agy.sh')
        self.assertEqual(list(legacy_agy.glob('*.backup.*')), [])

    def test_rendered_skill_shell_command_handles_spaces_in_home(self):
        spaced_home = self.root / 'home with spaces'
        spaced_home.mkdir()
        skill = self.repository / 'codex' / 'skills' / 'labnote'
        (skill / 'scripts').mkdir(parents=True)
        (skill / 'SKILL.md').write_text(
            '---\nname: labnote\ndescription: LabNote helper.\n---\n'
            '```sh\npython3 "{{SKILLS_SHELL_ROOT}}/labnote/scripts/labnote.py" ok\n```\n'
        )
        (skill / 'scripts' / 'labnote.py').write_text(
            'import sys\nprint("ARGS:" + "|".join(sys.argv[1:]))\n'
        )
        env = dict(self.environment)
        env.update(HOME=str(spaced_home), CODEX_HOME=str(spaced_home / '.codex'))
        self.install('install.sh', extra_env=env)
        skill_md = (spaced_home / '.agents' / 'skills' / 'labnote' / 'SKILL.md').read_text()
        cmd_line = [line for line in skill_md.splitlines() if 'labnote.py' in line][0]
        self.assertEqual(cmd_line, 'python3 "$HOME/.agents/skills/labnote/scripts/labnote.py" ok')
        run = subprocess.run(['sh', '-c', cmd_line], env=env, text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.strip(), 'ARGS:ok')


if __name__ == '__main__':
    unittest.main()
