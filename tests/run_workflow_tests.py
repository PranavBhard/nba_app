#!/usr/bin/env python3
"""
Master test runner for all workflow integration tests.

Runs all workflow tests to verify the layered architecture migration:
1. Data Layer Integration Tests
2. Training Workflow Tests
3. Prediction Workflow Tests
4. Master Training Workflow Tests

Usage:
    source venv/bin/activate
    PYTHONPATH=/Users/pranav/Documents/basketball python tests/run_workflow_tests.py
"""

import sys
import os
import subprocess
import time

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)


def run_test_file(test_file: str) -> tuple:
    """
    Run a single test file and return (success, output).
    """
    test_path = os.path.join(script_dir, test_file)

    if not os.path.exists(test_path):
        return False, f"Test file not found: {test_path}"

    env = os.environ.copy()
    env['PYTHONPATH'] = project_root

    try:
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            env=env,
            cwd=project_root
        )

        output = result.stdout + result.stderr
        success = result.returncode == 0
        return success, output

    except subprocess.TimeoutExpired:
        return False, "Test timed out after 5 minutes"
    except Exception as e:
        return False, f"Error running test: {e}"


def main():
    """Run all workflow tests."""
    print("=" * 70)
    print("WORKFLOW INTEGRATION TEST SUITE")
    print("=" * 70)
    print("\nThis suite verifies all major workflows after the layered")
    print("architecture migration.\n")

    test_files = [
        ("Data Layer Integration", "test_data_layer_integration.py"),
        ("Training Workflow", "test_training_workflow.py"),
        ("Prediction Workflow", "test_prediction_workflow.py"),
        ("Master Training Workflow", "test_master_training_workflow.py"),
    ]

    results = []
    start_time = time.time()

    for name, test_file in test_files:
        print(f"\n{'=' * 70}")
        print(f"Running: {name}")
        print(f"File: {test_file}")
        print("=" * 70)

        test_start = time.time()
        success, output = run_test_file(test_file)
        test_duration = time.time() - test_start

        # Print output
        print(output)

        results.append({
            'name': name,
            'file': test_file,
            'success': success,
            'duration': test_duration
        })

        status = "PASSED" if success else "FAILED"
        print(f"\n{name}: {status} ({test_duration:.1f}s)")

    # Overall summary
    total_duration = time.time() - start_time
    passed = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])

    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    print(f"\nTotal test suites: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_duration:.1f}s")

    if failed > 0:
        print("\nFailed test suites:")
        for r in results:
            if not r['success']:
                print(f"  X {r['name']} ({r['file']})")

    print("\n" + "=" * 70)
    if failed == 0:
        print("ALL WORKFLOW TESTS PASSED")
        print("=" * 70)
        print("\nThe layered architecture migration is verified!")
        print("All major workflows are functioning correctly:")
        print("  - Data layer repositories work")
        print("  - Training pipeline works")
        print("  - Prediction pipeline works")
        print("  - Master training creation works")
        return 0
    else:
        print(f"WORKFLOW TESTS FAILED: {failed} suite(s) failed")
        print("=" * 70)
        print("\nPlease review the failed tests above and fix any issues.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
