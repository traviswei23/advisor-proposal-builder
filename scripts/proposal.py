"""Validate a research decision brief and render its evidence and test plan."""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


def empty():
    return {"version": 1, "title": "", "question": "", "value": "", "decision": "",
            "constraint": "", "allowed_modes": [], "sources": [], "hypotheses": [],
            "routes": [], "tests": [], "choice": "", "tradeoff": "", "fallback": "",
            "objection": "", "reply": "", "next_milestone": ""}


def has_text(value):
    return isinstance(value, str) and bool(value.strip())


def require(row, names, where, issues):
    for key in names.split():
        if not has_text(row.get(key)):
            issues.append(f"{where}: missing {key}")


def table(case, key, fields, issues):
    rows = case.get(key)
    if not isinstance(rows, list):
        raise ValueError(f"{key}: expected array")
    out = {}
    for row in rows:
        if not isinstance(row, dict) or not has_text(row.get("id")) or row["id"] in out:
            raise ValueError(f"{key}: invalid or duplicate id")
        require(row, fields, row["id"], issues)
        out[row["id"]] = row
    if not out:
        issues.append(f"no {key}")
    return out


def references(row, key, known, issues):
    values = row.get(key)
    if not isinstance(values, list) or not values or any(not has_text(v) or v not in known for v in values):
        issues.append(f"{row['id']}: missing or unknown {key}")
        return set()
    return set(values)


def local_file(root, name):
    if not has_text(name) or Path(name).is_absolute():
        return False
    path = (root / name).resolve()
    return root in path.parents and path.is_file() and path.stat().st_size > 0


def verify_measurements(row, root, issues):
    """Bind displayed numerical readings to explicitly selected JSON cells."""
    artifact = root / row["artifact"]
    receipt_name = row.get("run_receipt")
    if receipt_name:
        if not local_file(root, receipt_name):
            issues.append(f"{row['id']}: missing run receipt")
        else:
            receipt = json.loads((root / receipt_name).read_text(encoding="utf-8-sig"))
            if (receipt.get("status") != "recorded" or receipt.get("result_sha256") !=
                    hashlib.sha256(artifact.read_bytes()).hexdigest()):
                issues.append(f"{row['id']}: receipt does not match observed artifact")
    bindings = row.get("measurements", [])
    if not isinstance(bindings, list):
        raise ValueError("measurements must be an array")
    if not bindings:
        return
    raw = json.loads(artifact.read_text(encoding="utf-8-sig"))
    for binding in bindings:
        value = raw
        path, digits = binding["path"], binding["digits"]
        if not isinstance(path, list) or type(digits) is not int or not 0 <= digits <= 12:
            raise ValueError("expected JSON key/index path and digits in 0..12")
        for part in path:
            if not isinstance(part, str) and not (type(part) is int and part >= 0):
                raise ValueError("invalid measurement path")
            value = value[part]
        if type(value) not in (float, int) or not math.isfinite(value):
            raise ValueError("expected a finite measurement")
        expected = format(value, f".{digits}f")
        phrase = binding.get("phrase", "{value}")
        if not isinstance(phrase, str) or phrase.count("{value}") != 1:
            raise ValueError("measurement phrase must include exactly one {value}")
        prefix, suffix = phrase.split("{value}")
        token = r"(?<![0-9.+−-])" + re.escape(expected) + r"(?![0-9.]|[eE][+-]?[0-9])"
        pattern = re.escape(prefix) + token + re.escape(suffix)
        if binding.get("display") != expected or not re.search(pattern, row["result"]):
            issues.append(f"{row['id']}: reported number differs from the bound result cell")


