# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3streamer']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 's3streamer',
    'version': '2021.2.4.1',
    'description': 'Stream files to AWS S3 using multipart upload.',
    'long_description': '==============\n**S3Streamer**\n==============\n\nOverview\n--------\n\nA frontend module to upload files to AWS S3 storage. The module supports large files as it chunks them into smaller sizes and recombines them into the original file in the specified S3 bucket. It employs multiprocessing, and there is the option of specifying the size of each chunk as well as how many chunks to send in a single run. The defaults are listed in **Optional Arguments** below.\n\nPrerequisites\n-------------\n\n- An AWS S3 bucket to receive uploads.\n- An AWS Lambda function to perform backend tasks.\n- The AWS CloudFormation template to create these resources are available in the project\'s GitHub repository.\n\nRequired (Positional) Arguments\n-------------------------------\n\n- Position 1: Filename (local full / relative path to the file)\n\nOptional (Keyword) Arguments\n----------------------------\n\n- path: Destination path in the S3 bucket (default: /)\n- parts: Number of multiprocessing parts to send simultaneously (default: 5)\n- partsize: Size of each part in MB (default: 100)\n- tmp: Location of local temporary directory to store temporary files created by the module (default: \'/tmp\')\n- purge: Whether to purge the specified file instead of uploading it (default: False)\n- requrl: The endpoint URL for backend Lambda function (default: \'https://<api_endpoint_url>\')\n- reqapikey: The API key for backend Lambda function (default: \'<api_key>\')\n\nUsage\n-----\n\nInstallation:\n\n.. code-block:: BASH\n\n   pip3 install s3streamer\n   # or\n   python3 -m pip install s3streamer\n\nIn Python3:\n\n.. code-block:: BASH\n\n   # To upload a new file.\n   from s3streamer.s3streamer import multipart\n   response = multipart(\n       \'myfile.iso\', \n       \'installer/images\'\n   )\n\n   # To remove a file from S3.\n   from s3streamer.s3streamer import multipart\n   response = multipart(\n       \'myfile.iso\', \n       \'installer/images\', \n       purge = True\n   )\n\nIn BASH:\n\n.. code-block:: BASH\n\n   # To upload a new file.\n   python3 -c \\\n   "from s3streamer.s3streamer import multipart; \\\n   response = multipart(\\\n   \'myfile.iso\', \\\n   \'installer/images\')"\n\n   # To remove a file from S3.\n   python3 -c \\\n   "from s3streamer.s3streamer import multipart; \\\n   response = multipart(\\\n   \'myfile.iso\', \\\n   \'installer/images\', \\\n   purge = True)"\n\nIf the upload is successful, the file will be available at **installer/images/myfile.iso**.\n\nChangelog\n---------\n\n2021.2.4.1\n\n- Updated README.\n\n2021.2.4.0\n\n- Simplified the module and backend to use as few assumptions as possible.\n- Removed authentication and authorization layer.\n- Removed CloudFront.\n- Removed S3 path verification; default is now the root path.\n- Removed overwrite flag; overwrites existing objects by default if already exists.\n- One-step backend deployment (plus credentials creation and stack update).\n- Cleaned-up module to replace most printouts with returns.\n\n2021.2.3.2\n\n- Removed CDN cache purge request from the module. That requet can be made separately based on use-cases.\n\n2021.2.3.1\n\n- Updated README to account for recent changes.\n\n2021.2.3.0\n\n- Streamlined all backend HTTP calls to use *requests* instead of *urllib*.\n- Updated backend to use API key and Bearer token for authentication and authorization.\n- Updated frontend to follow suit.\n\n2020.2.2.3\n\n- Added link to project repository.\n\n2020.2.2.2\n\n- Updated HTTP method for geturl action.\n\n2020.2.2.1\n\n- Removed tqdm as dependency. The module works more silently now.\n\n2020.2.2.0\n\n- Streamlined HTTP response throughout all layers of the streaming process. The frontend now echoes the status from the backend instead of producing its own, where possible.\n- Code cleanup.\n\n2020.2.1.7\n\n- Initial release of the finalized working module.\n\n*Current version: 2021.2.4.1*\n',
    'author': 'Ahmad Ferdaus Abd Razak',
    'author_email': 'ahmad.ferdaus.abd.razak@ni.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fer1035/pypi-s3streamer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
