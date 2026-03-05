/* ===== i18n translations ===== */

const TRANSLATIONS = {
  zh: {
    app_title: "数学科研小助手",
    app_subtitle: "用于辅助解决研究中遇到的数学问题。",
    input_problem: "输入问题",
    input_placeholder: "在此输入题目（LaTeX 格式）...",
    run_btn: "一键运行",
    stop_btn: "中断",
    status_idle: "未运行",
    status_stopped: "已中断",
    status_starting: "Agent 正在启动",
    status_waiting_first: "Agent 已启动，等待首次响应",
    status_no_output: "Agent 进程已结束（无输出，可能启动失败）",
    status_done: "求解完成",
    status_no_question: "请先输入问题",
    status_start_failed: "启动失败",
    solve_verify_title: "求解 & 验证对话",
    latex_output_title: "最终LaTeX输出（可直接粘贴到Overleaf，编译为完整PDF）",
    latex_placeholder: "求解完成后，完整 LaTeX 文档将在此显示...",
    copy_latex: "复制 LaTeX",
    copy: "复制",
    copied: "已复制!",
    settings_title: "设置",
    tab_prompts: "提示词设置",
    tab_api: "模型 API 设置",
    prompt_step1_label: "主求解提示",
    prompt_step1_desc: "指导模型以 LaTeX 论文格式输出研究级数学问题的解答，包含严谨性、诚实性、LaTeX 文档结构、引用规范和自检要求。",
    prompt_self_improve_label: "自改进提示",
    prompt_self_improve_desc: "首轮输出后要求模型复查并修正错误、填补论证漏洞，继续探索更深入的解答。",
    prompt_correction_label: "修正提示",
    prompt_correction_desc: "根据验证器的 bug report 改进解答，或对不认同的项给出详细解释以避免误解。",
    prompt_verify_sys_label: "验证系统提示",
    prompt_verify_sys_desc: "指导验证器作为数学专家严格验证解答，区分 Critical Error 与 Justification Gap，输出 Summary 和 Detailed Verification Log。",
    prompt_verify_reminder_label: "验证任务提醒",
    prompt_verify_reminder_desc: "提醒验证器关注 LaTeX 论文中的 Solution 部分，生成 summary 和 step-by-step verification log。",
    prompt_check_verify_label: "验证复核提示",
    prompt_check_verify_desc: "让验证器复核 findings 是否过严，引用是否准确。此提示词在当前代码中被注释未启用。",
    badge_disabled: "当前未启用",
    save_prompts: "保存提示词",
    reset_prompts: "恢复默认",
    save_api: "保存 API 设置",
    api_key_keep_hint: "留空表示保持当前已保存密钥不变。",
    api_key_saved_hint: "检测到已保存 API Key。留空保持不变；勾选可清空。",
    clear_api_key: "清空已保存 API Key",
    recommend_note: "推荐使用 gemini-3-pro-preview 或更新的系列模型以获得最佳体验。",
    pipeline_diagram: "Pipeline 架构图",
    model_name_label: "Model Name",
    saved: "已保存",
    save_failed: "保存失败",
    reset_done: "已恢复默认（未保存）",
    waiting_ai: "正在等待 AI 模型响应，请耐心等待...",
    tokens_unit: "tokens",
    role_solver: "求解器",
    role_verifier: "验证器",
    // detail_phase labels
    phase_solving: "求解中",
    phase_self_improving: "自我改进中",
    phase_verifying: "验证中",
    phase_correcting: "修正解答中",
    phase_re_verifying: "再次验证中",
    phase_api_waiting: "等待 AI 响应",
    phase_running: "运行中",
    // system message keys
    sys_self_improving: "自我改进中...",
    sys_start_verification: "开始验证",
    sys_verifying_solution: "验证解答",
    sys_verification_failed_correcting: "验证未通过，修正中...",
    sys_solution_good_reverifying: "解答正确，再次验证...",
    sys_verdict_pass: "验证结论: 通过",
    sys_verdict_fail: "验证结论: 未通过",
    sys_correct_solution_found: "正确解答已找到",
    sys_found_correct_in_run: "在第 {run} 轮找到正确解答",
    sys_no_correct_solution: "未找到正确解答",
    sys_error_in_run: "第 {run} 轮出错: {error}",
    sys_run_header: "第 {run} 轮 (共 {total} 轮)",
    sys_iteration_status: "迭代: {iter}, 正确: {corrects}, 错误: {errors}",
  },
  en: {
    app_title: "Mathematical Research Workbench",
    app_subtitle: "Used to assist in solving mathematical problems encountered in research.",
    input_problem: "Input Problem",
    input_placeholder: "Enter the problem here (LaTeX format)...",
    run_btn: "Run",
    stop_btn: "Stop",
    status_idle: "Idle",
    status_stopped: "Stopped",
    status_starting: "Agent starting",
    status_waiting_first: "Agent started, awaiting first response",
    status_no_output: "Agent exited (no output, possibly failed to start)",
    status_done: "Completed",
    status_no_question: "Please enter a problem first",
    status_start_failed: "Failed to start",
    solve_verify_title: "Solve & Verify Dialogue",
    latex_output_title: "Final LaTeX Output (paste into Overleaf to compile a complete PDF)",
    latex_placeholder: "The complete LaTeX document will appear here after solving...",
    copy_latex: "Copy LaTeX",
    copy: "Copy",
    copied: "Copied!",
    settings_title: "Settings",
    tab_prompts: "Prompt Settings",
    tab_api: "Model API Settings",
    prompt_step1_label: "Main Solver Prompt",
    prompt_step1_desc: "Instructs the model to output solutions as LaTeX papers for research-level math, including rigor, honesty, document structure, citation standards and self-check.",
    prompt_self_improve_label: "Self-Improvement Prompt",
    prompt_self_improve_desc: "After the first output, asks the model to review, fix errors, fill proof gaps, and explore deeper solutions.",
    prompt_correction_label: "Correction Prompt",
    prompt_correction_desc: "Uses the verifier's bug report to improve the solution, or provides detailed explanations for disputed findings.",
    prompt_verify_sys_label: "Verification System Prompt",
    prompt_verify_sys_desc: "Guides the verifier as a math expert to strictly verify solutions, distinguishing Critical Errors from Justification Gaps.",
    prompt_verify_reminder_label: "Verification Reminder",
    prompt_verify_reminder_desc: "Reminds the verifier to focus on the Solution section in the LaTeX paper and produce a summary and step-by-step verification log.",
    prompt_check_verify_label: "Verification Re-check Prompt",
    prompt_check_verify_desc: "Has the verifier re-check whether findings are too strict and citations are accurate. Currently disabled in code.",
    badge_disabled: "Disabled",
    save_prompts: "Save Prompts",
    reset_prompts: "Reset to Default",
    save_api: "Save API Settings",
    api_key_keep_hint: "Leave empty to keep the currently saved key unchanged.",
    api_key_saved_hint: "A saved API key is detected. Leave empty to keep it, or check to clear it.",
    clear_api_key: "Clear saved API Key",
    recommend_note: "Recommended: gemini-3-pro-preview or newer models for best results.",
    pipeline_diagram: "Pipeline Architecture",
    model_name_label: "Model Name",
    saved: "Saved",
    save_failed: "Save failed",
    reset_done: "Reset to defaults (unsaved)",
    waiting_ai: "Waiting for AI model response...",
    tokens_unit: "tokens",
    role_solver: "SOLVER",
    role_verifier: "VERIFIER",
    phase_solving: "Solving",
    phase_self_improving: "Self-improving",
    phase_verifying: "Verifying",
    phase_correcting: "Correcting solution",
    phase_re_verifying: "Re-verifying",
    phase_api_waiting: "Awaiting AI response",
    phase_running: "Running",
    sys_self_improving: "Self-improving...",
    sys_start_verification: "Starting verification",
    sys_verifying_solution: "Verifying solution",
    sys_verification_failed_correcting: "Verification failed, correcting...",
    sys_solution_good_reverifying: "Solution correct, re-verifying...",
    sys_verdict_pass: "Verdict: PASS",
    sys_verdict_fail: "Verdict: FAIL",
    sys_correct_solution_found: "Correct solution found",
    sys_found_correct_in_run: "Found correct solution in run {run}",
    sys_no_correct_solution: "No correct solution found",
    sys_error_in_run: "Error in run {run}: {error}",
    sys_run_header: "Run {run} of {total}",
    sys_iteration_status: "Iteration: {iter}, correct: {corrects}, errors: {errors}",
  },
};

