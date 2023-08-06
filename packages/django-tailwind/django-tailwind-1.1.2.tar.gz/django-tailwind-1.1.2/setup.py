# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tailwind',
 'tailwind.app_template_v1',
 'tailwind.app_template_v2',
 'tailwind.management',
 'tailwind.management.commands']

package_data = \
{'': ['*'],
 'tailwind.app_template_v1': ['static_src/*',
                              'static_src/src/*',
                              'templates/*'],
 'tailwind.app_template_v2': ['static_src/*',
                              'static_src/src/*',
                              'templates/*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'django-tailwind',
    'version': '1.1.2',
    'description': 'Tailwind CSS Framework for Django projects',
    'long_description': '# The integration of Tailwind CSS framework with Django a.k.a. Django + Tailwind = ❤\n\n## Quick start\n\n1. Install the `django-tailwind` package via Pip:\n\n   `python -m pip install django-tailwind`\n\n   Alternatively, you can install the latest development version via:\n\n   `python -m pip install git+https://github.com/timonweb/django-tailwind.git`\n\n2. Add `tailwind` to INSTALLED_APPS in **settings.py**\n\n3. Create a tailwind-compatible Django-app, I like to call it `theme`:\n\n   `python manage.py tailwind init theme`\n   \n   *NOTE:* By default, we install v2 of Tailwind CSS. If you want v1 Tailwind CSS you need to pass an additional `--legacy` parameter to the command:\n   `python manage.py tailwind init --legacy theme`.\n\n4. Add your newly created `theme` app to INSTALLED_APPS in **settings.py**\n\n5. In settings.py, register tailwind app by adding the following string:\n\n   `TAILWIND_APP_NAME = \'theme\'`\n\n6. Run a command to install all necessary dependencies for tailwind css:\n\n   `python manage.py tailwind install`\n\n7. Now, go and start tailwind in dev mode:\n\n   `python manage.py tailwind start`\n\n8. Django Tailwind comes with a simple `base.html` template that can be found under\n   `your_tailwind_app_name/templates/base.html`. You can always extend it or delete it if you\n   have own layout.\n\n9. If you\'re not using `base.html` template provided with Django Tailwind, add `styles.css` to your own `base.html` template file:\n\n   ```html\n   <link\n     rel="stylesheet"\n     href="{% static \'css/styles.css\' %}"\n     type="text/css"\n   />\n   ```\n\n10) You should now be able to use Tailwind CSS classes in your html.\n\n11) To build a production version of CSS run:\n\n    `python manage.py tailwind build`.\n\n## PurgeCSS setup\n\nTo avoid importing all of Tailwind (resulting in a massive CSS filesize), set up the purge configuration in `tailwind.config.js`.\nThis file is located in the `static_src` folder of the app created by `tailwind init {APP_NAME}`.\n\nFor example, your `tailwind.config.js` file could look like:\n\n```js\nmodule.exports = {\n  purge: [\n    // Templates within theme app (e.g. base.html)\n    \'../templates/**/*.html\',\n    // Templates in other apps\n    \'../../templates/**/*.html\',\n  ],\n  ...\n}\n```\n\nNote that you may need to adjust those paths to suit your specific project layout. It is important to ensure that _all_ of your HTML files are covered (or files with contain HTML content, such as .vue or .jsx files), to enusre PurgeCSS can whitelist all of your classes.\n\nFor more information on this, check out the "Controlling File Size" page of the Tailwind docs: [https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css](https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css) - particularly the "Removing Unused CSS" section, although the entire page is a useful reference.\n\nTo help speed up development builds, PurgeCSS is only run when you use the `tailwind build` management command (to create a production build of your CSS).\n\n## NPM executable path configuration\n\nSometimes (especially on Windows), Python executable can\'t find `NPM` installed in the system.\nIn this case, you need to set `NPM` executable path in settings.py file manually (Linux/Mac):\n\n```python\nNPM_BIN_PATH = \'/usr/local/bin/npm\'\n```\n\nOn windows it might look like:\n\n```python\nNPM_BIN_PATH = r"C:\\Program Files\\nodejs\\npm.cmd"\n```\n\nPlease note that `NPM` path of your system may be different. Try to run `which npm` in your\ncommand line to get the path.\n\n## Updating Tailwind CSS and dependencies\n\nIf there\'s a new release of the tailwind css came out you can always update your `theme` project\nwithout updating this django package by using two commands: `python manage.py tailwind check-updates` and\n`python manage.py tailwind update`.\n\n### Checking if there are updates for tailwind css and its dependencies\n\nBefore doing an update, you can check if there are any updates. Run the following command:\n```\npython manage.py tailwind check-updates\n```\n*Behind the scenes it runs `npm outdated` command within your `theme/static_src` directory.*\n\nIf there are updates, you\'ll see a table dependencies with the latest compatible versions.\nIf there are no updates, this command will return no output.\n\n### Updating tailwind css and its dependencies\n\nIf you want to use the latest version of tailwind css, run the following command:\n\n```\npython manage.py tailwind update\n```\n*Behind the scenes it runs `npm update` command within your `theme/static_src` directory.*\n\nIf there are updates, you\'ll see a log of updated dependencies.\nIf there are no updates, this command will return no output.\n\n## Bugs and suggestions\n\nIf you have found a bug, please use the issue tracker on GitHub.\n\n[https://github.com/timonweb/django-tailwind/issues](https://github.com/timonweb/django-tailwind/issues)\n\n2020 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)\n',
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timonweb/django-tailwind',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
