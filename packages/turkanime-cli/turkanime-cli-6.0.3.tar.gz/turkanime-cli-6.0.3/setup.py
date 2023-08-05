# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turkanime_cli', 'turkanime_cli.cli']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'easygui>=0.98.2,<0.99.0',
 'questionary>=1.9.0,<2.0.0',
 'rich>=9.5.1',
 'selenium>=3.141.0,<4.0.0',
 'youtube_dl>=2021.0.0']

entry_points = \
{'console_scripts': ['turkanime = turkanime_cli.cli.turkanime:main']}

setup_kwargs = {
    'name': 'turkanime-cli',
    'version': '6.0.3',
    'description': 'Türkanime video oynatıcı ve indirici',
    'long_description': "# TürkAnimu-Cli\n[![GitHub all releases](https://img.shields.io/github/downloads/kebablord/turkanime-indirici/total?style=flat-square)](https://github.com/KebabLord/turkanime-indirici/releases/latest)  [![GitHub release (latest by date)](https://img.shields.io/github/v/release/kebablord/turkanime-indirici?style=flat-square)](https://github.com/kebablord/turkanime-indirici/releases/latest/download/turkanimu.exe)  [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kebablord/turkanime-indirici/Hata%20kontrol%C3%BC%20ve%20lint?style=flat-square)](https://github.com/KebabLord/turkanime-indirici/actions)\n\nTürkanime için terminal video oynatıcı ve indirici. İtinayla her bölümü indirir & oynatır.\n - Yığın bölüm indirebilir\n - Animu izleyebilir\n - Uygulama içinden arama yapabilir\n - Fansub seçtirebilir\n - Bir yandan izlerken bir yandan animeyi kaydedebilir\n - İndirmelere kaldığı yerden devam edebilir\n \n#### Desteklenen kaynaklar:\n```Sibnet, Odnoklassinki, Sendvid, Mail.ru, VK, Google+, Myvi, GoogleDrive, Yandisk, Vidmoly, Yourupload, Dailymotion```\n\n ### İzleme ekranı\n ![izleme.gif](https://raw.githubusercontent.com/KebabLord/turkanime-indirici/master/ss_izle.gif)\n\n ### İndirme ekranı\n ![indirme.gif](https://raw.githubusercontent.com/KebabLord/turkanime-indirici/master/ss_indir.gif)\n\n\n### Yapılacaklar:\n - ~~Domain güncellemesinden beridir kod stabil çalışmıyor, düzeltilecek.~~\n - ~~Kod çorba gibi, basitleştirilecek.~~\n - ~~Navigasyon  ve indirme algoritması http talepleriyle sağlanacak.~~\n - ~~Zaman bloğu olarak sleep'den kurtulunacak, elementin yüklenmesi beklenecek.~~\n - ~~Prompt kütüphanesi olarak berbat durumda olan PyInquirer'den Questionary'e geçilecek.~~\n - ~~Arama sonuçları da http talepleriyle getirilecek.~~\n - ~~Fansub seçme özelliği tekrar eklenecek.~~\n",
    'author': 'Junicchi',
    'author_email': 'junicchi@waifu.club',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kebablord/turkanime-indirici',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
