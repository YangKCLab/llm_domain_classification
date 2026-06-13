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
        token_count = {
            "input": usage["prompt_tokens"],
            "output": usage["completion_tokens"],
            "reasoning_tokens": usage["completion_tokens_details"]["reasoning_tokens"],
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
