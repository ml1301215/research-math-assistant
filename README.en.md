# Mathematical Research Assistant

[中文](./README.md) | [English](./README.en.md)

> "In mathematics you don't understand things. You just get used to them."
>
> — John von Neumann.

An AI agent system built for math enthusiasts and researchers to solve research-stage mathematical problems, using a lightweight pipeline: solve -> verify -> self-correct.

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

## Overview

This project mainly includes:

- `code/agent.py`: Core Agent pipeline (solving, verification, self-correction).
- `ui_server/server.py`: Flask backend (task execution, log parsing, result extraction, settings persistence).
- `ui_server/static/`: Frontend files (`index.html`, `app.js`, `styles.css`).
- `ui_server/settings.example.json`: Configuration template without sensitive info.
- `ui_server/runs/`: Per-run output directory.
- `requirements.txt`: Python dependencies.

Validated with Gemini 3 Pro integration, the system can solve mathematical problems that appear in real research workflows.
- arXiv: [Can a Lightweight Automated AI Pipeline Solve Research-Level Mathematical Problems?](https://arxiv.org/abs/2602.13695v1)

## Showcase

### Web UI Example

![Mathematical Research Assistant Web UI](./ui-snap.png)

### LaTeX Compilation Result Example (1+1)

- PDF demo: [`latex-demo.pdf`](./latex-demo.pdf)

## Prerequisites

1. **Python 3.9+** installed
2. A usable **LLM API** (`base_url`, `model_name`, `api_key`)
3. Install dependencies

```bash
pip install -r requirements.txt
```

## Setup

1. Clone repository

```bash
git clone https://github.com/ml1301215/research-math-assistant.git
cd research-math-assistant
```

2. Start web service

```bash
python ui_server/server.py
```

3. Open in browser

- `http://127.0.0.1:8000`

4. Configure API in Settings

- Base URL
- Model Name
- API Key
- temperature
- max_tokens

## Usage

### Web UI (recommended)

1. Input a math problem (LaTeX recommended).
2. Click `Run`.
3. Watch real-time solver/verifier dialogue.
4. Copy final LaTeX output after completion.

### CLI (`code/agent.py`)

```bash
python code/agent.py "<problem_file>" --log "<log_file>" --memory "<memory_file>" --config "<config_json>"
```

**Options:**

- `--log LOG_FILE`: log output path
- `--memory MEMORY_FILE`: memory file path
- `--config CONFIG_JSON`: override API/prompt settings
- `--max_runs N`: maximum run iterations

## Output and Logging

- Runtime artifacts are written to `ui_server/runs/<run_id>/`
- UI shows structured dialogue (instead of raw prompt dumps)
- Final LaTeX is available in UI and `/result`

## Troubleshooting

1. **API key save failed**: check `/settings` response and file write permission.
2. **No model response**: verify base URL, model name, and API key.
3. **Long runtime**: hard problems and larger models naturally take longer.
4. **Empty final LaTeX**: inspect `agent.log` and `stderr.log` in the run directory.

## Citation

If you use this project in your research, please cite:

```bibtex
@article{meng2026lightweight,
  title={Can a Lightweight Automated AI Pipeline Solve Research-Level Mathematical Problems?},
  author={Meng, Lve and Zhao, Weilong and Zhang, Yanzhi and Guan, Haoxiang and He, Jiyan},
  journal={arXiv preprint arXiv:2602.13695},
  year={2026}
}
```

## Acknowledgement and Related Work

- We sincerely thank the work of `2025 Lin Yang, Yichen Huang`. They proposed and demonstrated an efficient Agent-based solve-verify iteration paradigm, which provided key references for the workflow and engineering implementation of this project.
- Reference repository: [`lyang36/IMO25`](https://github.com/lyang36/IMO25)

## License

MIT License - Copyright (c) 2026 Lve Meng
