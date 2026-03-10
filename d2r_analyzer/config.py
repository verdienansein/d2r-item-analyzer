from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    openai_api_key: str
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    capture_hotkey: str = "<ctrl>+a"
    evaluation_mode: str = "manual"
    manual_evaluation_rules_file: str = "d2r_analyzer/tests/config_rules/test_rules.json"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = AppConfig()
