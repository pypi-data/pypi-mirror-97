# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apm_agent_utils']

package_data = \
{'': ['*']}

install_requires = \
['elastic-apm>=5.4.0,<6.0.0', 'qualname>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'apm-agent-utils',
    'version': '1.3.0',
    'description': 'This package can help you create Elastic APM instrumentations using regex',
    'long_description': '## Elastic APM Agent Utils\nThis package can help you create Elastic APM instrumentations using regex.\n\n### Dependencies\n1. `python3.6+`  \n2. `elastic-apm`  \n\n### Installation\n```sh\npip install apm-agent-utils\n```\n\n### Usage\nCreate a file named `instrumentations.py`\n```python\n# instrumentations.py\nfrom apm_agent_utils.instrumentation import InstrumentationBuilder\n\nbuilder = InstrumentationBuilder("Test")\nbuilder.add_instrument("logic.logic1", r"^hello.*")  # finding and wrapping your funtions by regex\nbuilder.add_instrument("logic.logic2", r".*")\n\nTest = builder.create_instrument()\n```\nIn your `app.py`, adding the following lines at top of the file.  \n```python\nimport elasticapm\nfrom apm_agent_utils.utils import add_instrumentation\n\nadd_instrumentation("instrumentations.Test")\nelasticapm.instrument()\n```\n==> `app.py`  \n```python\n# app.py\nimport elasticapm\nfrom apm_agent_utils.utils import add_instrumentation\nfrom elasticapm.contrib.flask import ElasticAPM\nfrom flask import Flask\n\nadd_instrumentation("instrumentations.Instrument")\nelasticapm.instrument()\n\napp = Flask(__name__)\napp.config[\'ELASTIC_APM\'] = {\n    \'SERVICE_NAME\': \'vuonglv_test\',\n    \'SECRET_TOKEN\': \'#####\',\n    \'SERVER_URL\': \'http://##.##.##.##:8200/\',\n    \'DEBUG\': True\n}\n\napm = ElasticAPM(app)\n```\n`main.py` - your controllers\n```python\n# main.py\nfrom app import app\n\nfrom logic.logic1 import hello\nfrom logic.logic2 import foo, bar\n\n\n@app.route("/")\ndef run():\n    print(hello())\n    print(foo())\n    print(bar())\n    return {"ok": True}\n\n\nif __name__ == "__main__":\n    app.run(debug=True)\n```\nProject structure look like this:  \n![structure](screenshots/structure.png)  \nRun app\n```bash\npython3 main.py\n```\nGet your endpoint\n```curl\ncurl --location --request GET \'http://localhost:5000\'\n```\nGoto your APM dashboard, result look like this:\n![successful dashboard](screenshots/dashboard.png)\n',
    'author': 'vuonglv',
    'author_email': 'it.vuonglv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vuonglv1612/apm-agent-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
