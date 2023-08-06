# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['better_exceptions>=0.2.2,<0.3.0',
 'bs4>=0.0.1,<0.0.2',
 'fire>=0.3.1,<0.4.0',
 'halo>=0.0.29,<0.0.30',
 'ipython>=7.15.0,<8.0.0',
 'keyring>=21.2.1,<22.0.0',
 'pick>=0.6.7,<0.7.0',
 'requests>=2.24.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

entry_points = \
{'console_scripts': ['dakoker = src.dakoker:main']}

setup_kwargs = {
    'name': 'dakoker',
    'version': '0.1.29',
    'description': '',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/dakoker.svg)](https://pypi.python.org/pypi/dakoker)\n\nMF-Dakoker\n=======\n\n[MFクラウド勤怠](https://biz.moneyforward.com/attendance)利用者向けに作った打刻・勤怠状況確認ツールです。\n\n### 出勤・退勤等の打刻\n![Gif](https://raw.github.com/wiki/nixiesquid/mf-dakoker/end.gif)\n\n### 打刻履歴の確認\n![Gif](https://raw.github.com/wiki/nixiesquid/mf-dakoker/history.gif)\n\n主な機能\n- MFクラウド勤怠へのログイン\n- 出勤・退勤の打刻\n- 休憩開始・終了の打刻\n- 当日の勤怠状況の確認(打刻日時)\n- ブラウザでMFクラウド勤怠ページを直接開く\n- ログイン情報キャシュ・キャッシュクリア\n\n実装したい機能\n- 二重打刻の防止機能\n- 指定日の勤怠状況の確認(打刻日時)\n\n動作環境\n- Python 3.9\n- poetry 1.0.9\n\n## インストール方法\n`pip3 install dakoker`\n\nまた、現在Chrome Driver・Safari Driverに対応しており、以下の設定が必要です。\n\n- Chrome Driverの場合\n  - `brew install chromedriver` (mac OS Xの場合) でchromedriverをインストール\n  - お使いのChromeブラウザとChrome Driverのバージョンが合っていない場合、正しく動作しないケースがあります。バージョンが合ったChrome Driverを使うようにしてください。\n\n- Safari Driverの場合\n  - Safari 10.0以上を使っている場合使用可能です\n  - Safari Driverを利用する場合、"環境設定"から開発メニューを表示させ、「リモートオートメーション」を許可してください。\n\n### 初回利用時\nログインのため、以下の情報を入力します。\n\n2回目以降は使用OSのパスワード保存領域(e.g. mac OS Xであればキーチェーン上)・その他ローカル領域にキャッシュされたログイン情報を読み込み、自動ログインします。\n\n- 企業ID\n- ユーザーID もしくは登録メールアドレス\n- パスワード\n\n![初回ログイン時](https://gyazo.com/e0657a3eecfc6a486a469a0cebd98db1.png)\n\n## 使い方\n\n- 出勤\n  - `dakoker start`\n- 退勤\n  - `dakoker end`\n- 休憩開始\n  - `dakoker start_break`\n- 休憩終了\n  - `dakoker end_break`\n- 当日の勤怠状況の確認\n  - `dakoker history`\n- ブラウザでMFクラウド勤怠ページを直接開く\n  - `dakoker open`\n- ログイン情報キャッシュのクリア\n  - `dakoker clear`\n',
    'author': 'nixiesquid',
    'author_email': 'audu817@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
