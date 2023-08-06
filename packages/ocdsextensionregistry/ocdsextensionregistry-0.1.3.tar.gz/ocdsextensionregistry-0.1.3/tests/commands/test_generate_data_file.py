import json
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from ocdsextensionregistry.cli.__main__ import main
from tests import read

args = ['ocdsextensionregistry', 'generate-data-file']


@patch('sys.stdout', new_callable=StringIO)
def test_command(stdout, monkeypatch):
    monkeypatch.setattr(sys, 'argv', args + ['location==v1.1.4'])
    main()

    assert stdout.getvalue() == read('location-v1.1.4.json')


@patch('sys.stdout', new_callable=StringIO)
def test_command_latest_version_master(stdout, monkeypatch):
    monkeypatch.setattr(sys, 'argv', args + ['location==v1.1.4', 'location==master'])
    main()

    assert json.loads(stdout.getvalue())['location']['latest_version'] == 'master'


@patch('sys.stdout', new_callable=StringIO)
def test_command_latest_version_default(stdout, monkeypatch):
    monkeypatch.setattr(sys, 'argv', args + ['legalBasis==1.1', 'legalBasis==1.2'])
    main()

    assert json.loads(stdout.getvalue())['legalBasis']['latest_version'] == '1.1'


@patch('sys.stdout', new_callable=StringIO)
def test_command_latest_version_dated(stdout, monkeypatch):
    monkeypatch.setattr(sys, 'argv', args + ['location==v1.1.5', 'location==v1.1.4'])
    main()

    assert json.loads(stdout.getvalue())['location']['latest_version'] == 'v1.1.5'


@patch('sys.stderr', new_callable=StringIO)
@patch('sys.stdout', new_callable=StringIO)
def test_command_missing_locale_dir(stdout, stderr, monkeypatch):
    with pytest.raises(SystemExit) as excinfo:
        monkeypatch.setattr(sys, 'argv', args + ['--languages', 'es', 'location==v1.1.4'])
        main()

    assert stdout.getvalue() == ''
    assert '--locale-dir is required if --languages is set.' in stderr.getvalue()
    assert excinfo.value.code == 2


@patch('sys.stdout', new_callable=StringIO)
def test_command_directory(stdout, monkeypatch, tmpdir):
    versions_dir = tmpdir.mkdir('outputdir')
    version_dir = versions_dir.mkdir('location').mkdir('v1.1.4')
    locale_dir = tmpdir.mkdir('localedir')
    for locale in ('en', 'es'):
        locale_dir.mkdir(locale)

    version_dir.join('extension.json').write('{"name": "Location", "description": "…"}')
    version_dir.join('README.md').write('# Location')

    monkeypatch.setattr(sys, 'argv', args + ['--versions-dir', str(versions_dir), '--locale-dir', str(locale_dir),
                                             'location==v1.1.4'])
    main()

    assert json.loads(stdout.getvalue()) == {
        'location': {
            'id': 'location',
            'category': 'item',
            'core': True,
            'name': {
                'en': 'Location',
                'es': 'Location',
            },
            'description': {
                'en': '…',
                'es': '…',
            },
            'latest_version': 'v1.1.4',
            'versions': {
                'v1.1.4': {
                    'id': 'location',
                    'date': '2019-02-25',
                    'version': 'v1.1.4',
                    'base_url': 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.4/',  # noqa: E501
                    'download_url': 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1.4',  # noqa: E501
                    'publisher': {
                        'name': 'open-contracting-extensions',
                        'url': 'https://github.com/open-contracting-extensions',
                    },
                    'metadata': {
                        'name': {
                            'en': 'Location',
                            'es': 'Location',
                        },
                        'description': {
                            'en': '…',
                            'es': '…',
                        },
                        'documentationUrl': {},
                        'compatibility': ['1.1'],
                    },
                    'schemas': {
                        'record-package-schema.json': {},
                        'release-package-schema.json': {},
                        'release-schema.json': {},
                    },
                    'codelists': {},
                    'readme': {
                        'en': '# Location\n',
                        'es': '# Location\n',
                    },
                },
            },
        },
    }
