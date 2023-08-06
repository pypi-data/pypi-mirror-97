import sys
from io import StringIO
from unittest.mock import patch

from ocdsextensionregistry.cli.__main__ import main

args = ['ocdsextensionregistry']


@patch('sys.stdout', new_callable=StringIO)
def test_command(stdout, monkeypatch, tmpdir):
    monkeypatch.setattr(sys, 'argv', args)
    main()

    assert 'usage: ocdsextensionregistry' in stdout.getvalue()
