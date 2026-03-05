# UI 服务说明

`ui_server` 提供本地 Web 交互层，用于驱动 `code/agent.py` 并实时展示结果。

## 启动

在 `IMO25/` 目录执行：

```bash
python ui_server/server.py
```

浏览器访问：

- `http://127.0.0.1:8000`

## 后端接口

- `POST /run`：启动一次新任务
- `POST /stop`：中断任务
- `GET /log`：轮询增量消息（solver/verifier/system）和阶段状态
- `GET /result`：提取最终 LaTeX
- `GET /settings`：读取当前配置（不回传明文 API Key）
- `POST /settings`：保存 API 与提示词配置

## 运行产物

每次运行会在 `ui_server/runs/<run_id>/` 下生成：

- `problem.txt`
- `agent.log`
- `memory.json`
- `meta.json`
- `config.json`
- `stderr.log`

## 配置文件

- 本地持久配置：`ui_server/settings.json`（已被 `.gitignore` 忽略）
- 示例模板：`ui_server/settings.example.json`

建议使用 UI 填写 API Key，避免把密钥写进代码或提交到版本库。
