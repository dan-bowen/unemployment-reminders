from os.path import dirname, abspath, join
import sys

# Find code directory relative to test directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../src'))
sys.path.append(CODE_DIR)
