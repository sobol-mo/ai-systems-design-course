"""Readable course artifacts do not replace raw transport evidence."""
import json
import pytest
from types import SimpleNamespace

from learning_project.lab07 import ACTION_SCHEMA, run_first_action


def reply(value):
    return SimpleNamespace(returncode=0, stdout=json.dumps({
        'status': 'SUCCESS', 'response': json.dumps(value)}), stderr='')


def test_first_request_contains_structured_schema_and_preserves_transport(tmp_path):
    calls = []
    raw = reply({'operation': 'retrieval operation', 'arguments': {
        'text query': 'query embedding vector comparison', 'collection': 'S-AGENT/v1'}})
    def provider(command, **kwargs):
        calls.append(command)
        return raw
    run_first_action(model_id='test', output_dir=tmp_path/'first', runner=provider)
    request = json.loads((tmp_path/'first/request.json').read_text(encoding='utf-8'))
    assert request['output contract']['schema'] == ACTION_SCHEMA
    assert isinstance(request['output contract']['instruction'], str)
    assert json.loads((tmp_path/'first/provider-response.json').read_text(encoding='utf-8'))['stdout'] == raw.stdout
    command = calls[0]
    sent = json.loads(command[command.index('--print') + 1].split('\n\n', 1)[1])
    assert sent == request


def test_continuations_keep_schemas_and_progress_structured(tmp_path):
    from learning_project.lab07_loop import continue_adaptive
    from learning_project.lab07_comparison import run_fixed
    from learning_project.lab06_generation import OUTCOME_SCHEMA
    read = {'operation': 'retrieval operation', 'arguments': {
        'text query': 'query embedding vector comparison', 'collection': 'S-AGENT/v1'}}
    first = tmp_path/'first'
    run_first_action(model_id='test', output_dir=first, runner=lambda *a, **kw: reply(read))
    outcome = {'outcome_type': 'refusal', 'blocking_condition': 'insufficient supplied source evidence'}
    replies = iter([{'operation': 'model-backed prerequisite-explanation operation', 'arguments': {}},
                    outcome, {'operation': 'stop', 'arguments': {}}])
    continue_adaptive(first_action_dir=first, model_id='test', output_dir=tmp_path/'adaptive',
                      runner=lambda *a, **kw: reply(next(replies)))
    run_fixed(first_action_dir=first, model_id='test', output_dir=tmp_path/'fixed',
              runner=lambda *a, **kw: reply(outcome))
    for relative, schema in [('adaptive/decision-1/request.json', ACTION_SCHEMA),
                             ('adaptive/decision-1/generation/request.json', OUTCOME_SCHEMA),
                             ('fixed/generation/request.json', OUTCOME_SCHEMA)]:
        request = json.loads((tmp_path/relative).read_text(encoding='utf-8'))
        assert request['output contract']['schema'] == schema
    feedback = json.loads((tmp_path/'adaptive/decision-2/request.json').read_text(encoding='utf-8'))
    assert feedback['task instruction']['task-progress data'] == {'generation return': outcome}
    assert json.dumps(outcome) not in feedback['task instruction']['instruction']


def test_cli_prints_windows_paths_without_json_escaping(monkeypatch, capsys):
    from learning_project.cli import main
    import learning_project.lab07 as lab07
    result = {'status': 'candidates returned', 'trace': r'reports\lab07\first-read\trace.json'}
    monkeypatch.setattr(lab07, 'run_first_action', lambda **kw: result)
    args = ['lab07', 'run-first-action', '--model', 'test', '--output-dir', 'reports/lab07/first-read']
    assert main(args) == 0
    assert capsys.readouterr().out == ('status: candidates returned\n'
                                      'trace: reports\\lab07\\first-read\\trace.json\n')
    assert main(args + ['--json']) == 0
    assert json.loads(capsys.readouterr().out) == result


