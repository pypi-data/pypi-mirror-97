# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['politylink',
 'politylink.elasticsearch',
 'politylink.graphql',
 'politylink.helpers',
 'politylink.nlp']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.9.1,<8.0.0',
 'ginza>=4.0.5,<5.0.0',
 'kanjize>=0.1.0,<0.2.0',
 'nltk>=3.5,<4.0',
 'pandas>=1.0.5,<2.0.0',
 'sgqlc>=11.0,<12.0',
 'spacy>=2.3.5,<3.0.0']

setup_kwargs = {
    'name': 'politylink',
    'version': '0.1.57',
    'description': '',
    'long_description': '## インストール\n```\npip install politylink\n```\n`politylink.nlp.keyphrase`を使用する場合は、追加で以下を実行してください。\n```\npip install git+https://github.com/boudinfl/pke.git\npython -m nltk.downloader stopwords\n```\n## 使い方\n\n### GraphQLClient\n\nPolityLinkの[GraphQLエンドポイント](https://graphql.politylink.jp/)にアクセスするためのGraphQLClientが用意されています。\n```\nfrom politylink.graphql.client import GraphQLClient\nclient = GraphQLClient()\n```\n\n#### 基本編\n\n`exec`メソッドを使えば任意のGraphQLクエリを実行することができます。\n```\nquery = """\nquery {\n  Bill(filter: {submittedDate: {year: 2020, month: 1, day: 20}}) {\n    name\n  }\n}\n"""\nclient.exec(query)\n```\n2020年1月20日に提出された3つの法律案の名前がJSON形式で得られるはずです。\n```\n{\'data\': {\'Bill\': [{\'name\': \'特定複合観光施設区域の整備の推進に関する法律及び特定複合観光施設区域整備法を廃止する法律案\'},\n   {\'name\': \'地方交付税法及び特別会計に関する法律の一部を改正する法律案\'},\n   {\'name\': \'平成三十年度歳入歳出の決算上の剰余金の処理の特例に関する法律案\'}]}}\n```\n\nまた、`get_all_*`メソッドを使うことで、返り値をJSONではなくPythonクラスのインスタンスとして取得することができます。\n例えば`get_all_bills`では法律案をBillインスタンスとして取得することができます。\n\n```\nbills = client.get_all_bills(fields=[\'id\', \'name\'])\nfirst_bill = bills[0]\n\nprint(f\'{len(bills)}件の法律案を取得しました\')\nprint(f\'最初の法律案は「{first_bill.name}」（{first_bill.id}）です\')\n```\n\n全ての法律案のidと名前（name）が得られるはずです。\n返り値はBillインスタンスなので、ドットを使って各フィールドにアクセスできます。\n```\n207件の法律案を取得しました\n最初の法律案は「地方交付税法及び特別会計に関する法律の一部を改正する法律案」（Bill:s1QZfjoCPyfdXXbrplP3-A）です\n```\n\nまた`filter_`を引数に渡すことで条件を指定して取得することもできます。詳しくは応用編を見てください。\n\n\n#### 応用編\n\nGraphQLClientは[sgqlc](https://github.com/profusion/sgqlc)のラッパークラスであり、クエリをコードで組み立てることも可能です。\n例えば最初の`exec`の例のクエリを組み立てると以下のようになります。\n\n```\nfrom politylink.graphql.schema import Query, _BillFilter, _Neo4jDateTimeInput\nfrom sgqlc.operation import Operation\n\nop = Operation(Query)\nfilter_ = _BillFilter(None)\nfilter_.submitted_date = _Neo4jDateTimeInput(year=2020, month=1, day=20)\nbills = op.bill(filter=filter_)\nbills.name()\nclient.exec(op)\n```\n\n組み立てた`Operation`は自動で文字列に変換されるので`exec`に直接渡すことができます。\n\nまた上で作ったfilter_は`get_all_*`メソッドの引数として渡すこともできます。\n```\nclient.get_all_bills(fields=[\'name\'], filter_=filter_)\n```\n\n最初の3件の法律案がBillインスタンスとして取得できました。\n```\n[Bill(name=\'地方交付税法及び特別会計に関する法律の一部を改正する法律案\'),\n Bill(name=\'平成三十年度歳入歳出の決算上の剰余金の処理の特例に関する法律案\'),\n Bill(name=\'特定複合観光施設区域の整備の推進に関する法律及び特定複合観光施設区域整備法を廃止する法律案\')]\n```\n',
    'author': 'Mitsuki Usui',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://politylink.jp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
