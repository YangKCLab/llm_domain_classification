import json

model_prices = {
    "OpenAI": {
        "gpt-4.1-nano-2025-04-14": {"input": 0.1, "output": 0.4, "cached_input": 0.025},
        "gpt-4.1-mini-2025-04-14": {"input": 0.4, "output": 1.6, "cached_input": 0.10},
        "gpt-4.1-2025-04-14": {"input": 2, "output": 8, "cached_input": 0.5},
        "o1-2024-12-17": {"input": 15, "output": 60, "cached_input": 7.5},
        "o3-2025-04-16": {"input": 10, "output": 40, "cached_input": 2.5},
        "o3-mini-2025-01-31": {"input": 1.1, "output": 4.4, "cached_input": 0.55},
        "o4-mini-2025-04-16": {"input": 1.1, "output": 4.4, "cached_input": 0.275},
        "gpt-5-nano-2025-08-07": {"input": 0.05, "output": 0.4, "cached_input": 0.005},
        "gpt-5-mini-2025-08-07": {"input": 0.25, "output": 2, "cached_input": 0.025},
        "gpt-5-2025-08-07": {"input": 1.25, "output": 10, "cached_input": 0.125},
        "gpt-5.1-2025-11-13": {"input": 1.25, "output": 10, "cached_input": 0.125},
        "gpt-5.2-2025-12-11": {"input": 1.75, "output": 14, "cached_input": 0.175},
        "gpt-5.4-nano-2026-03-17": {"input": 0.2, "output": 1.25, "cached_input": 0.02},
        "gpt-5.4-mini-2026-03-17": {
            "input": 0.75,
            "output": 4.5,
            "cached_input": 0.075,
        },
        "gpt-5.4-2026-03-05": {"input": 2.5, "output": 15, "cached_input": 0.25},
        "gpt-5.5-2026-04-23": {"input": 5, "output": 30, "cached_input": 0.5},
    },
    "Anthropic": {
        "claude-3-5-haiku-20241022": {
            "input": 0.8,
            "output": 4,
            "cache_write": 0.1,
            "cache_read": 0.08,
        },
        "claude-3-5-sonnet-20241022": {
            "input": 3,
            "output": 15,
            "cache_write": 3.75,
            "cache_read": 0.3,
        },
        "claude-3-7-sonnet-20250219": {
            "input": 3,
            "output": 15,
            "cache_write": 3.75,
            "cache_read": 0.3,
        },
        "claude-haiku-4-5-20251001": {
            "input": 1,
            "output": 4,
            "cache_write": 1,
            "cache_read": 0.08,
        },
        "claude-sonnet-4-5-20250929": {
            "input": 3,
            "output": 15,
            "cache_write": 3.75,
            "cache_read": 0.3,
        },
        "claude-opus-4-5-20251101": {
            "input": 5,
            "output": 25,
            "cache_write": 6.25,
            "cache_read": 0.5,
        },
    },
    "XAI": {
        "grok-3-beta": {
            "input": 3,
            "output": 15,
        },
        "grok-3-mini-beta": {
            "input": 0.3,
            "output": 0.5,
            "reasoning_tokens": 0.5,
        },
        "grok-4.3": {
            "input": 1.25,
            "output": 2.5,
        },
        "grok-4.20-0309-reasoning": {
            "input": 1.25,
            "output": 2.5,
        },
        "grok-4.20-0309-non-reasoning": {
            "input": 1.25,
            "output": 2.5,
        },
    },
    "Together": {
        "Llama-3.3-70B-Instruct-Turbo": {
            "input": 0.88,
            "output": 0.88,
        },
        "Llama-4-Scout-17B-16E-Instruct": {
            "input": 0.18,
            "output": 0.59,
        },
        "Llama-4-Maverick-17B-128E-Instruct-FP8": {
            "input": 0.27,
            "output": 0.85,
        },
        "DeepSeek-V3": {
            "input": 1.25,
            "output": 1.25,
        },
        "DeepSeek-R1": {
            "input": 3,
            "output": 7,
        },
        # Keys are the short model name (no org prefix) to match the name passed
        # to parse_together.py / TogetherCostCalculator; the org-prefixed full IDs
        # are used on the query side (commands.sh + api.py reasoning_models set).
        "DeepSeek-V4-Pro": {
            "input": 2.10,
            "output": 4.40,
        },
        # DeepSeek-V4-Flash is not on Together's published serverless pricing as
        # of 2026-06; values below are a best estimate from third-party listings
        # and must be verified (model may not be serverless-available on Together).
        "DeepSeek-V4-Flash": {
            "input": 0.14,
            "output": 0.28,
        },
        "gpt-oss-20b": {
            "input": 0.05,
            "output": 0.20,
        },
        "gpt-oss-120b": {
            "input": 0.15,
            "output": 0.60,
        },
        "Kimi-K2.6": {
            "input": 1.20,
            "output": 4.50,
        },
        "MiniMax-M2.7": {
            "input": 0.30,
            "output": 1.20,
        },
        "MiniMax-M3": {
            "input": 0.30,
            "output": 1.20,
        },
        "GLM-5.1": {
            "input": 1.40,
            "output": 4.40,
        },
    },
    "Google": {
        "gemini-2.0-flash": {
            "input": 0.1,
            "output": 0.4,
        },
        "gemini-2.0-flash-lite": {
            "input": 0.075,
            "output": 0.3,
        },
    },
}


