import pytest
import sys

if __name__ == '__main__':
    args = [
        '--cov=app',
        '--cov=models',
        '--cov=hooks',
        '--cov=decorators',
        '--cov-config=.coveragerc',
        '--cov-report=term-missing',
        'tests/'
    ]

    exit_code = pytest.main(args)
    sys.exit(exit_code)