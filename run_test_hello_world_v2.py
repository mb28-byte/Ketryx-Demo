import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
import os

# --- Configuration for Ketryx Traceability ---
TEST_CASE_ID = "tc-hw-1" # Must match the ID in your Markdown test case file
REPORT_FILENAME = "test_results.xml"
CODE_TO_TEST = "hello.py" # The actual file being tested
EXPECTED_OUTPUT = "hello world"

# --- Function to Perform Test and Generate XML ---
def run_and_report_test():
    # Variables to track test outcome
    test_passed = False
    error_message = ""
    
    # --- 1. Execute the target code (hello.py) ---
    print(f"Executing code under test: {CODE_TO_TEST}")
    try:
        # Executes the simple 'hello.py' script
        result = subprocess.run(
            [sys.executable, CODE_TO_TEST],
            capture_output=True,
            text=True,
            check=True # Raise exception on non-zero exit code
        )
        
        # --- 2. Check the output ---
        actual_output = result.stdout.strip()
        if actual_output == EXPECTED_OUTPUT:
            test_passed = True
            print(f"Test '{TEST_CASE_ID}' passed: Output matched expected value.")
        else:
            error_message = f"Output Mismatch: Expected '{EXPECTED_OUTPUT}', but got '{actual_output}'"
            print(f"Test '{TEST_CASE_ID}' FAILED: {error_message}")

    except subprocess.CalledProcessError as e:
        test_passed = False
        error_message = f"Script Execution Failed. Stderr: {e.stderr.strip()}"
        print(f"Test '{TEST_CASE_ID}' ERROR: {error_message}")
    except FileNotFoundError:
        test_passed = False
        error_message = f"Critical Error: Code file '{CODE_TO_TEST}' not found. Ensure 'hello.py' is in the root directory."
        print(f"Test '{TEST_CASE_ID}' ERROR: {error_message}")


    # --- 3. Generate JUnit XML Report (Required by Ketryx) ---
    
    # Root element
    testsuites = ET.Element("testsuites", name="Ketryx_CI_Report", time=str(time.time()))
    testsuite = ET.SubElement(
        testsuites,
        "testsuite",
        name="Hello_World_Test",
        tests="1",
        failures="1" if not test_passed else "0",
        errors="0",
        time="1.0"
    )
    
    # Test case element
    testcase = ET.SubElement(
        testsuite,
        "testcase",
        # CRUCIAL: The 'name' attribute must match the Ketryx item ID for traceability
        name=TEST_CASE_ID, 
        classname="app.hello_world",
        time="1.0"
    )

    if not test_passed:
        # If the test failed, add a <failure> element
        ET.SubElement(
            testcase,
            "failure",
            message=error_message,
            type="AssertionError"
        ).text = error_message

    # Format and save the XML
    rough_string = ET.tostring(testsuites, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    with open(REPORT_FILENAME, "w") as f:
        f.write(reparsed.toprettyxml(indent="  "))
    
    print(f"\n--- REPORT GENERATED ---")
    print(f"Report saved to: {REPORT_FILENAME}")
    
    # Exit with a non-zero code if the test failed, so the CI job reflects the test status
    if not test_passed:
        sys.exit(1)
    
if __name__ == "__main__":
    run_and_report_test()
