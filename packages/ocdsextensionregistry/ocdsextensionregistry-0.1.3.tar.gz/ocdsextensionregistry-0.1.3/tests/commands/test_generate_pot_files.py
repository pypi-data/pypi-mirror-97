import os
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from ocdsextensionregistry.cli.__main__ import main

args = ['ocdsextensionregistry', 'generate-pot-files']


@patch('sys.stdout', new_callable=StringIO)
def test_command(stdout, monkeypatch, tmpdir):
    monkeypatch.setattr(sys, 'argv', args + [str(tmpdir), 'location==v1.1.4'])
    main()

    assert stdout.getvalue() == ''

    tree = list(os.walk(tmpdir))

    assert len(tree) == 3
    # extensions
    assert tree[0][1] == ['location']
    assert tree[0][2] == []
    # versions
    assert tree[1][1] == ['v1.1.4']
    assert tree[1][2] == []
    # files
    assert tree[2][1] == []
    assert sorted(tree[2][2]) == ['codelists.pot', 'docs.pot', 'schema.pot']


@patch('sys.stdout', new_callable=StringIO)
def test_command_directory(stdout, monkeypatch, tmpdir):
    output_dir = tmpdir.mkdir('build').mkdir('locale')
    versions_dir = tmpdir.mkdir('outputdir')

    versions_dir.mkdir('location').mkdir('v1.1.4').join('README.md').write('# Location')

    monkeypatch.setattr(sys, 'argv', args + ['--versions-dir', str(versions_dir), str(output_dir), 'location==v1.1.4'])
    main()

    assert stdout.getvalue() == ''

    tree = list(os.walk(output_dir))

    assert len(tree) == 3
    # extensions
    assert tree[0][1] == ['location']
    assert tree[0][2] == []
    # versions
    assert tree[1][1] == ['v1.1.4']
    assert tree[1][2] == []
    # files
    assert tree[2][1] == []
    assert sorted(tree[2][2]) == ['docs.pot']


@patch('sys.stdout', new_callable=StringIO)
def test_command_missing_directory(stdout, monkeypatch, tmpdir, caplog):
    output_dir = tmpdir.mkdir('build').mkdir('locale')
    versions_dir = tmpdir.mkdir('outputdir')

    monkeypatch.setattr(sys, 'argv', args + ['--versions-dir', str(versions_dir), str(output_dir), 'location==v1.1.4'])
    main()

    assert stdout.getvalue() == ''

    tree = list(os.walk(output_dir))

    assert len(tree) == 1
    assert tree[0][1] == []
    assert tree[0][2] == []

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == 'Not processing location==v1.1.4 (not in {})'.format(versions_dir)


@patch('sys.stdout', new_callable=StringIO)
def test_command_missing_download_url(stdout, monkeypatch, tmpdir, caplog):
    output_dir = tmpdir.mkdir('build').mkdir('locale')
    file = tmpdir.join('extension_versions.csv')

    file.write('Id,Date,Version,Base URL,Download URL\nlocation,,v1.1.4,http://example.com/,')

    monkeypatch.setattr(sys, 'argv', args + ['--extension-versions-url', Path(file).as_uri(), str(output_dir),
                                             'location==v1.1.4'])
    main()

    assert stdout.getvalue() == ''

    tree = list(os.walk(output_dir))

    assert len(tree) == 1
    assert tree[0][1] == []
    assert tree[0][2] == []

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == 'Not processing location==v1.1.4 (no Download URL)'
