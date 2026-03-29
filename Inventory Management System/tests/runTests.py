from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _extract_pytest_summary(output: str) -> str:
	"""Return the final pytest summary line when available."""
	for line in reversed(output.splitlines()):
		text = line.strip()
		if text.startswith("===") and ("passed" in text or "failed" in text or "error" in text):
			return text
	return "No pytest summary found."


def _extract_collected_count(output: str) -> str:
	match = re.search(r"collected\s+(\d+)\s+items?", output)
	if match:
		return match.group(1)
	return "unknown"


def _build_pytest_command() -> list[str] | None:
	"""Pick a pytest launcher that exists in the current environment."""
	# First choice: pytest from the current interpreter.
	if shutil.which(sys.executable):
		check = subprocess.run(
			[sys.executable, "-m", "pytest", "--version"],
			capture_output=True,
			text=True,
		)
		if check.returncode == 0:
			return [sys.executable, "-m", "pytest"]

	# Fallback: pytest CLI available on PATH (often points to another Python env).
	pytest_cli = shutil.which("pytest")
	if pytest_cli:
		return [pytest_cli]

	return None


def run_suite(name: str, target: Path, pytest_base_cmd: list[str], project_root: Path) -> dict:
	start = time.perf_counter()
	cmd = pytest_base_cmd + [str(target), "-v"]
	result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_root))
	duration = time.perf_counter() - start

	combined_output = (result.stdout or "") + "\n" + (result.stderr or "")
	summary = _extract_pytest_summary(combined_output)
	collected = _extract_collected_count(combined_output)
	passed = result.returncode == 0

	print("\n" + "=" * 72)
	print(f"Suite: {name}")
	print(f"Target: {target}")
	print(f"Collected tests: {collected}")
	print(f"Status: {'PASSED' if passed else 'FAILED'}")
	print(f"Duration: {duration:.2f}s")
	print(f"Pytest summary: {summary}")
	print("-" * 72)
	print("Detailed output:")
	print(result.stdout.strip() or "<no stdout>")
	if result.stderr.strip():
		print("\nStderr:")
		print(result.stderr.strip())

	return {
		"name": name,
		"target": str(target),
		"status": "PASSED" if passed else "FAILED",
		"duration": duration,
		"summary": summary,
	}


def main() -> int:
	tests_dir = Path(__file__).resolve().parent
	project_root = tests_dir.parent
	pytest_base_cmd = _build_pytest_command()

	if pytest_base_cmd is None:
		print("Could not find pytest in this Python environment or on PATH.")
		print("Install pytest, then run this script again.")
		return 1

	suites = [
		("Unit Tests", tests_dir / "unit"),
		("Integration Tests", tests_dir / "integration"),
		("Regression Tests", tests_dir / "regression"),
	]

	print("Starting Inventory Management System test run...")
	print(f"Using pytest launcher: {' '.join(pytest_base_cmd)}")
	results = [run_suite(name, target, pytest_base_cmd, project_root) for name, target in suites]

	print("\n" + "#" * 72)
	print("Overall Test Summary")
	print("#" * 72)

	failed = 0
	total_duration = 0.0
	for item in results:
		total_duration += item["duration"]
		print(
			f"- {item['name']}: {item['status']} | "
			f"{item['duration']:.2f}s | {item['summary']}"
		)
		if item["status"] == "FAILED":
			failed += 1

	print(f"\nTotal runtime: {total_duration:.2f}s")
	if failed:
		print(f"Final result: FAILED ({failed} suite(s) failed)")
		return 1

	print("Final result: PASSED (all suites passed)")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
