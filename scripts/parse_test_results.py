#!/usr/bin/env python3
"""
Parse JUnit XML test results and generate GitHub-flavored summary.

This script parses pytest JUnit XML output and creates:
- Test result summary with pass/fail counts
- Slowest test identification
- Failure analysis with tracebacks
- GitHub Actions step summary formatting
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple


def parse_junit_xml(xml_path: Path) -> Dict:
    """Parse JUnit XML file and extract test results."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'errors': 0,
        'duration': 0.0,
        'failures': [],
        'slow_tests': [],
        'test_cases': []
    }

    # Parse testsuite attributes
    for testsuite in root.findall('.//testsuite'):
        results['total'] += int(testsuite.get('tests', 0))
        results['failed'] += int(testsuite.get('failures', 0))
        results['skipped'] += int(testsuite.get('skipped', 0))
        results['errors'] += int(testsuite.get('errors', 0))
        results['duration'] += float(testsuite.get('time', 0))

    # Parse individual test cases
    for testcase in root.findall('.//testcase'):
        name = testcase.get('name')
        classname = testcase.get('classname')
        time = float(testcase.get('time', 0))

        test_info = {
            'name': name,
            'classname': classname,
            'time': time,
            'status': 'passed'
        }

        # Check for failures
        failure = testcase.find('failure')
        if failure is not None:
            test_info['status'] = 'failed'
            test_info['message'] = failure.get('message', '')
            test_info['traceback'] = failure.text or ''
            results['failures'].append(test_info)

        # Check for errors
        error = testcase.find('error')
        if error is not None:
            test_info['status'] = 'error'
            test_info['message'] = error.get('message', '')
            test_info['traceback'] = error.text or ''
            results['failures'].append(test_info)

        # Check for skipped
        skipped = testcase.find('skipped')
        if skipped is not None:
            test_info['status'] = 'skipped'

        results['test_cases'].append(test_info)

        # Track slow tests (> 1 second)
        if time > 1.0:
            results['slow_tests'].append(test_info)

    results['passed'] = results['total'] - results['failed'] - results['skipped'] - results['errors']

    # Sort slow tests by duration
    results['slow_tests'].sort(key=lambda x: x['time'], reverse=True)

    return results


def generate_summary(results: Dict) -> str:
    """Generate GitHub-flavored markdown summary."""
    lines = []

    # Header
    lines.append("# Test Results Summary")
    lines.append("")

    # Overall stats
    total = results['total']
    passed = results['passed']
    failed = results['failed']
    skipped = results['skipped']
    errors = results['errors']
    duration = results['duration']

    pass_rate = (passed / total * 100) if total > 0 else 0

    # Status emoji
    if failed == 0 and errors == 0:
        status_emoji = "✅"
        status_text = "PASSED"
    else:
        status_emoji = "❌"
        status_text = "FAILED"

    lines.append(f"## {status_emoji} Status: {status_text}")
    lines.append("")
    lines.append(f"- **Total Tests:** {total}")
    lines.append(f"- **Passed:** {passed} ({pass_rate:.1f}%)")
    lines.append(f"- **Failed:** {failed}")
    lines.append(f"- **Skipped:** {skipped}")
    lines.append(f"- **Errors:** {errors}")
    lines.append(f"- **Duration:** {duration:.2f}s")
    lines.append("")

    # Failures section
    if results['failures']:
        lines.append("## ❌ Failures")
        lines.append("")
        for i, failure in enumerate(results['failures'][:10], 1):  # Limit to 10
            lines.append(f"### {i}. {failure['classname']}::{failure['name']}")
            lines.append("")
            lines.append(f"**Status:** {failure['status']}")
            lines.append("")
            if failure.get('message'):
                lines.append(f"**Message:** `{failure['message']}`")
                lines.append("")
            if failure.get('traceback'):
                lines.append("<details>")
                lines.append("<summary>Traceback</summary>")
                lines.append("")
                lines.append("```python")
                lines.append(failure['traceback'][:2000])  # Limit traceback length
                lines.append("```")
                lines.append("</details>")
                lines.append("")

    # Slow tests section
    if results['slow_tests']:
        lines.append("## 🐌 Slowest Tests (>1s)")
        lines.append("")
        lines.append("| Test | Duration |")
        lines.append("|------|----------|")
        for test in results['slow_tests'][:10]:  # Top 10
            name = f"{test['classname']}::{test['name']}"
            duration = f"{test['time']:.2f}s"
            lines.append(f"| `{name[:80]}` | {duration} |")
        lines.append("")

    # Performance insights
    if results['test_cases']:
        avg_time = sum(t['time'] for t in results['test_cases']) / len(results['test_cases'])
        lines.append("## 📊 Performance Insights")
        lines.append("")
        lines.append(f"- **Average test duration:** {avg_time:.3f}s")
        lines.append(f"- **Fastest test:** {min(t['time'] for t in results['test_cases']):.3f}s")
        lines.append(f"- **Slowest test:** {max(t['time'] for t in results['test_cases']):.3f}s")
        lines.append("")

    return "\n".join(lines)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: parse_test_results.py <junit-xml-file>")
        sys.exit(1)

    xml_path = Path(sys.argv[1])

    if not xml_path.exists():
        print(f"Error: File not found: {xml_path}")
        sys.exit(1)

    print(f"Parsing test results from: {xml_path}")

    try:
        results = parse_junit_xml(xml_path)
        summary = generate_summary(results)

        print(summary)

        # Exit with failure code if tests failed
        if results['failed'] > 0 or results['errors'] > 0:
            sys.exit(1)

    except Exception as e:
        print(f"Error parsing test results: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
