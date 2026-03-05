from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Dict, Any, List, Tuple

from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
RUNS_DIR = BASE_DIR / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)

AGENT_PATH = PROJECT_ROOT / "code" / "agent.py"
SETTINGS_FILE = BASE_DIR / "settings.json"

app = Flask(__name__, static_folder=str(BASE_DIR / "static"), static_url_path="")


def _is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
            if handle:
                exit_code = ctypes.c_ulong()
                kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
                kernel32.CloseHandle(handle)
                return exit_code.value == 259  # STILL_ACTIVE
            return False
        else:
            os.kill(pid, 0)
            return True
    except (OSError, PermissionError):
        return False

_TS_RE = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\s*")

_SOLVER_CONTENT_MARKERS = (
    ">>>>>>> First solution:",
    ">>>>>>> Corrected solution:",
)

_VERIFIER_CONTENT_MARKERS = (
    ">>>>>>> Verification results:",
    ">>>>>>>Bug report:",
)

_VERDICT_MARKER = ">>>>>>> Is verification good?"

_SKIP_MARKERS = (
    ">>>>>> Initial prompt.",
    ">>>>>>> Verification prompt:",
    ">>>>>>> New prompt:",
    ">>>>>>> Other prompts:",
)

_DUPLICATE_MARKERS = (
    ">>>>>>> Initial verification:",
    ">>>>>>> verify results:",
)

_DONE_MARKERS = (
    ">>>>>>> Correct solution found.",
    ">>>>>>> Failed in finding a correct solution.",
    ">>>>>>> Failed in finding a complete solution.",
)

_SYSTEM_MARKERS = (
    ">>>>>>> Self improvement start:",
    ">>>>>>> Start verification.",
    ">>>>>>> Vefify the solution.",
    ">>>>>>> Verify the solution.",
    ">>>>>>> Verification does not pass, correcting ...",
    ">>>>>>> Solution is good, verifying again ...",
    ">>>>>>> Correct solution found.",
    ">>>>>>> Failed in finding a correct solution.",
    ">>>>>>> Failed in finding a complete solution.",
)


def _strip_ts(line: str) -> str:
    return _TS_RE.sub("", line)


def _try_json_loads(line: str) -> str | None:
    """Attempt to decode a JSON-encoded string on a single line."""
    s = line.strip()
    if not s.startswith('"'):
        return None
    try:
        return json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None