const SYSTEM_MSG_KEYS = [
  "self_improving",
  "start_verification",
  "verifying_solution",
  "verification_failed_correcting",
  "solution_good_reverifying",
  "verdict_pass",
  "verdict_fail",
  "correct_solution_found",
  "found_correct_in_run",
  "no_correct_solution",
  "error_in_run",
  "run_header",
  "iteration_status",
];

let currentLang = localStorage.getItem("app_lang") || "zh";

function t(key, params) {
  let text = (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) || key;
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      text = text.replace(new RegExp(`\\{${k}\\}`, "g"), v);
    }
  }
  return text;
}

function applyLanguage() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const val = t(key);
    if (val !== key) el.textContent = val;
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    const val = t(key);
    if (val !== key) el.placeholder = val;
  });
  document.documentElement.lang = currentLang === "zh" ? "zh-CN" : "en";
  document.title = t("app_title");
  refreshApiKeyHint();
}

/* ===== Main app elements ===== */

const runBtn = document.getElementById("runBtn");
const stopBtn = document.getElementById("stopBtn");
const statusEl = document.getElementById("status");
const questionEl = document.getElementById("question");
const chatEl = document.getElementById("chat");
const latexEl = document.getElementById("latex-output");
const copyBtn = document.getElementById("copyBtn");

