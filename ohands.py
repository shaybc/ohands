"""Run an editable coding task through OpenHands, LiteLLM, and a running AIGW."""
import os
from pathlib import Path

# Set OHANDS_PROMPT in .env and edit WORKSPACE, then run: python ohands.py
WORKSPACE = Path(__file__).resolve().parent


def main() -> None:
    """Load local settings and execute OHANDS_PROMPT with OpenHands' coding tools."""
    from dotenv import load_dotenv

    project_directory = Path(__file__).resolve().parent
    config_path = Path(os.environ.get("AIGW_CONFIG", project_directory / ".env"))
    load_dotenv(config_path)

    # Must be set before importing OpenHands, which imports LiteLLM. to set litellm to work in offline mode
    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "true"
    os.environ["LITELLM_OFFLINE_MODE"] = "true"
    os.environ["HF_HUB_OFFLINE"] = "1"

    workspace = Path(os.environ.get("AIGW_WORKSPACE", str(WORKSPACE))).expanduser().resolve()
    if not workspace.is_dir():
        raise ValueError(f"Workspace is not a directory: {workspace}")
    prompt = os.environ.get("OHANDS_PROMPT", "").strip()
    if not prompt:
        raise ValueError("Set OHANDS_PROMPT in the .env file or process environment.")

    from openhands.sdk import LLM, Agent, Conversation, Tool
    from openhands.tools.file_editor import FileEditorTool
    from openhands.tools.task_tracker import TaskTrackerTool
    from openhands.tools.terminal import TerminalTool

    host = os.environ.get("HOST", "127.0.0.1")
    if host in ("0.0.0.0", "::"):
        host = "127.0.0.1"
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    default_url = f"http://{host}:{os.environ.get('PORT', '7331')}/v1"
    model = os.environ.get("GEMINI_CONNECTOR_MODEL", "gemini-2.5-pro")
    llm = LLM(
        model=os.environ.get("LLM_MODEL", f"openai/{model}"),
        base_url=os.environ.get("LLM_BASE_URL", default_url),
        api_key=os.environ.get("LLM_API_KEY", "dummy"),
        api_mode="chat",
        native_tool_calling=True,
        stream=False,
        timeout=int(os.environ.get("LLM_TIMEOUT", "300")),
        max_output_tokens=int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "8192")),
        caching_prompt=False,
        disable_vision=True,
    )
    agent = Agent(llm=llm, tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ])
    conversation = Conversation(
        agent=agent,
        workspace=str(workspace),
        max_iteration_per_run=int(os.environ.get("AIGW_MAX_ITERATIONS", "100")),
    )
    try:
        conversation.send_message(prompt)
        conversation.run()
    finally:
        conversation.close()


if __name__ == "__main__":
    main()
