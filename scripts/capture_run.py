"""Run one project-local Python simulation and preserve its inputs, logs and JSON result."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone


def sha(data):
    return hashlib.sha256(data).hexdigest()


def under(root, name):
    if not name or Path(name).is_absolute():
        raise ValueError(f"expected a project-relative path: {name}")
    resolved = (root / name).resolve()
    if root not in resolved.parents:
        raise ValueError(f"path outside case: {name}")
    return resolved


def bad_number(value):
    raise ValueError(f"non-finite measurement: {value}")


def finite_json(raw):
    data = json.loads(raw.decode("utf-8-sig"), parse_constant=bad_number)

    def verify(value):
        if isinstance(value, float) and not math.isfinite(value):
            bad_number(value)
        if isinstance(value, dict):
            for v in value.values():
                verify(v)
        if isinstance(value, list):
            for v in value:
                verify(v)
    verify(data)
    if data is None or data == [] or data == {} or isinstance(data, str):
        raise ValueError("missing structured scientific output")
    return data


def capture(root, run_id, script, inputs, argv, timeout):
    root = root.resolve()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", run_id):
        raise ValueError("invalid run ID")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be positive and finite")
    program = under(root, script)
    if program.suffix.lower() != ".py" or not program.is_file():
        raise ValueError("expected existing local Python entry point")
    files = {n: under(root, n) for n in dict.fromkeys([script, *inputs])}
    digests = {n: sha(path.read_bytes()) for n, path in files.items()}
    run_dir = under(root, "runs/" + run_id)
    run_dir.mkdir(parents=True, exist_ok=False)
    receipt = {"run_id": run_id, "started": datetime.now(timezone.utc).isoformat(),
               "entry": script, "arguments": argv, "python": sys.version.split()[0],
               "timeout_s": timeout, "inputs": digests, "status": "started"}
    path = run_dir / "receipt.json"

    def persist():
        temp = run_dir / "receipt.tmp"
        temp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temp, path)

    persist()
    out, err = b"", b""
    try:
        proc = subprocess.run([sys.executable, str(program), *argv], cwd=root,
                              capture_output=True, timeout=timeout)
        out, err = proc.stdout, proc.stderr
        receipt["exit_code"] = proc.returncode
        if proc.returncode:
            receipt["status"] = "process_failed"
        else:
            finite_json(out)
            if any(sha(f.read_bytes()) != digests[n] for n, f in files.items()):
                raise ValueError("declared input changed during the run")
            (run_dir / "result.json").write_bytes(out)
            receipt.update(status="recorded", result_sha256=sha(out))
    except subprocess.TimeoutExpired as exc:
        out, err = exc.stdout or b"", exc.stderr or b""
        receipt["status"] = "timeout"
    except (ValueError, OSError) as exc:
        receipt.update(status="invalid_output_or_input", detail=str(exc))
    (run_dir / "stdout.log").write_bytes(out)
    (run_dir / "stderr.log").write_bytes(err)
    receipt["finished"] = datetime.now(timezone.utc).isoformat()
    persist()
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--script", required=True, help="project-relative Python entry")
    parser.add_argument("--input", action="append", default=[], help="additional project-relative input")
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.args[1:] if args.args[:1] == ["--"] else args.args
    try:
        receipt = capture(args.case, args.run_id, args.script, args.input, argv, args.timeout)
        print(f"{receipt['run_id']} {receipt['status']}")
        return 0 if receipt["status"] == "recorded" else 1
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
