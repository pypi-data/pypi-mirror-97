import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(name='db_operations',
                 version='1.0.1',
                 author='K.lz',
                 author_email='565150134@qq.com',
                 description='Simple operation of database',
                 url='https://github.com/kimkimheel/db_operations',
                 packages=setuptools.find_packages(),
                 install_requires=['pymysql','pymssql','cx_Oracle','pandas','psycopg2'],
                 long_description = long_description,
                 long_description_content_type="text/markdown",
                 zip_safe=False)