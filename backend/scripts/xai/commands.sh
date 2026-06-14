# Grok3 mini beta
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv xai grok-3-mini-beta ../../../data/intermediate/raw_responses/xai/grok-3-mini-beta

uv run parse_xai.py xai grok-3-mini-beta ../../../data/intermediate/raw_responses/xai/grok-3-mini-beta ../../../data/intermediate/parsed_responses/xai/grok-3-mini-beta.parquet

# Grok3 beta
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv xai grok-3-beta ../../../data/intermediate/raw_responses/xai/grok-3-beta

uv run parse_xai.py xai grok-3-beta ../../../data/intermediate/raw_responses/xai/grok-3-beta ../../../data/intermediate/parsed_responses/xai/grok-3-beta.parquet

# Grok 4.3
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv xai grok-4.3 ../../../data/intermediate/raw_responses/xai/grok-4.3

uv run parse_xai.py xai grok-4.3 ../../../data/intermediate/raw_responses/xai/grok-4.3 ../../../data/intermediate/parsed_responses/xai/grok-4.3.parquet

# Grok 4.20 reasoning
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv xai grok-4.20-0309-reasoning ../../../data/intermediate/raw_responses/xai/grok-4.20-0309-reasoning

uv run parse_xai.py xai grok-4.20-0309-reasoning ../../../data/intermediate/raw_responses/xai/grok-4.20-0309-reasoning ../../../data/intermediate/parsed_responses/xai/grok-4.20-0309-reasoning.parquet

# Grok 4.20 non-reasoning
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv xai grok-4.20-0309-non-reasoning ../../../data/intermediate/raw_responses/xai/grok-4.20-0309-non-reasoning

uv run parse_xai.py xai grok-4.20-0309-non-reasoning ../../../data/intermediate/raw_responses/xai/grok-4.20-0309-non-reasoning ../../../data/intermediate/parsed_responses/xai/grok-4.20-0309-non-reasoning.parquet
