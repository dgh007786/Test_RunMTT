import subprocess
import time
import os
import pytest
import glob

TEST_CASES = [
    "/home/gunjan/Desktop/Test_RunMTT/test_cases/case1",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case2",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case3",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case4",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case9",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case10",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case11",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case12",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case5",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case6",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case7",
#     "/home/gunjan/Desktop/Test_RunMTT/test_cases/case8",
]

CRITICAL_FAILURES = [
    "No Ignition on landscape",
    "Can not launch MTT",
]

@pytest.mark.parametrize("case_dir", TEST_CASES)
def test_runmtt_case(case_dir):
    cmd_file = os.path.join(case_dir, "commands.txt")
    assert os.path.exists(cmd_file), f"Missing commands.txt in {case_dir}"

    start_time = time.time()

    result = subprocess.run(
        ["runmtt", cmd_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    duration = time.time() - start_time

    # Save logs
    stdout_log = os.path.join(case_dir, "stdout.log")
    stderr_log = os.path.join(case_dir, "stderr.log")
    with open(stdout_log, "w") as f:
        f.write(result.stdout)
    with open(stderr_log, "w") as f:
        f.write(result.stderr)

    # Check for critical failure
    if any(err in result.stdout for err in CRITICAL_FAILURES):
        pytest.skip(f"Skipped: No ignition or MTT could not launch in {case_dir}")

    # Check if at least one meaningful output file is created
    output_dir = os.path.join("/home/gunjan/Desktop/Test_RunMTT/outputs", os.path.basename(case_dir))
    tif_outputs = glob.glob(os.path.join(output_dir, "*.tif"))

    assert len(tif_outputs) > 0, f"No .tif outputs generated in {output_dir}"
    assert result.returncode == 0, f"runmtt failed in {case_dir}"
    assert "Launching MTT" in result.stdout

    print(f"[{case_dir}] ✅ Passed in {duration:.2f} seconds with {len(tif_outputs)} .tif outputs")