class CostCalculatorBase:
    def __init__(self, model_name: str, provider: str):
        if model_name not in model_prices[provider]:
            raise ValueError(f"Model {model_name} not found in {provider} model prices")
        model_unit_prices = model_prices[provider][model_name]
        self.model_unit_prices = model_unit_prices

    def calculate_cost(self, response: str) -> dict:
        price_unit = 1_000_000
        resp_obj = self._parse_response(response)
        token_count = self._extract_token_count(resp_obj)
        cost = 0
        for item, num in token_count.items():
            cost += self.model_unit_prices.get(item, 0) * num / price_unit
        return {"cost": cost, "token_count": token_count}

    def _parse_response(self, response) -> dict:
        if isinstance(response, str):
            if response.endswith(".json"):
                with open(response, "r") as f:
                    resp = json.load(f)
            else:
                resp = json.loads(response)
        elif isinstance(response, dict):
            resp = response
        else:
            raise ValueError("Invalid response type")
        return resp

    def _extract_token_count(self, resp_obj: dict) -> dict:
        raise NotImplementedError("Subclasses must implement this method")


class OpenAICostCalculator(CostCalculatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name, "OpenAI")

    def _extract_token_count(self, resp_obj: dict) -> dict:
        usage = resp_obj["usage"]
        token_count = {
            "input": usage["input_tokens"],
            "cached_input": usage["input_tokens_details"]["cached_tokens"],
            "output": usage["output_tokens"],
            "reasoning_tokens": usage["output_tokens_details"]["reasoning_tokens"],
        }
        return token_count


class AnthropicCostCalculator(CostCalculatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name, "Anthropic")

    def _extract_token_count(self, resp_obj: dict) -> dict:
        usage = resp_obj["usage"]
        token_count = {
            "input": usage["input_tokens"],
            "output": usage["output_tokens"],
            "cache_write": usage["cache_creation_input_tokens"],
            "cache_read": usage["cache_read_input_tokens"],
        }
        return token_count


class XAICostCalculator(CostCalculatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name, "XAI")

    def _extract_token_count(self, resp_obj: dict) -> dict:
        usage = resp_obj["usage"]
        # Non-reasoning Grok models may omit completion_tokens_details or
        # reasoning_tokens, so default to 0 rather than KeyError-ing.
        completion_details = usage.get("completion_tokens_details") or {}
        token_count = {
            "input": usage["prompt_tokens"],
            "output": usage["completion_tokens"],
            "reasoning_tokens": completion_details.get("reasoning_tokens", 0),
        }
        return token_count


class TogetherCostCalculator(CostCalculatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name, "Together")

    def _extract_token_count(self, resp_obj: dict) -> dict:
        usage = resp_obj["usage"]
        token_count = {
            "input": usage["prompt_tokens"],
            "output": usage["completion_tokens"],
            # "cached_tokens": usage["cached_tokens"], # not always available
        }
        return token_count


class GoogleCostCalculator(CostCalculatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name, "Google")

    def _extract_token_count(self, resp_obj: dict) -> dict:
        usage = resp_obj["usage_metadata"]
        token_count = {
            "input": usage["prompt_token_count"],
            "output": usage["candidates_token_count"],
        }
        return token_count
