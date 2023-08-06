set -e
set -x

pytest --cov=revdb --cov=tests --cov-report=term-missing
