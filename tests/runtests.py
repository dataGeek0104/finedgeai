import subprocess
import sys

# 1) run pytest as a list—no shell
ret = subprocess.run(["pytest"], check=False).returncode
if ret != 0:
    sys.exit(ret)

# 2) remove the cache directory
subprocess.run(["rm", "-rf", ".pytest_cache"], check=True)
