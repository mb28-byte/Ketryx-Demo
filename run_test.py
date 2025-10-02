import subprocess
import sys

# Define the constants for the test
CODE_TO_TEST = "hello.py"
EXPECTED_OUTPUT = "hello world"
TEST_CASE_ID = "tc-hw-1"

try:
    # 1. Execute the script and capture the output
    result = subprocess.run(
        [sys.executable, CODE_TO_TEST],
        capture_output=True,
        text=True,
        check=True # Raise an exception if hello.py returns an error code
    )
    
    # 2. Compare the actual output to the expected output
    actual_output = result.stdout.strip()

    if actual_output == EXPECTED_OUTPUT:
        print(f"Test Execution Result for {TEST_CASE_ID}: PASS")
        sys.exit(0)  # Exit successfully for CI to proceed
    else:
        print(f"Test Execution Result for {TEST_CASE_ID}: FAIL")
        print(f"  Expected: '{EXPECTED_OUTPUT}'")
        print(f"  Actual:   '{actual_output}'")
        sys.exit(1)  # Exit with error code to indicate failure

except subprocess.CalledProcessError as e:
    print(f"Test Execution Result for {TEST_CASE_ID}: ERROR")
    print(f"  Script failed to execute. Error: {e.stderr.strip()}")
    sys.exit(1)
except FileNotFoundError:
    print(f"Test Execution Result for {TEST_CASE_ID}: ERROR")
    print(f"  Code file not found at: {CODE_TO_TEST}")
    sys.exit(1)
