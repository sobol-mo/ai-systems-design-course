"""Generation evidence is distinct from semantic judging."""
import json
import unittest

import test_lab06_graph_queries as queries
from learning_project import lab06_generation as generation


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.query = queries.GraphQueryTests()
        self.query.setUp()
        self.addCleanup(self.query.doCleanups)
        self.root = self.query.root
        self.protocol = self.root / 'protocol.json'

    def prepare(self):
        return generation.prepare_generation(collection=self.query.collection,
            graph_path=self.query.graph, model_id='gemini-3.8-flash-low', output=self.protocol)

    def test_freeze_two_development_cases_with_identical_generator_and_no_reference_leak(self):
        self.prepare()
        p = json.loads(self.protocol.read_text())
        self.assertEqual(p['generator']['model_id'], 'gemini-3.8-flash-low')
        self.assertEqual(p['attempts_per_position'], 1)
        self.assertEqual(len(p['cases']), 2)
        for case in p['cases']:
            self.assertEqual(case['membership'], 'development')
            self.assertEqual(len(case['reference']['required_connections']), 2)
            requests = list(case['requests'].values())
            for request in requests:
                self.assertEqual(set(request), {'task instruction', 'supplied source evidence', 'output contract'})
                self.assertNotIn('reference', request)
            self.assertEqual(requests[0]['task instruction'], requests[1]['task instruction'])
            self.assertEqual(requests[0]['output contract'], requests[1]['output contract'])
        self.assertEqual(p['cases'][1]['requests']['without graph expansion'],
                         p['cases'][1]['requests']['with graph expansion'])
        self.assertNotEqual(p['cases'][0]['requests']['without graph expansion'],
                            p['cases'][0]['requests']['with graph expansion'])

    def test_run_preserves_full_transport_and_extracts_one_outcome(self):
        from types import SimpleNamespace
        self.prepare()
        calls = []
        outcome = {'outcome_type': 'refusal', 'blocking_condition': 'insufficient supplied source evidence'}
        stdout = json.dumps({'status': 'SUCCESS', 'response': json.dumps(outcome), 'usage': {'tokens': 123}})
        def runner(command, **kwargs):
            calls.append(command)
            return SimpleNamespace(returncode=0, stdout=stdout, stderr='diagnostic')
        paths = generation.run_generation(protocol_path=self.protocol, case_id='EC-06-1-v1',
            role='without graph expansion', output_dir=self.root / 'run', runner=runner,
            collection=self.query.collection, graph_path=self.query.graph)
        self.assertEqual(json.loads(paths['outcome'].read_text()), outcome)
        raw = json.loads(paths['response'].read_text())
        self.assertEqual(raw['stdout'], stdout)
        self.assertEqual(raw['stderr'], 'diagnostic')
        self.assertIn('--json-schema', calls[0])
        prompt = calls[0][calls[0].index('--print') + 1]
        self.assertNotIn('required_connections', prompt)
        self.assertNotIn('graph_digest', prompt)
        metadata = json.loads(paths['metadata'].read_text())
        self.assertEqual(metadata['status'], 'observed')
        self.assertEqual(metadata['semantic_judgment'], 'not performed')
        self.assertEqual(metadata['latency_boundary'], 'AGY process invocation through process completion only')

    def test_collision_on_each_sibling_including_links_stops_before_provider(self):
        from learning_project.workflow import WorkflowError
        self.prepare()
        for filename in ['attempt.json', 'provider-response.json', 'outcome.json', 'run-metadata.json']:
            for kind in ['regular', 'dangling', 'existing-target']:
                with self.subTest(filename=filename, kind=kind):
                    folder = self.root / (filename + kind)
                    folder.mkdir()
                    path = folder / filename
                    target = self.root / ('outside-' + filename + kind)
                    if kind == 'regular':
                        path.write_text('unchanged')
                    else:
                        if kind == 'existing-target':
                            target.write_text('unchanged')
                        path.symlink_to(target)
                    def forbidden(*args, **kwargs):
                        self.fail('Provider invoked after collision')
                    with self.assertRaises(WorkflowError):
                        generation.run_generation(protocol_path=self.protocol, case_id='EC-06-1-v1',
                            role='without graph expansion', output_dir=folder, runner=forbidden,
                            collection=self.query.collection, graph_path=self.query.graph)
                    if target.exists():
                        self.assertEqual(target.read_text(), 'unchanged')

    def test_failed_transport_and_malformed_content_keep_evidence_and_metadata(self):
        from types import SimpleNamespace
        from learning_project.workflow import WorkflowError
        import subprocess
        self.prepare()
        variants = [SimpleNamespace(returncode=3, stdout='failed', stderr='quota'),
                    SimpleNamespace(returncode=0, stdout=json.dumps({'status': 'SUCCESS', 'response': '{} {}'}), stderr=''),
                    subprocess.TimeoutExpired(['agy'], 330, output=b'partial', stderr=b'timeout')]
        for index, value in enumerate(variants):
            folder = self.root / f'failed-{index}'
            def runner(*args, **kwargs):
                if isinstance(value, Exception):
                    raise value
                return value
            with self.assertRaises(WorkflowError):
                generation.run_generation(protocol_path=self.protocol, case_id='EC-06-1-v1',
                    role='without graph expansion', output_dir=folder, runner=runner,
                    collection=self.query.collection, graph_path=self.query.graph)
            self.assertTrue((folder / 'provider-response.json').exists())
            self.assertEqual(json.loads((folder / 'run-metadata.json').read_text())['status'], 'execution failure')
            self.assertFalse((folder / 'outcome.json').exists())

    def test_protocol_tampering_is_rejected_before_provider(self):
        from learning_project.workflow import WorkflowError
        self.prepare()
        protocol = json.loads(self.protocol.read_text())
        protocol['cases'][0]['requests']['without graph expansion']['task instruction'] = 'Use reference facts'
        self.protocol.write_text(json.dumps(protocol))
        def forbidden(*args, **kwargs):
            self.fail('Provider invoked for changed protocol')
        with self.assertRaises(WorkflowError):
            generation.run_generation(protocol_path=self.protocol, case_id='EC-06-1-v1',
                role='without graph expansion', output_dir=self.root / 'tampered', runner=forbidden,
                collection=self.query.collection, graph_path=self.query.graph)

    def test_cli_preparation_and_verification_detects_changed_outcome(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from learning_project.workflow import WorkflowError
        code, message = self.query.cli('prepare-generation', '--collection', self.query.collection,
            '--graph', self.query.graph, '--model', 'gemini-3.8-flash-low', '--output', self.protocol)
        self.assertEqual(code, 0, message)
        def runner(*args, **kwargs):
            return SimpleNamespace(returncode=0, stdout=json.dumps({'status': 'SUCCESS', 'response': json.dumps({
                'outcome_type': 'refusal', 'blocking_condition': 'insufficient supplied source evidence'})}), stderr='')
        folder = self.root / 'runs'
        for case_id in ['EC-06-1-v1', 'EC-06-2-v1']:
            for role in generation.ROLES:
                generation.run_generation(protocol_path=self.protocol, collection=self.query.collection,
                    graph_path=self.query.graph, case_id=case_id, role=role,
                    output_dir=folder / case_id / role.replace(' ', '-'), runner=runner)
        result = generation.verify_generation(protocol_path=self.protocol, collection=self.query.collection,
            graph_path=self.query.graph, runs_dir=folder)
        self.assertEqual(result['observed_outputs'], 4)
        outcome = folder / 'EC-06-1-v1' / 'without-graph-expansion' / 'outcome.json'
        outcome.write_text('{}')
        with self.assertRaises(WorkflowError):
            generation.verify_generation(protocol_path=self.protocol, collection=self.query.collection,
                graph_path=self.query.graph, runs_dir=folder)

    def test_schema_capture_uses_explicit_structured_output_without_scanning_for_favorable_json(self):
        from types import SimpleNamespace
        self.prepare()
        outcome = {'outcome_type': 'refusal', 'blocking_condition': 'insufficient supplied source evidence'}
        capture = self.root / 'capture.json'
        capture.write_text(json.dumps({'stdout': json.dumps({'status': 'SUCCESS',
            'response': 'prose {} {}', 'structured_output': outcome}), 'stderr': '', 'returncode': 0}))
        paths = generation.run_generation(protocol_path=self.protocol, collection=self.query.collection,
            graph_path=self.query.graph, case_id='EC-06-1-v1', role='without graph expansion',
            output_dir=self.root / 'imported', recorded_response=capture)
        self.assertEqual(json.loads(paths['outcome'].read_text()), outcome)
        metadata = json.loads(paths['metadata'].read_text())
        self.assertEqual(metadata['evidence_kind'], 'imported provider capture')
        self.assertIn('capture_digest', metadata)


if __name__ == '__main__':
    unittest.main()