let runId = "";
let msgCount = 0;
let pollTimer = null;
let startTime = null;
let timerInterval = null;
let currentDetailPhase = "";

/* ===== Status helpers ===== */

function formatElapsed(ms) {
  const totalSec = Math.floor(ms / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function formatTokens(n) {
  const value = Number(n || 0);
  if (value < 1000) return String(Math.floor(value));
  return `${(value / 1000).toFixed(1)}k`;
}

function setStatusAnimated(phaseKey, showDots, showTimer, tokenUsage, showTokens = false) {
  const phaseText = t(phaseKey);
  let html = `<span class="status-phase">${phaseText}${showDots ? "..." : ""}</span>`;
  if (showTimer && startTime) {
    const elapsed = formatElapsed(Date.now() - startTime);
    html += `<span class="status-timer">${elapsed}</span>`;
  }
  const totalTokens = tokenUsage && typeof tokenUsage.total !== "undefined"
    ? Number(tokenUsage.total || 0)
    : null;
  if (showTokens && totalTokens !== null) {
    html += `<span class="status-timer">| ${formatTokens(totalTokens)} ${t("tokens_unit")}</span>`;
  }
  statusEl.innerHTML = html;
  statusEl.classList.toggle("active", showDots);
}

function setStatusText(i18nKey) {
  statusEl.innerHTML = `<span class="status-phase">${t(i18nKey)}</span>`;
  statusEl.classList.remove("active");
}

function startTimer() {
  startTime = Date.now();
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    if (!statusEl.classList.contains("active")) return;
    const timerSpan = statusEl.querySelector(".status-timer");
    if (timerSpan) {
      timerSpan.textContent = formatElapsed(Date.now() - startTime);
    }
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

/* ===== System message rendering ===== */

function renderSystemContent(msg) {
  const key = msg.content;
  const params = msg.params || {};
  const i18nKey = "sys_" + key;
  if (TRANSLATIONS.zh[i18nKey]) {
    return t(i18nKey, params);
  }
  if (params.raw) return params.raw;
  return key;
}

/* ===== Chat bubbles ===== */

function createBubble(msg) {
  const div = document.createElement("div");
  div.className = `bubble ${msg.role}`;

  if (msg.role === "system") {
    div.textContent = renderSystemContent(msg);
  } else {
    const tag = document.createElement("div");
    tag.className = "role-tag";
    tag.textContent = msg.role === "solver" ? t("role_solver") : t("role_verifier");
    div.appendChild(tag);

    if (msg.role === "solver") {
      const cbtn = document.createElement("button");
      cbtn.className = "bubble-copy-btn";
      cbtn.textContent = t("copy");
      cbtn.addEventListener("click", () => {
        navigator.clipboard.writeText(msg.content).then(() => {
          cbtn.textContent = t("copied");
          setTimeout(() => { cbtn.textContent = t("copy"); }, 1500);
        });
      });
      div.appendChild(cbtn);
    }

    const body = document.createElement("div");
    body.textContent = msg.content;
    div.appendChild(body);
  }

  return div;
}

function appendMessages(msgs) {
  const wasAtBottom =
    chatEl.scrollHeight - chatEl.scrollTop - chatEl.clientHeight < 50;

  msgs.forEach((m) => {
    chatEl.appendChild(createBubble(m));
  });

  if (wasAtBottom) {
    chatEl.scrollTop = chatEl.scrollHeight;
  }
}

function removeWaitingBubble() {
  const existing = chatEl.querySelector(".bubble.waiting");
  if (existing) existing.remove();
}

function showWaitingBubble() {
  if (chatEl.querySelector(".bubble.waiting")) return;
  const div = document.createElement("div");
  div.className = "bubble system waiting";
  div.textContent = t("waiting_ai");
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

/* ===== Detail phase → status ===== */

const PHASE_STATUS_MAP = {
  solving: "phase_solving",
  self_improving: "phase_self_improving",
  verifying: "phase_verifying",
  correcting: "phase_correcting",
  re_verifying: "phase_re_verifying",
};

function updateStatusFromPhase(data) {
  if (data.status === "starting") {
    setStatusAnimated("status_starting", true, true, data.token_usage, false);
    return;
  }

  const dp = data.detail_phase || "";
  const phaseKey = PHASE_STATUS_MAP[dp];

  if (phaseKey && data.alive) {
    setStatusAnimated(phaseKey, true, true, data.token_usage, false);
  } else if (data.phase === "api_waiting" && data.alive) {
    setStatusAnimated("phase_api_waiting", true, true, data.token_usage, false);
  } else if (data.alive) {
    setStatusAnimated("phase_solving", true, true, data.token_usage, false);
  }
}

/* ===== Polling ===== */

async function pollLog() {
  if (!runId) return;
  try {
    const res = await fetch(`/log?run_id=${runId}&after=${msgCount}`);
    const data = await res.json();

    if (data.messages && data.messages.length > 0) {
      removeWaitingBubble();
      appendMessages(data.messages);
      msgCount = data.total;
    }

    if (data.phase === "api_waiting" && msgCount === 0 && data.alive) {
      showWaitingBubble();
    }

    updateStatusFromPhase(data);

    if (data.done) {
      removeWaitingBubble();
      stopPolling();
      stopTimer();
      if (!data.alive && msgCount === 0) {
        setStatusText("status_no_output");
      } else {
        setStatusAnimated("status_done", false, true, data.token_usage, true);
      }
      enterIdleState();
      fetchResult();
    }
  } catch (err) {
    console.error("poll error:", err);
  }
}

async function fetchResult() {
  if (!runId) return;
  try {
    const res = await fetch(`/result?run_id=${runId}`);
    const data = await res.json();
    if (data.latex) {
      latexEl.value = data.latex;
      copyBtn.style.display = "inline-block";
    }
  } catch (err) {
    console.error("result error:", err);
  }
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

/* ===== Run button ===== */

function enterRunningState() {
  runBtn.style.display = "none";
  stopBtn.style.display = "inline-block";
}

function enterIdleState() {
  runBtn.style.display = "inline-block";
  runBtn.disabled = false;
  stopBtn.style.display = "none";
}

async function startRun(question) {
  stopPolling();
  stopTimer();
  msgCount = 0;
  currentDetailPhase = "";
  chatEl.innerHTML = "";
  latexEl.value = "";
  copyBtn.style.display = "none";
  enterRunningState();
  setStatusAnimated("status_starting", true, false, { total: 0 }, false);
  startTimer();

  const body = { question };

  try {
    const res = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (data.error) {
      setStatusText("status_start_failed");
      stopTimer();
      enterIdleState();
      return;
    }
    runId = data.run_id;
    setStatusAnimated("status_waiting_first", true, true, { total: 0 }, false);
    pollTimer = setInterval(pollLog, 2000);
  } catch (err) {
    setStatusText("status_start_failed");
    stopTimer();
    enterIdleState();
  }
}

runBtn.addEventListener("click", () => {
  const question = questionEl.value.trim();
  if (!question) {
    setStatusText("status_no_question");
    return;
  }
  startRun(question);
});

stopBtn.addEventListener("click", async () => {
  if (!runId) return;
  stopBtn.disabled = true;
  try {
    const res = await fetch("/stop", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run_id: runId }),
    });
    const data = await res.json();
    if (!data.ok) {
      console.warn("stop response:", data);
    }
  } catch (err) {
    console.error("stop error:", err);
  }
  stopPolling();
  stopTimer();
  removeWaitingBubble();
  setStatusText("status_stopped");
  enterIdleState();
  stopBtn.disabled = false;
});

/* ===== Copy button ===== */

copyBtn.addEventListener("click", () => {
  latexEl.select();
  navigator.clipboard.writeText(latexEl.value).then(
    () => {
      copyBtn.textContent = t("copied");
      setTimeout(() => (copyBtn.textContent = t("copy_latex")), 1500);
    },
    () => {
      document.execCommand("copy");
    }
  );
});

/* ===== Language toggle ===== */

const langBtn = document.getElementById("langBtn");

langBtn.addEventListener("click", () => {
  currentLang = currentLang === "zh" ? "en" : "zh";
  localStorage.setItem("app_lang", currentLang);
  applyLanguage();
});

/* ===== Settings modal ===== */

const settingsBtn = document.getElementById("settingsBtn");
const settingsModal = document.getElementById("settingsModal");
const closeModal = document.getElementById("closeModal");
const tabBtns = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");
const savePromptsBtn = document.getElementById("savePrompts");
const resetPromptsBtn = document.getElementById("resetPrompts");
const promptSaveStatus = document.getElementById("promptSaveStatus");
const saveApiBtn = document.getElementById("saveApi");
const apiSaveStatus = document.getElementById("apiSaveStatus");
const apiKeyHintEl = document.getElementById("apiKeyHint");
const clearApiKeyEl = document.getElementById("clearApiKey");

let defaultPrompts = {};
let hasSavedApiKey = false;

function refreshApiKeyHint() {
  if (!apiKeyHintEl) return;
  apiKeyHintEl.textContent = hasSavedApiKey ? t("api_key_saved_hint") : t("api_key_keep_hint");
}

function openSettings() {
  settingsModal.style.display = "flex";
  loadSettings();
}

function closeSettings() {
  settingsModal.style.display = "none";
}

settingsBtn.addEventListener("click", openSettings);
closeModal.addEventListener("click", closeSettings);

settingsModal.addEventListener("click", (e) => {
  if (e.target === settingsModal) closeSettings();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && settingsModal.style.display === "flex") {
    closeSettings();
  }
});

tabBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabBtns.forEach((b) => b.classList.remove("active"));
    tabContents.forEach((c) => c.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
});

