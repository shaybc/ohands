# OHANDS

Standalone OpenHands Software Agent SDK task runner. It uses embedded LiteLLM to
connect to a separately running AIGW through OpenAI-compatible Chat Completions.
The OpenHands SDK source repository is not required on this machine.

## Run

1. Install Python 3.12+ and activate your intended Python environment.
2. Configure pip to use your internal Artifactory PyPI repository.
3. Copy `.env.example` to `.env` (a placeholder `.env` is supplied locally).
4. Set `LLM_BASE_URL`, `LLM_MODEL`, the target `AIGW_WORKSPACE`, and the multiline
   `OHANDS_PROMPT`. The inbound API key is a placeholder, not an enterprise secret.
5. Start AIGW separately with its `run-aigw.cmd`.
6. Run `run-ohands.cmd` here. It installs `requirements.txt`, then runs `ohands.py`.
   Use `python ohands.py` to skip installation when packages are already installed.

The supplied prompt requests review only. Set your implementation request in
`OHANDS_PROMPT` to have the SDK edit files and run commands. Each launch creates a
single task conversation. Terminal, file editor, and task tracker tools are
registered. They run with the Python process's permissions; the workspace is not
a filesystem sandbox. Windows uses the SDK's PowerShell backend. Install the
target project's own build/test tools separately.

## Configuration

The runner loads `.env` beside `ohands.py`; process variables override that file.
`AIGW_CONFIG` can select a different env file. Existing setting names are retained
for compatibility: `AIGW_WORKSPACE`, `AIGW_MAX_ITERATIONS` (100 by default), and
`AIGW_WHEELHOUSE` for optional offline package installation. No wheel folder is
needed when the packages are available through the configured Artifactory index.
The launcher uses the active `python` interpreter; it does not create a virtual
environment. Keep gateway connector credentials in AIGW's separate configuration.

`LLM_MODEL` must use `openai/<enterprise-model-id>` and `LLM_BASE_URL` must include
`/v1`. `LLM_TIMEOUT` defaults to 300 seconds and `LLM_MAX_OUTPUT_TOKENS` to 8192.
For a container or remote gateway, set an address reachable from the runner.

Before importing the SDK, the runner sets `LITELLM_LOCAL_MODEL_COST_MAP=true`,
`LITELLM_OFFLINE_MODE=true`, and `HF_HUB_OFFLINE=1`. Any needed tokenizer data must
already be cached. The LLM still connects to the configured AIGW endpoint.
Dependencies pin `agent-client-protocol==0.10.1` and `litellm==1.110.3` alongside
OpenHands SDK/tools 1.44.1. Package resolution on your Artifactory and an actual
enterprise model run remain environment-specific checks.

## Tests

```cmd
python -m unittest discover -s tests -p "test_*.py"
```

Tests use the real dotenv loader for configuration checks and mocked SDK calls;
they do not install dependencies or send prompts to a model.