def validate(case, root):
    if not isinstance(case, dict) or type(case.get("version")) is not int or case["version"] != 1:
        raise ValueError("unsupported proposal format")
    issues = []
    require(case, "title question value decision constraint choice tradeoff fallback objection reply next_milestone",
            "proposal", issues)
    modes = case.get("allowed_modes")
    supported = {"simulation", "analytic", "existing_data", "field", "laboratory", "qualitative", "other"}
    if not isinstance(modes, list) or not modes or any(not has_text(m) or m not in supported for m in modes):
        raise ValueError("set allowed_modes from the project scope")
    sources = table(case, "sources", "work location use level", issues)
    for key, source in sources.items():
        if source.get("level") not in {"original", "abstract", "metadata", "user_record"}:
            issues.append(f"{key}: unknown source level")
        ref = source.get("ref", "")
        if not has_text(ref) or not ((urlsplit(ref).scheme in {"https", "http"} and urlsplit(ref).netloc)
                                    or local_file(root, ref)):
            issues.append(f"{key}: give a public source URL or a nonempty case-relative artifact")
    hypotheses = table(case, "hypotheses", "explanation prediction", issues)
    if len(hypotheses) < 2:
        issues.append("the main explanation needs a rival or a null model")
    for row in hypotheses.values():
        references(row, "sources", sources, issues)
    routes = table(case, "routes", "method resources role", issues)
    if case.get("choice") not in routes:
        issues.append("chosen route not in routes")
    if not any(r.get("role") == "baseline" for r in routes.values()):
        issues.append("no baseline route")
    tests = table(case, "tests", "action observable controls resolution resources proceed pivot inconclusive", issues)
    linked = set()
    chosen_tested = False
    for key, row in tests.items():
        compared = references(row, "routes", routes, issues)
        predicts = references(row, "hypotheses", hypotheses, issues)
        purpose = row.get("purpose", "discriminate")
        if purpose == "discriminate":
            linked.update(predicts)
            chosen_tested |= case.get("choice") in compared
            if not any(routes[r].get("role") == "baseline" for r in compared) or len(compared) < 2:
                issues.append(f"{key}: compare with an explicit baseline")
            if len(predicts) < 2:
                issues.append(f"{key}: test must distinguish explanations")
        elif purpose not in {"sanity", "calibration"}:
            issues.append(f"{key}: unknown test purpose")
        if row.get("mode") not in modes:
            issues.append(f"{key}: test outside allowed modes")
        if row.get("state") not in {"planned", "observed"}:
            issues.append(f"{key}: invalid test state")
        if row.get("state") == "observed":
            if not has_text(row.get("result")) or not local_file(root, row.get("artifact")):
                issues.append(f"{key}: observed result lacks an inspectable artifact or reading")
            else:
                verify_measurements(row, root, issues)
        elif any(row.get(k) for k in ("result", "artifact", "measurements", "run_receipt")):
            issues.append(f"{key}: separate observed results from proposed work")
        decisions = {str(row.get(k, "")).strip().casefold() for k in ("proceed", "pivot", "inconclusive")}
        if len(decisions) < 3:
            issues.append(f"{key}: indistinguishable decision rules")
    if set(hypotheses) != linked:
        issues.append("some hypotheses have no distinguishing test")
    if not chosen_tested:
        issues.append("chosen route has no test")
    return issues


def render(case):
    lines = [f"# {case['title']}", "", f"**会议要决定的事**　{case['decision']}", "",
             f"{case['question']} {case['value']}", "", f"**范围和资源**　{case['constraint']}",
             "", "## 依据与竞争解释", ""]
    for s in case["sources"]:
        lines.append(f"- {s['id']}　{s['work']}，{s['location']}。{s['use']} [来源]({s['ref']})")
    for h in case["hypotheses"]:
        lines.extend(["", f"**{h['id']}**　{h['explanation']} 预测为{h['prediction']}（依据 {', '.join(h['sources'])}）。"])
    lines.extend(["", "## 路线与判别试验", ""])
    for r in case["routes"]:
        lines.append(f"- {r['id']}　{r['method']} 所需资源为{r['resources']}。")
    for t in case["tests"]:
        purpose = t.get("purpose", "discriminate")
        if purpose == "discriminate":
            role = f"对照 {', '.join(t['routes'])}，区分 {', '.join(t['hypotheses'])}。"
        else:
            label = "实现自检" if purpose == "sanity" else "校准"
            role = f"{label}涉及路线 {', '.join(t['routes'])}，服务于 {', '.join(t['hypotheses'])}。"
        lines.extend(["", f"**{t['id']}**　{t['action']} {role}",
                      "", f"记录{t['observable']}。固定{t['controls']}。分辨条件为{t['resolution']}。所需资源为{t['resources']}。",
                      "", f"- 继续的条件和动作　{t['proceed']}", f"- 转向的条件和动作　{t['pivot']}",
                      f"- 无法区分时　{t['inconclusive']}"])
        if t["state"] == "observed":
            lines.append(f"- 已执行　{t['result']} [原始记录]({t['artifact']})")
        else:
            lines.append("- 计划中，尚无观测结果。")
    lines.extend(["", "## 建议导师决定", "", f"优先选择 {case['choice']}。{case['tradeoff']}",
                  "", f"备选及触发条件　{case['fallback']}", "",
                  f"最强质疑　{case['objection']}", "", f"当前回应　{case['reply']}",
                  "", f"下一里程碑　{case['next_milestone']}"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "check", "brief"))
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    file = args.file.resolve()
    try:
        if args.command == "init":
            file.parent.mkdir(parents=True, exist_ok=True)
            with file.open("x", encoding="utf-8") as stream:
                json.dump(empty(), stream, ensure_ascii=False, indent=2)
            return 0
        data = json.loads(file.read_text(encoding="utf-8-sig"))
        issues = validate(data, file.parent)
        if issues:
            print("\n".join(issues), file=sys.stderr)
            return 1
        print(render(data) if args.command == "brief" else "PLAN RECORDS CONSISTENT", end="\n")
        return 0
    except (ValueError, OSError, IndexError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