document.querySelectorAll(".accordion-toggle").forEach((toggle) => {
  toggle.addEventListener("click", () => {
    toggle.parentElement.classList.toggle("open");
  });
});

async function loadSettings() {
  try {
    const res = await fetch("/settings");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    defaultPrompts = { ...(data.default_prompts || data.prompts || {}) };

    document.querySelectorAll(".prompt-editor").forEach((el) => {
      const key = el.dataset.prompt;
      if (data.prompts && data.prompts[key] != null) {
        el.value = data.prompts[key];
      }
    });

    const api = data.api || {};
    document.getElementById("apiBaseUrl").value = api.base_url || "";
    document.getElementById("apiModelName").value = api.model_name || "";
    document.getElementById("apiTemperature").value =
      api.temperature != null ? api.temperature : "";
    document.getElementById("apiMaxTokens").value =
      api.max_tokens != null ? api.max_tokens : "";
    hasSavedApiKey = Boolean(data.has_api_key);
    clearApiKeyEl.checked = false;
    refreshApiKeyHint();
  } catch (err) {
    console.error("load settings error:", err);
  }
}

function flashStatus(el, i18nKey) {
  el.textContent = t(i18nKey);
  setTimeout(() => {
    el.textContent = "";
  }, 2500);
}

savePromptsBtn.addEventListener("click", async () => {
  const prompts = {};
  document.querySelectorAll(".prompt-editor").forEach((el) => {
    prompts[el.dataset.prompt] = el.value;
  });

  try {
    const res = await fetch("/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompts }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || data.ok === false) {
      throw new Error(data.error || `HTTP ${res.status}`);
    }
    flashStatus(promptSaveStatus, "saved");
  } catch (err) {
    console.error("save prompts error:", err);
    flashStatus(promptSaveStatus, "save_failed");
  }
});

