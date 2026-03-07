# 数学研究助手

[中文](./README.md) | [English](./README.en.md)

> “在几何学里，没有专为国王铺设的大道”
>
> — 欧几里得，回答托勒密国王时所言

这是一个面向数学爱好者与数学研究者的 AI Agent 系统，用于辅助求解学习或研究中遇到的数学问题。系统采用轻量化「求解 -> 验证 -> 自我修正」流程，并提供简洁易用的 Web UI。

## 项目概述

适用范围：
本项目可以帮助你检索相关文献、提供数学问题的理解路径，并辅助数学学习与研究；但它无法替代扎实的数学思考、推导训练与对数学本身的审美体验。

通过调用 Gemini 3 Pro 或其他推理能力相近的模型 API，可以实现：

1. 为数学教材中的练习题（如 GTM 系列）提供详细证明思路，并在必要时附上参考文献。
2. 为工程场景中的数学问题提供参考解答与参考文献。
3. 为真实研究过程中的数学问题提供参考思路（待进一步验证）。
4. 提供自动化求解流程，仅需输入感兴趣的问题描述。
5. 求解完成后输出完整的 LaTeX 代码，可直接粘贴到 Overleaf 等 LaTeX 编译器生成 PDF，便于阅读与写作。

- arXiv: [Can a Lightweight Automated AI Pipeline Solve Research-Level Mathematical Problems?](https://arxiv.org/abs/2602.13695v1)


项目主要包含以下模块：

- `code/agent.py`：核心 Agent 流程（求解、验证、自我修正）。
- `ui_server/server.py`：Flask 后端（任务运行、日志解析、结果提取、设置持久化）。
- `ui_server/static/`：前端界面文件（`index.html`、`app.js`、`styles.css`）。
- `ui_server/settings.example.json`：不含敏感信息的配置模板。
- `ui_server/runs/`：每次运行的产物目录。
- `requirements.txt`：Python 依赖。


## 效果展示

### 网页界面示例

![Mathematical Research Assistant Web UI](./ui-snap.png)

### LaTeX 编译结果示例（1+1）

- PDF 示例：[`latex-demo.pdf`](./latex-demo.pdf)

## 环境要求

1. 已安装 **Python 3.9+**
2. 可用的 **LLM API**（`base_url`、`model_name`、`api_key`）
3. 安装依赖

```bash
pip install -r requirements.txt
```

## 安装与启动

1. 克隆仓库

```bash
git clone https://github.com/ml1301215/research-math-assistant.git
cd research-math-assistant
```

2. 启动 Web 服务

```bash
python ui_server/server.py
```

3. 浏览器打开

- `http://127.0.0.1:8000`

4. 在设置页配置 API

- Base URL
- Model Name
- API Key
- temperature
- max_tokens

## 使用方法

### Web UI（推荐）

1. 输入数学问题（建议提供完整的问题描述）。
2. 点击 `Run`。
3. 实时查看求解器/验证器对话。
4. 完成后复制最终 LaTeX 输出。

### 命令行 (`code/agent.py`)

```bash
python code/agent.py "<problem_file>" --log "<log_file>" --memory "<memory_file>" --config "<config_json>"
```

**参数：**

- `--log LOG_FILE`：日志输出路径
- `--memory MEMORY_FILE`：记忆文件路径
- `--config CONFIG_JSON`：覆盖 API/提示词配置
- `--max_runs N`：最大迭代轮次

## 输出与日志

- 运行产物写入 `ui_server/runs/<run_id>/`
- UI 展示结构化对话（不直接展示原始提示词）
- 最终 LaTeX 可在 UI 和 `/result` 获取

## 常见问题

1. **API Key 保存失败**：检查 `/settings` 返回内容与文件写权限。
2. **模型无响应**：复查 Base URL、Model Name、API Key。
3. **运行耗时较长**：难题和大模型通常耗时更久。
4. **最终 LaTeX 为空**：检查对应运行目录下 `agent.log` 与 `stderr.log`。


## 引用

如果你在研究中使用本项目，请引用：

```bibtex
@article{meng2026lightweight,
  title={Can a Lightweight Automated AI Pipeline Solve Research-Level Mathematical Problems?},
  author={Meng, Lve and Zhao, Weilong and Zhang, Yanzhi and Guan, Haoxiang and He, Jiyan},
  journal={arXiv preprint arXiv:2602.13695},
  year={2026}
}
```

## 致谢与相关工作

- 衷心感谢 `2025 Lin Yang, Yichen Huang` 的工作，他们提出并实践了高效的 Agent 求解-验证迭代范式，为本项目的流程设计与工程实现提供了重要参考。
- 参考仓库：[`lyang36/IMO25`](https://github.com/lyang36/IMO25)

## 许可证


```text
MIT License

Copyright (c) 2026 Lve Meng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