@pytest.mark.parametrize('legacy', [False, True])
def test_complete_capture_replays_without_mutating_old_or_new_artifacts(tmp_path, legacy):
    from learning_project.lab07_loop import continue_adaptive, _validated_first_read
    from learning_project.lab07_comparison import run_fixed
    from learning_project.lab07_boundaries import run_boundary_checks
    from learning_project.lab07_reporting import _verify_domain
    from learning_project.workflow import WorkflowError
    first = tmp_path/'first-read'
    read = {'operation': 'retrieval operation', 'arguments': {
        'text query': 'query embedding vector comparison', 'collection': 'S-AGENT/v1'}}
    run_first_action(model_id='test', output_dir=first, runner=lambda *a, **kw: reply(read),
                     _legacy_request=legacy)
    outcome = {'outcome_type': 'refusal', 'blocking_condition': 'insufficient supplied source evidence'}
    replies = iter([{'operation': 'model-backed prerequisite-explanation operation', 'arguments': {}},
                    outcome, {'operation': 'stop', 'arguments': {}}])
    continue_adaptive(first_action_dir=first, model_id='test', output_dir=tmp_path/'adaptive',
                      runner=lambda *a, **kw: reply(next(replies)))
    run_fixed(first_action_dir=first, model_id='test', output_dir=tmp_path/'fixed',
              runner=lambda *a, **kw: reply(outcome))
    run_boundary_checks(first_action_dir=first, output_dir=tmp_path/'boundaries')
    before = {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    _verify_domain(tmp_path)
    assert {p: p.read_bytes() for p in tmp_path.rglob('*.json')} == before
    request_path = tmp_path/'adaptive/decision-1/request.json'
    request = json.loads(request_path.read_text(encoding='utf-8'))
    assert isinstance(request['output contract'], str if legacy else dict)
    # Compatibility must not weaken exact-request checks.
    request_path.write_text(json.dumps({**request, 'unrecorded change': True}), encoding='utf-8')
    with pytest.raises(WorkflowError, match='differs from deterministic replay'):
        _verify_domain(tmp_path)
    first_request_path = first/'request.json'
    first_request = json.loads(first_request_path.read_text(encoding='utf-8'))
    first_request['task instruction'] += ' Changed task.'
    first_request_path.write_text(json.dumps(first_request), encoding='utf-8')
    with pytest.raises(WorkflowError, match='differs from replay'):
        _validated_first_read(first)


@pytest.mark.parametrize('command,module,function,arguments', [
    ('run-first-action', 'lab07', 'run_first_action', ['--model', 'test', '--output-dir', 'out']),
    ('continue-adaptive', 'lab07_loop', 'continue_adaptive',
     ['--model', 'test', '--first-action-dir', 'first', '--output-dir', 'out']),
    ('run-fixed', 'lab07_comparison', 'run_fixed',
     ['--model', 'test', '--first-action-dir', 'first', '--output-dir', 'out']),
    ('check-boundaries', 'lab07_boundaries', 'run_boundary_checks',
     ['--first-action-dir', 'first', '--output-dir', 'out']),
    ('init-report', 'lab07_reporting', 'init_report', ['--report-dir', 'out']),
    ('validate-report', 'lab07_reporting', 'validate_report', ['--report-dir', 'out']),
    ('verify', 'lab07_reporting', 'verify', ['--report-dir', 'out', '--final-commit', 'a'*40]),
])
def test_every_lab07_command_supports_human_and_json_output(monkeypatch, capsys, command, module, function, arguments):
    import importlib
    from learning_project.cli import main
    result = {'status': 'passed', 'outcome': 'passed', 'metadata': r'reports\lab07\run-metadata.json'}
    monkeypatch.setattr(importlib.import_module('learning_project.' + module), function, lambda **kw: result)
    args = ['lab07', command, *arguments]
    assert main(args) == 0
    output = capsys.readouterr().out
    assert 'status: passed\n' in output
    assert 'metadata: ' + result['metadata'] + '\n' in output
    assert main(args + ['--json']) == 0
    assert json.loads(capsys.readouterr().out) == result