resetPromptsBtn.addEventListener("click", () => {
  document.querySelectorAll(".prompt-editor").forEach((el) => {
    const key = el.dataset.prompt;
    if (defaultPrompts[key] != null) {
      el.value = defaultPrompts[key];
    }
  });
  flashStatus(promptSaveStatus, "reset_done");
});

saveApiBtn.addEventListener("click", async () => {
  const rawTemp = document.getElementById("apiTemperature").value.trim();
  const rawMaxTokens = document.getElementById("apiMaxTokens").value.trim();
  const parsedTemp = rawTemp === "" ? 0.1 : Number(rawTemp);
  const parsedMaxTokens = rawMaxTokens === "" ? 24576 : Number.parseInt(rawMaxTokens, 10);

  const api = {
    base_url: document.getElementById("apiBaseUrl").value.trim(),
    model_name: document.getElementById("apiModelName").value.trim(),
    temperature: Number.isFinite(parsedTemp) ? parsedTemp : 0.1,
    max_tokens: Number.isFinite(parsedMaxTokens) ? parsedMaxTokens : 24576,
  };

  const keyVal = document.getElementById("apiKey").value.trim();
  if (clearApiKeyEl.checked) {
    api.api_key_mode = "clear";
  } else if (keyVal) {
    api.api_key_mode = "set";
    api.api_key = keyVal;
  } else {
    api.api_key_mode = "keep";
  }

  try {
    const res = await fetch("/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || data.ok === false) {
      throw new Error(data.error || `HTTP ${res.status}`);
    }
    hasSavedApiKey = Boolean(data.has_api_key);
    clearApiKeyEl.checked = false;
    document.getElementById("apiKey").value = "";
    refreshApiKeyHint();
    flashStatus(apiSaveStatus, "saved");
  } catch (err) {
    console.error("save api settings error:", err);
    flashStatus(apiSaveStatus, "save_failed");
  }
});

/* ===== Init ===== */

applyLanguage();
