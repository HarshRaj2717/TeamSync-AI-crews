# Step 1
from io import StringIO
import sys

tmp = sys.stdout

my_result = StringIO()

sys.stdout = my_result

print('hello world')

sys.stdout = tmp

print('VARIABLE:', my_result.getvalue())
# hello world