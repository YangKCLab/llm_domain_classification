import os
from dotenv import load_dotenv

from openai import OpenAI
from anthropic import Anthropic
from together import Together
from google import genai
from google.genai import types

from llmdomainrating.prompts import (
    SYS_BASE,
    USER_INSTRUCTION,
    USER_FORMAT,
    DOMAIN_RATING_JSON_SCHEMA,
    DomainRating,
)


class BaseClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self._create_api_client()

    def _create_api_client(self):
        raise NotImplementedError("Subclasses must implement this method")

    def query_model(self, domain: str, model: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")


class OpenAIClient(BaseClient):
    def __init__(self, api_key: str = None):
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
        super().__init__(api_key)

    def _create_api_client(self):
        self.client = OpenAI(api_key=self.api_key)

    def query_model(self, domain: str, model: str) -> str:
        if model.startswith("o") or model.startswith("gpt-5"):
            resp = self.response_api_reasoning(domain, model)
        else:
            resp = self.response_api(domain, model)
        return resp

    def response_api(self, domain: str, model: str) -> str:
        try:
            resp = self.client.responses.parse(
                model=model,
                instructions=SYS_BASE,
                input=USER_INSTRUCTION.format(domain=domain),
                temperature=0,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "domain_rating",
                        "strict": True,
                        "schema": DOMAIN_RATING_JSON_SCHEMA,
                    }
                },
            )
            return resp.model_dump_json()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def response_api_reasoning(self, domain: str, model: str) -> str:
        try:
            resp = self.client.responses.parse(
                model=model,
                instructions=SYS_BASE,
                input=USER_INSTRUCTION.format(domain=domain),
                reasoning={
                    "effort": "medium",
                    "summary": "auto",
                },
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "domain_rating",
                        "strict": True,
                        "schema": DOMAIN_RATING_JSON_SCHEMA,
                    }
                },
            )
            return resp.model_dump_json()
        except Exception as e:
            print(f"Error: {e}")
            return None


class AnthropicClient(BaseClient):
    def __init__(self, api_key: str = None):
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("ANTHROPIC_API_KEY")
        super().__init__(api_key)

    def _create_api_client(self):
        self.client = Anthropic(api_key=self.api_key)

    def query_model(self, domain: str, model: str) -> str:
        try:
            resp = self.client.messages.create(
                model=model,
                system=SYS_BASE,
                messages=[
                    {
                        "role": "user",
                        "content": f"{USER_INSTRUCTION.format(domain=domain)}\n{USER_FORMAT}",
                    }
                ],
                max_tokens=8192,
                temperature=0,
            )
            return resp.to_json()
        except Exception as e:
            print(f"Error: {e}")
            return None


class XAIAPIClient(BaseClient):
    def __init__(self, api_key: str = None):
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("XAI_API_KEY")
        super().__init__(api_key)

    def _create_api_client(self):
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.x.ai/v1")

    def query_model(self, domain: str, model: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYS_BASE},
                    {"role": "user", "content": USER_INSTRUCTION.format(domain=domain)},
                ],
                temperature=0,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "domain_rating",
                        "strict": True,
                        "schema": DOMAIN_RATING_JSON_SCHEMA,
                    },
                },
            )
            return resp.model_dump_json()
        except Exception as e:
            print(f"Error: {e}")
            return None


class TogetherClient(BaseClient):
    def __init__(self, api_key: str = None):
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("TOGETHER_API_KEY")
        super().__init__(api_key)

    def _create_api_client(self):
        self.client = Together(api_key=self.api_key)

    def query_model(self, domain: str, model: str) -> str:
        reasoning_models = set(
            [
                "deepseek-ai/DeepSeek-R1",
                "deepseek-ai/DeepSeek-V4-Pro",
                "deepseek-ai/DeepSeek-V4-Flash",
                "openai/gpt-oss-20b",
                "openai/gpt-oss-120b",
                "moonshotai/Kimi-K2.6",
                "MiniMaxAI/MiniMax-M2.7",
                "MiniMaxAI/MiniMax-M3",
                "zai-org/GLM-5.1",
            ]
        )
        if model in reasoning_models:
            resp = self.query_reasoning_model(domain, model)
        else:
            resp = self.query_normal_model(domain, model)
        return resp

    def query_normal_model(self, domain: str, model: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYS_BASE},
                    {"role": "user", "content": USER_INSTRUCTION.format(domain=domain)},
                ],
                temperature=0,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "domain_rating",
                        "strict": True,
                        "schema": DOMAIN_RATING_JSON_SCHEMA,
                    },
                },
            )
            return resp.model_dump_json()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def query_reasoning_model(self, domain: str, model: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYS_BASE},
                    {
                        "role": "user",
                        "content": f"{USER_INSTRUCTION.format(domain=domain)}\n{USER_FORMAT}",
                    },
                ],
                temperature=0,
            )
            return resp.model_dump_json()
        except Exception as e:
            print(f"Error: {e}")
            return None


class GoogleClient(BaseClient):
    def __init__(self, api_key: str = None):
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
        super().__init__(api_key)

    def _create_api_client(self):
        self.client = genai.Client(api_key=self.api_key)

    def query_model(self, domain: str, model: str) -> str:
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            text=USER_INSTRUCTION.format(domain=domain)
                        ),
                    ],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=DomainRating,
                system_instruction=[
                    types.Part.from_text(text=SYS_BASE),
                ],
            )
            resp = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )
            return resp.model_dump_json()
        except Exception as e:
            print(f"Error: {e}")
            return None


def create_api_client(provider: str, api_key: str = None):
    provider_mapping = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "xai": XAIAPIClient,
        "together": TogetherClient,
        "google": GoogleClient,
    }
    if provider not in provider_mapping:
        raise ValueError(
            f"Unknown provider: {provider}, must be one of {provider_mapping.keys()}"
        )
    return provider_mapping[provider](api_key)
