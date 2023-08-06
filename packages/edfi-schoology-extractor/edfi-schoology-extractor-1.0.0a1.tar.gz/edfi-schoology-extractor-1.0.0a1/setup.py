# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edfi_schoology_extractor',
 'edfi_schoology_extractor.api',
 'edfi_schoology_extractor.helpers',
 'edfi_schoology_extractor.mapping']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.20,<2.0.0',
 'configargparse>=1.2.3,<2.0.0',
 'edfi-lms-extractor-lib==1.0.0a3',
 'errorhandler>=2.0.1,<3.0.0',
 'oauthlib>=3.1.0,<4.0.0',
 'opnieuw>=1.1.0,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'requests>=2.24.0,<3.0.0',
 'requests_oauthlib>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'edfi-schoology-extractor',
    'version': '1.0.0a1',
    'description': 'Extract tool for retrieving student data from Canvas',
    'long_description': '# Schoology Extractor\n\nThis tool retrieves and writes out to CSV students, active sections†,\nassignments, and submissions by querying the Schoology API († sections that are\nin an active grading period). For more information on the this tool and its\noutput files, please see the main repository\n[readme](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit).\n\n## Special Notes About Working With Schoology\n\nSpecial note about _attendance events_: the Schoology API handles _negative\nattendance_ events: if a student is marked as present, or is not marked at all,\nthen the system will not return a record for that day.\n\nSystem usage (activities) in Schoology are only available by downloading a file\nthrough the Schoology website. If you wish to track system student use of the\nsystem, then please read [Schoology\'s instructions on usage\nanalytics](https://support.schoology.com/hc/en-us/articles/360036884914-Usage-Analytics-New-School-Analytics-Enterprise-).\nEach downloaded file needs to be stored in an input directory, and that\ndirectory must be provided to the extractor configuration.\n\n## Getting Started\n\n1. Download the latest code from [the project homepage](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit) by clicking on the green "CODE" button and choosing an appropriate option. If choosing the Zip option, extract the file contents using your favorite zip tool.\n1. Open a command prompt* and change to this file\'s directory (* e.g. cmd.exe, PowerShell, bash).\n1. Ensure you have [Python 3.8+ and Poetry](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit#getting-started).\n1. At a command prompt, install all required dependencies:\n\n   ```bash\n   poetry install\n   ```\n\n1. Optional: make a copy of the `.env.example` file, named simply `.env`, and\n   customize the settings as described in the Configuration section below.\n1. Open [https://app.schoology.com/api](https://app.schoology.com/api) and\n   sign-in with an administrative account to acquire an API key and secret; if\n   using a `.env` file, insert those values into the file.\n1. Run the extractor one of two ways:\n   * Execute the extractor with minimum command line arguments:\n\n      ```bash\n      poetry run python edfi_schoology_extractor -k [schoology client key]\n          -s [schoology client secret]\n      ```\n\n   * Alternately, run with environment variables or `.env` file:\n\n     ```bash\n     poetry run python edfi_schoology_extractor\n     ```\n\n   * For detailed help, execute `poetry run python canvas_extractor -h`.\n\n## Configuration\n\nApplication configuration is provided through environment variables or command\nline interface (CLI) arguments. CLI arguments take precedence over environment\nvariables. Environment variables can be set the normal way, or by using a\ndedicated [`.env` file](https://pypi.org/project/python-dotenv/). For `.env`\nsupport, we provided a [.env.example](.env.example) which you can copy, rename\nto `.env`, and adjust to your desired parameters. Supported parameters:\n\n| Description | Required | Command Line Argument | Environment Variable |\n| ----------- | -------- | --------------------- | -------------------- |\n| Schoology API Key | yes | `-k` or `--client-key` | SCHOOLOGY_KEY |\n| Schoology API Secret | yes | `-s` or `--client-secret` | SCHOOLOGY_SECRET |\n| Usage analytics input directory | no | `-i` or `--input-directory` | SCHOOLOGY_INPUT_DIRECTORY |\n| Output Directory | no (default: [working directory]/data) | `-o` or `--output-directory` | SCHOOLOGY_OUTPUT_PATH |\n| Log level** | no (default: INFO) | `-l` or `--log-level` | SCHOOLOGY_LOG_LEVEL |\n| Page size | no (default: 20) | `-p` or `--page-size` | PAGE_SIZE |\n| Number of retry attempts for failed API calls | no (default: 4) | none | REQUEST_RETRY_COUNT |\n| Timeout window for retry attempts, in seconds | no (default: 60 seconds) | none | REQUEST_RETRY_TIMEOUT_SECONDS |\n\n\\** Valid values for the optional _log level_:\n\n* DEBUG\n* INFO(default)\n* WARNING\n* ERROR\n* CRITICAL\n\n### Logging and Exit Codes\n\nLog statements are written to the standard output. If you wish to capture log\ndetails, then be sure to redirect the output to a file. For example:\n\n```bash\npoetry run python edfi_schoology_extractor > 2020-12-07-15-43.log\n```\n\nIf any errors occurred during the script run, then there will be a final print\nmessage to the standard error handler as an additional mechanism for calling\nattention to the error: `"A fatal error occurred, please review the log output\nfor more information."`\n\nThe application will exit with status code `1` if there were any log messages at\nthe ERROR or CRITICAL level, otherwise it will exit with status code `0`.\n\n## Developer Operations\n\n1. Style check: `poetry run flake8`\n1. Static typing check: `poetry run mypy .`\n1. Run unit tests: `poetry run pytest`\n1. Run unit tests with code coverage: `poetry run coverage run -m pytest`\n1. View code coverage: `poetry run coverage report`\n\n_Also see\n[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_ for\nuse of the build script.\n\n### Visual Studio Code (Optional)\n\nTo work in Visual Studio Code install the Python Extension.\nThen type `Ctrl-Shift-P`, then choose `Python:Select Interpreter`,\nthen choose the environment that includes `.venv` in the name.\n\n## Legal Information\n\nCopyright (c) 2021 Ed-Fi Alliance, LLC and contributors.\n\nLicensed under the [Apache License, Version 2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the "License").\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n\nSee [NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md) for\nadditional copyright and license notifications.\n',
    'author': 'Ed-Fi Alliance, LLC, and contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