def parse_agent_log(log_text: str) -> Tuple[List[Dict[str, Any]], bool, str, str, Dict[str, int]]:
    """Parse an agent log into structured messages.

    Returns (messages, done, phase, detail_phase, token_usage) where:
    - messages: list of {"role": "solver"|"verifier"|"system", "content": str, "params"?: dict}
    - done: whether the agent has finished
    - phase: "idle" | "api_waiting" | "running"
    - detail_phase: granular phase such as "solving", "verifying", "correcting", etc.
    """
    messages: List[Dict[str, Any]] = []
    done = False
    phase = "idle"
    detail_phase = "idle"
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_all_tokens = 0
    lines = log_text.split("\n")
    i = 0
    n = len(lines)

    if n > 1:
        phase = "running"

    while i < n:
        raw = lines[i]
        stripped = _strip_ts(raw).rstrip()

        if stripped == "Sending request to API...":
            phase = "api_waiting"
            i += 1
            continue

        if not stripped.startswith(">>>>>") and not stripped.startswith("Number of iterations:"):
            i += 1
            continue

        phase = "running"

        if stripped.startswith(">>>>>>> TOKEN_USAGE:"):
            usage_match = re.search(
                r"prompt=(\d+)\s+completion=(\d+)\s+total=(\d+)",
                stripped,
            )
            if usage_match:
                total_prompt_tokens += int(usage_match.group(1))
                total_completion_tokens += int(usage_match.group(2))
                total_all_tokens += int(usage_match.group(3))
            i += 1
            continue

        # --- Content markers whose NEXT LINE is a JSON string to decode ---

        if any(stripped.startswith(m) for m in _SOLVER_CONTENT_MARKERS):
            i += 1
            if i < n:
                text = _try_json_loads(lines[i])
                if text:
                    doc_match = re.search(
                        r"(\\documentclass.*\\end\{document\})",
                        text, flags=re.DOTALL)
                    display_text = doc_match.group(1).strip() if doc_match else text
                    messages.append({"role": "solver", "content": display_text})
                i += 1
            continue

        if any(stripped.startswith(m) for m in _VERIFIER_CONTENT_MARKERS):
            i += 1
            if i < n:
                text = _try_json_loads(lines[i])
                if text is not None and text.strip():
                    messages.append({"role": "verifier", "content": text})
                i += 1
            continue

        if stripped.startswith(_VERDICT_MARKER):
            i += 1
            verdict_text = ""
            if i < n:
                v = _try_json_loads(lines[i])
                if v is not None:
                    verdict_text = v
                i += 1
            passed = "yes" in verdict_text.lower() if verdict_text else False
            key = "verdict_pass" if passed else "verdict_fail"
            messages.append({"role": "system", "content": key})
            continue

        # --- Skip markers ---

        if any(stripped.startswith(m) for m in _SKIP_MARKERS):
            if stripped.startswith(">>>>>> Initial prompt"):
                detail_phase = "solving"
            i += 1
            while i < n:
                peek = _strip_ts(lines[i]).rstrip()
                if peek.startswith(">>>>>") or peek.startswith("Number of iterations:"):
                    break
                i += 1
            continue

        # --- Duplicate markers ---

        if any(stripped.startswith(m) for m in _DUPLICATE_MARKERS):
            i += 1
            if i < n and lines[i].strip().startswith('"'):
                i += 1
            continue

        # --- Done markers ---

        if stripped.startswith(">>>>>>> Correct solution found."):
            done = True
            detail_phase = "done"
            messages.append({"role": "system", "content": "correct_solution_found"})
            i += 1
            if i < n and lines[i].strip().startswith('"'):
                i += 1
            continue

        if stripped.startswith(">>>>>>> Found a correct solution in run"):
            done = True
            detail_phase = "done"
            run_match = re.search(r"run (\d+)", stripped)
            run_num = run_match.group(1) if run_match else "?"
            messages.append({"role": "system", "content": "found_correct_in_run",
                             "params": {"run": run_num}})
            i += 1
            if i < n and lines[i].strip().startswith('"'):
                i += 1
            continue

        if any(stripped.startswith(m) for m in _DONE_MARKERS) and "Correct solution found" not in stripped:
            done = True
            detail_phase = "done"
            messages.append({"role": "system", "content": "no_correct_solution"})
            i += 1
            continue

        if stripped.startswith(">>>>>>> Error in run"):
            run_match = re.search(r"run (\d+)", stripped)
            run_num = run_match.group(1) if run_match else "?"
            err_match = re.search(r":\s*(.+)", stripped)
            err_msg = err_match.group(1).strip() if err_match else ""
            messages.append({"role": "system", "content": "error_in_run",
                             "params": {"run": run_num, "error": err_msg}})
            i += 1
            continue

        # --- Run header ---

        if ">>>>>>>>>>>>>>>>>>>>>>>>>> Run" in stripped:
            run_match = re.search(r"Run (\d+) of (\d+)", stripped)
            if run_match:
                messages.append({"role": "system", "content": "run_header",
                                 "params": {"run": run_match.group(1),
                                            "total": run_match.group(2)}})
            i += 1
            continue

        # --- Iteration counter ---

        if stripped.startswith("Number of iterations:"):
            iter_match = re.search(r"iterations:\s*(\d+).*?corrects:\s*(\d+).*?errors:\s*(\d+)", stripped)
            if iter_match:
                messages.append({"role": "system", "content": "iteration_status",
                                 "params": {"iter": iter_match.group(1),
                                            "corrects": iter_match.group(2),
                                            "errors": iter_match.group(3)}})
            else:
                messages.append({"role": "system", "content": "iteration_status",
                                 "params": {"raw": stripped}})
            i += 1
            continue

        # --- System markers with detail_phase tracking ---

        if any(stripped.startswith(m) for m in _SYSTEM_MARKERS):
            clean = stripped.lstrip("> ").rstrip(". ").strip()
            _PHASE_MAP = {
                "Self improvement start": ("self_improving", "self_improving"),
                "Start verification": ("verifying", "start_verification"),
                "Vefify the solution": ("verifying", "verifying_solution"),
                "Verify the solution": ("verifying", "verifying_solution"),
                "Verification does not pass, correcting": ("correcting", "verification_failed_correcting"),
                "Solution is good, verifying again": ("re_verifying", "solution_good_reverifying"),
            }
            msg_key = clean
            for eng, (dp, key) in _PHASE_MAP.items():
                if eng in clean:
                    detail_phase = dp
                    msg_key = key
                    break
            messages.append({"role": "system", "content": msg_key})
            i += 1
            continue

        i += 1

    token_usage = {
        "prompt": total_prompt_tokens,
        "completion": total_completion_tokens,
        "total": total_all_tokens,
    }
    return messages, done, phase, detail_phase, token_usage


