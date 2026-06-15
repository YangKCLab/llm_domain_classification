# Claude 3.5 Haiku
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv anthropic claude-3-5-haiku-20241022 ../../../data/intermediate/raw_responses/anthropic/claude-3-5-haiku-20241022

uv run parse_anthropic.py anthropic claude-3-5-haiku-20241022 ../../../data/intermediate/raw_responses/anthropic/claude-3-5-haiku-20241022 ../../../data/intermediate/parsed_responses/anthropic/claude-3-5-haiku-20241022.parquet

# Claude 3.5 Sonnet
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv anthropic claude-3-5-sonnet-20241022 ../../../data/intermediate/raw_responses/anthropic/claude-3-5-sonnet-20241022

uv run parse_anthropic.py anthropic claude-3-5-sonnet-20241022 ../../../data/intermediate/raw_responses/anthropic/claude-3-5-sonnet-20241022 ../../../data/intermediate/parsed_responses/anthropic/claude-3-5-sonnet-20241022.parquet

# Claude 3.7 Sonnet
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv anthropic claude-3-7-sonnet-20250219 ../../../data/intermediate/raw_responses/anthropic/claude-3-7-sonnet-20250219

uv run parse_anthropic.py anthropic claude-3-7-sonnet-20250219 ../../../data/intermediate/raw_responses/anthropic/claude-3-7-sonnet-20250219 ../../../data/intermediate/parsed_responses/anthropic/claude-3-7-sonnet-20250219.parquet

# Claude Haiku 4.5
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv anthropic claude-haiku-4-5-20251001 ../../../data/intermediate/raw_responses/anthropic/claude-haiku-4-5-20251001

uv run parse_anthropic.py anthropic claude-haiku-4-5-20251001 ../../../data/intermediate/raw_responses/anthropic/claude-haiku-4-5-20251001 ../../../data/intermediate/parsed_responses/anthropic/claude-haiku-4-5-20251001.parquet

# Claude Sonnet 4.5
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv anthropic claude-sonnet-4-5-20250929 ../../../data/intermediate/raw_responses/anthropic/claude-sonnet-4-5-20250929 20

uv run parse_anthropic.py anthropic claude-sonnet-4-5-20250929 ../../../data/intermediate/raw_responses/anthropic/claude-sonnet-4-5-20250929 ../../../data/intermediate/parsed_responses/anthropic/claude-sonnet-4-5-20250929.parquet

# Claude Opus 4.5
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv anthropic claude-opus-4-5-20251101 ../../../data/intermediate/raw_responses/anthropic/claude-opus-4-5-20251101 20

uv run parse_anthropic.py anthropic claude-opus-4-5-20251101 ../../../data/intermediate/raw_responses/anthropic/claude-opus-4-5-20251101 ../../../data/intermediate/parsed_responses/anthropic/claude-opus-4-5-20251101.parquet
