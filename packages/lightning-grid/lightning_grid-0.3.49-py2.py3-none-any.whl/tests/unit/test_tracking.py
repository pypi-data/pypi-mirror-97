import pprint
from unittest.mock import patch

import click

from grid import Segment
from grid.tracking import Grid
from grid.tracking import TrackingEvents


class TestTracking:
    def test_env_sensitive(self):
        for key, is_sensitive in {
                "HOME": False,
                "PATH": False,
                "AWS_ACCESS_KEY_ID": True,
                "AWS_SECRET_ACCESS_KEY": True,
        }.items():
            assert is_sensitive == Segment._is_env_sensitive(key)

    def test_segment(self):
        def check_context(ctx):
            assert 'version' in ctx
            assert 'cwd' in ctx
            assert 'env' != ctx['env']
            assert 'json' in ctx

        with patch('analytics.Client', autospec=True):
            s = Segment()
            s.client.identify.assert_called_once()
            args, kwargs = s.client.identify.call_args
            print("Identify called", args, pprint.pformat(kwargs))
            check_context(kwargs['context'])

            s.send_event(TrackingEvents.CLI_FINISHED, {'s': 'b'})
            s.client.track.assert_called_once()
            args, kwargs = s.client.track.call_args
            print("CLI Finished called", args, pprint.pformat(kwargs))
            check_context(kwargs['context'])
            assert TrackingEvents.CLI_FINISHED.value == kwargs['event']
            assert {'s': 'b', 'json': '{"s": "b"}'} == kwargs['properties']

            error_msg = ""
            try:
                error_msg = "I'm a super cool error message"
                raise click.ClickException(error_msg)
            except Exception as e:
                s.report_exception(e)
            assert 2 == s.client.track.call_count

            args, kwargs = s.client.track.call_args
            print("exception caught", args, pprint.pformat(kwargs))
            check_context(kwargs['context'])
            props = kwargs['properties']
            assert props['error'] == 'ClickException'
            assert props['message'] == error_msg
            assert len(props['stacktrace']) > 0

            s.flush()
            s.client.flush.assert_called_once()

            class MockException:
                message = 'test'

            s.report_exception(MockException)

            _, kwargs = s.client.track.call_args
            props = kwargs['properties']
            assert props['message'] == 'test'

    def test_handles_grid_client_exception(self, monkeypatch):
        def mp_init(*args, **kwargs):
            raise click.ClickException('test failure')

        # If the exception is not handled, then this would fail.
        monkeypatch.setattr(Grid, '__init__', mp_init)
        Segment()
