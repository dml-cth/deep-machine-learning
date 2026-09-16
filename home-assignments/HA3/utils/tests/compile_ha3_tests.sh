cd "$(dirname "$0")"
rm -f ./__pycache__/ha3_tests_source*.pyc
echo "python -m compileall ./ha3_tests_source.py"
python -m compileall ./ha3_tests_source.py
mv ./__pycache__/ha3_tests_source*.pyc ./ha3_tests.pyc