def _extract_latex_document(text: str) -> str:
    pattern = r"(\\documentclass[^\n]{0,80}\n.*\\end\{document\})"
    match = re.search(pattern, text, flags=re.DOTALL)
    if match and r"\begin{document}" in match.group(1):
        return match.group(1).strip()
    return ""


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _get_default_prompts() -> Dict[str, str]:
    """Import prompt defaults from agent.py at runtime."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("agent_module", str(AGENT_PATH))
    mod = importlib.util.module_from_spec(spec)
    mod.__name__ = "agent_module"
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    return {
        "step1_prompt": getattr(mod, "step1_prompt", ""),
        "self_improvement_prompt": getattr(mod, "self_improvement_prompt", ""),
        "correction_prompt": getattr(mod, "correction_prompt", ""),
        "verification_system_prompt": getattr(mod, "verification_system_prompt", ""),
        "verification_remider": getattr(mod, "verification_remider", ""),
        "check_verification_prompt": getattr(mod, "check_verification_prompt", ""),
    }


_DEFAULT_API = {
    "base_url": "https://llm-api-jpe.dou.chat",
    "model_name": "google/gemini-3-pro-preview",
    "api_key": "",
    "temperature": 0.1,
    "max_tokens": 24576,
}

_cached_default_prompts: Dict[str, str] | None = None


def _load_settings() -> Dict[str, Any]:
    """Load merged settings: saved values on top of defaults."""
    global _cached_default_prompts
    if _cached_default_prompts is None:
        _cached_default_prompts = _get_default_prompts()

    saved = _read_json(SETTINGS_FILE)
    return {
        "api": {**_DEFAULT_API, **saved.get("api", {})},
        "prompts": {**_cached_default_prompts, **saved.get("prompts", {})},
    }


def _save_settings(data: Dict[str, Any]) -> None:
    _write_json(SETTINGS_FILE, data)


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/settings")
def get_settings():
    settings = _load_settings()
    safe = {
        "api": {k: v for k, v in settings["api"].items() if k != "api_key"},
        "prompts": settings["prompts"],
        "default_prompts": (_cached_default_prompts or _get_default_prompts()),
        "has_api_key": bool(settings["api"].get("api_key")),
    }
    return jsonify(safe)


@app.post("/settings")
def post_settings():
    data = request.get_json(silent=True) or {}
    current = _load_settings()

    if "api" in data:
        api_data = data["api"] or {}
        for k in ("base_url", "model_name"):
            if k in api_data:
                current["api"][k] = str(api_data[k] or "").strip()

        if "temperature" in api_data:
            try:
                current["api"]["temperature"] = float(api_data["temperature"])
            except (TypeError, ValueError):
                pass

        if "max_tokens" in api_data:
            try:
                current["api"]["max_tokens"] = int(api_data["max_tokens"])
            except (TypeError, ValueError):
                pass

        key_mode = str(api_data.get("api_key_mode", "")).strip().lower()
        if key_mode == "clear":
            current["api"]["api_key"] = ""
        elif key_mode == "set":
            current["api"]["api_key"] = str(api_data.get("api_key", "") or "").strip()
        elif "api_key" in api_data:
            current["api"]["api_key"] = str(api_data.get("api_key", "") or "").strip()

    if "prompts" in data:
        for k in current["prompts"]:
            if k in data["prompts"]:
                current["prompts"][k] = data["prompts"][k]

    _save_settings(current)
    return jsonify({"ok": True})


@app.post("/stop")
def stop_agent():
    payload = request.get_json(silent=True) or {}
    run_id = (payload.get("run_id") or "").strip()
    if not run_id:
        return jsonify({"ok": False, "reason": "run_id is required"}), 400

    meta = _read_json(RUNS_DIR / run_id / "meta.json")
    pid = meta.get("pid", 0)
    if not pid:
        print(f"[stop] no pid found for run_id={run_id}")
        return jsonify({"ok": False, "reason": "no pid"})

    alive_before = _is_pid_alive(pid)
    print(f"[stop] run_id={run_id}, pid={pid}, alive_before={alive_before}")

    try:
        if sys.platform == "win32":
            ret = subprocess.call(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            print(f"[stop] taskkill returned {ret}")
        else:
            os.kill(pid, signal.SIGTERM)
    except OSError as e:
        print(f"[stop] OSError: {e}")
        return jsonify({"ok": False, "reason": str(e)})

    return jsonify({"ok": True})


@app.post("/run")
def run_agent():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400

    run_id = uuid.uuid4().hex
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    problem_file = run_dir / "problem.txt"
    log_file = run_dir / "agent.log"
    memory_file = run_dir / "memory.json"
    meta_file = run_dir / "meta.json"
    config_file = run_dir / "config.json"

    problem_file.write_text(question, encoding="utf-8")

    settings = _load_settings()
    _write_json(config_file, settings)

    cmd = [
        sys.executable,
        str(AGENT_PATH),
        str(problem_file),
        "--log",
        str(log_file),
        "--memory",
        str(memory_file),
        "--config",
        str(config_file),
    ]
    env = os.environ.copy()
    api_key = settings["api"].get("api_key", "")
    if api_key:
        env["OPENAI_API_KEY"] = api_key

    stderr_log = run_dir / "stderr.log"
    stderr_fh = stderr_log.open("w", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        cwd=str(PROJECT_ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=stderr_fh,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )

    _write_json(
        meta_file,
        {
            "run_id": run_id,
            "pid": proc.pid,
            "problem_file": str(problem_file),
            "log_file": str(log_file),
            "memory_file": str(memory_file),
        },
    )

    return jsonify({"run_id": run_id, "log_path": str(log_file)})


@app.get("/log")
def read_log():
    run_id = request.args.get("run_id", "").strip()
    after = int(request.args.get("after", "0"))
    if not run_id:
        return jsonify({"error": "run_id is required"}), 400

    run_dir = RUNS_DIR / run_id
    meta = _read_json(run_dir / "meta.json")
    pid = meta.get("pid", 0)
    alive = _is_pid_alive(pid)

    log_file_str = meta.get("log_file", "")
    log_path = Path(log_file_str) if log_file_str else None
    if not log_path or not log_path.exists():
        status = "starting" if alive else "no_log"
        return jsonify({"messages": [], "done": not alive, "total": 0,
                        "alive": alive, "phase": "idle", "status": status,
                        "token_usage": {"prompt": 0, "completion": 0, "total": 0}})

    text = log_path.read_text(encoding="utf-8", errors="ignore")
    all_msgs, done, phase, detail_phase, token_usage = parse_agent_log(text)

    if not alive and not done:
        done = True

    new_msgs = all_msgs[after:]
    return jsonify({
        "messages": new_msgs,
        "total": len(all_msgs),
        "done": done,
        "alive": alive,
        "phase": phase,
        "detail_phase": detail_phase,
        "token_usage": token_usage,
    })


@app.get("/result")
def get_result():
    run_id = request.args.get("run_id", "").strip()
    if not run_id:
        return jsonify({"error": "run_id is required"}), 400

    run_dir = RUNS_DIR / run_id
    meta = _read_json(run_dir / "meta.json")
    log_file_str = meta.get("log_file", "")
    log_path = Path(log_file_str) if log_file_str else None
    if not log_path or not log_path.exists():
        return jsonify({"latex": ""})

    text = log_path.read_text(encoding="utf-8", errors="ignore")

    latex = ""
    last_solver_content = ""
    all_msgs, _, _, _, _ = parse_agent_log(text)
    for msg in reversed(all_msgs):
        if msg["role"] == "solver":
            if not last_solver_content:
                last_solver_content = msg["content"]
            doc_match = re.search(
                r"(\\documentclass.*\\end\{document\})",
                msg["content"],
                flags=re.DOTALL,
            )
            if doc_match:
                latex = doc_match.group(1).strip()
                break

    # Fallback for failed/incomplete runs: show the latest solver output.
    if not latex and last_solver_content:
        reqno_start = last_solver_content.find(r"\documentclass[reqno]{amsart}")
        generic_start = last_solver_content.find(r"\documentclass")
        start_idx = reqno_start if reqno_start != -1 else generic_start
        if start_idx != -1:
            tail = last_solver_content[start_idx:]
            end_idx = tail.find(r"\end{document}")
            if end_idx != -1:
                latex = tail[:end_idx + len(r"\end{document}")].strip()
            else:
                latex = tail.strip()
        else:
            latex = last_solver_content.strip()

    if not latex:
        latex = _extract_latex_document(text)

    return jsonify({"latex": latex})



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False, threaded=True)
