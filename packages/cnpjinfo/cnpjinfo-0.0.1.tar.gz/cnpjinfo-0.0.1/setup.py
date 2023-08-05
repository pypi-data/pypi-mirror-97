from setuptools import setup

setup(
    name = 'cnpjinfo',
    version = '0.0.1',
    author = 'Julian de Almeida Santos',
    author_email = 'julian.santos.info@gmail.com',
    packages = ['cnpjinfo'],
    description = 'Library for obtaining cnpj information via scraping from the receitaws website.',
    long_description = 'Library for obtaining cnpj information via scraping from the receitaws website.',
    url = 'https://github.com/juliansantosinfo/cnpjinfo.git',
    project_urls = {
        'Código fonte': 'https://github.com/juliansantosinfo/cnpjinfo.git',
        'Download': 'https://github.com/juliansantosinfo/cnpjinfo/archive/0.0.1.zip'
    },
    license = 'MIT',
    keywords = ['cnpj', 'information', 'receitaws'],
    install_requires = ['beautifulsoup4']
)
