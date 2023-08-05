
from setuptools import setup, find_packages
from pipreqs.pipreqs import get_all_imports, get_pkg_names, get_import_local
reqs = get_import_local(get_pkg_names(
    get_all_imports('./', encoding='utf-8')), encoding='utf-8')
reqs = list(map(lambda req: '{}>={}'.format(
    req['name'], req['version'] if req['name'] != 'fastapi' else '0.60.0'), reqs))


with open('requirements.txt', mode='w', encoding='utf-8') as f:
    f.write('\n'.join(reqs))

setup(
    name='qg_common_sdk',
    version='1.1.0',
    description=(
        '全高python统一处理底层框架封装包'
    ),
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding='utf-8').read(),
    author='lbb',
    author_email='liubeibei15895926598@gmail.com',
    maintainer='lbb',
    maintainer_email='liubeibei15895926598@gmail.com',
    license='GPL3 License',
    packages=find_packages(),
    platforms=["all"],
    url='http://192.168.117.144/cetc28/spiderStructFrameWork',
    install_requires=reqs,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)
