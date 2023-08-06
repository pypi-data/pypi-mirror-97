# Example Package

This is the OMG package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

py setup.py sdist bdist_wheel

py -m twine upload dist/*
py -m twine upload --skip-existing dist/*
py -m twine upload --repository testpypi dist/*

py -m twine upload --repository testpypi --skip-existing dist/*


py -m pip install --index-url  https://test.pypi.org/project/pyomega/0.0.2/ --no-deps pyomega-pyomega

py -m pip install -i https://test.pypi.org/simple/ pyomega==0.0.2

