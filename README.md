# IMO25 数学求解与验证系统

一个本地可运行的数学问题求解系统：使用单 Agent 流程完成「求解 -> 验证 -> 自我修正」，并通过 Web 界面实时查看求解器/验证器对话及最终 LaTeX 输出。

## 主要能力

- 支持自定义 LLM API：`Base URL`、`Model`、`API Key`、`temperature`、`max_tokens`
- 支持自定义系统提示词（默认自动回填为当前内置提示词，不需要从零编写）
- 前端展示完整流程状态、求解与验证对话、最终 LaTeX 文档
- 支持中断当前运行

## 目录结构

- `code/agent.py`：核心求解与验证流程
- `ui_server/server.py`：Flask 后端（运行任务、日志解析、结果提取、设置读写）
- `ui_server/static/`：前端页面（`index.html` / `app.js` / `styles.css`）
- `ui_server/runs/`：每次运行产物（日志、内存、配置、元数据）
- `ui_server/settings.example.json`：配置示例模板（不含密钥）
- `requirements.txt`：Python 依赖

## 快速开始

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 启动 Web 服务

在 `IMO25/` 目录执行：

```bash
python ui_server/server.py
```

浏览器访问：

- `http://127.0.0.1:8000`

### 3) 配置你自己的 LLM API

打开页面右上角设置，进入「模型 API 设置」：

- Base URL（例如 OpenAI-compatible 网关）
- Model Name
- API Key
- temperature
- max_tokens

说明：

- API Key 输入框留空：保持当前已保存密钥不变
- 勾选“清空已保存 API Key”：删除已保存密钥

### 4) 配置提示词

进入「提示词设置」：

- 每个提示词都有默认值和简要说明
- 可在默认基础上微调后保存
- 点击“恢复默认”可回到 `agent.py` 内置默认提示词

## CLI 运行（可选）

可直接运行 `code/agent.py`：

```bash
python code/agent.py "<problem_file>" --log "<log_file>" --memory "<memory_file>" --config "<config_json>"
```

常用参数：

- `--log`：日志文件路径
- `--memory`：记忆文件路径
- `--config`：覆盖默认 API/提示词配置
- `--max_runs`：总运行轮次

## 安全与版本控制建议

- 不要提交真实 API Key
- 不要提交运行产物（`ui_server/runs/`）
- 本项目 `.gitignore` 已默认忽略常见敏感文件与运行目录

## 常见问题

- 运行中长时间无输出：通常是模型响应耗时，可查看状态文本和 `ui_server/runs/<run_id>/agent.log`
- 最终区为空：检查日志中是否有完整 LaTeX 文档；失败场景会尽量回退到最后一轮求解器输出
- token 显示为 0：通常是网关响应未返回 `usage` 或返回结构不一致