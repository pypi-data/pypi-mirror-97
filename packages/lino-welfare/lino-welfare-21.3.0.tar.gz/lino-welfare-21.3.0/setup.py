from setuptools import setup
fn = 'lino_welfare/setup_info.py'
exec (compile(open(fn, "rb").read(), fn, 'exec'))
if __name__ == '__main__':
    setup(**SETUP_INFO)
