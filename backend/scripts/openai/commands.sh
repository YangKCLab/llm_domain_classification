# GPT-4o-mini, for testing purposes
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai gpt-4o-mini ../../../data/intermediate/raw_responses/openai/gpt4omini

uv run parse_openai.py openai gpt-4o-mini ../../../data/intermediate/raw_responses/openai/gpt4omini ../../../data/intermediate/parsed_responses/openai/gpt4omini.parquet

# GPT-4.1 nano
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai gpt-4.1-nano-2025-04-14 ../../../data/intermediate/raw_responses/openai/gpt-4.1-nano-2025-04-14

uv run parse_openai.py openai gpt-4.1-nano-2025-04-14 ../../../data/intermediate/raw_responses/openai/gpt-4.1-nano-2025-04-14 ../../../data/intermediate/parsed_responses/openai/gpt-4.1-nano-2025-04-14.parquet

# GPT-4.1 mini
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai gpt-4.1-mini-2025-04-14 ../../../data/intermediate/raw_responses/openai/gpt-4.1-mini-2025-04-14

uv run parse_openai.py openai gpt-4.1-mini-2025-04-14 ../../../data/intermediate/raw_responses/openai/gpt-4.1-mini-2025-04-14 ../../../data/intermediate/parsed_responses/openai/gpt-4.1-mini-2025-04-14.parquet

# GPT-4.1
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai gpt-4.1-2025-04-14 ../../../data/intermediate/raw_responses/openai/gpt-4.1-2025-04-14

uv run parse_openai.py openai gpt-4.1-2025-04-14 ../../../data/intermediate/raw_responses/openai/gpt-4.1-2025-04-14 ../../../data/intermediate/parsed_responses/openai/gpt-4.1-2025-04-14.parquet

# o3-mini
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai o3-mini-2025-01-31 ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31

uv run parse_openai.py openai o3-mini-2025-01-31 ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31 ../../../data/intermediate/parsed_responses/openai/o3-mini-2025-01-31.parquet

# o4-mini
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai o4-mini-2025-04-16 ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16

uv run parse_openai.py openai o4-mini-2025-04-16 ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16 ../../../data/intermediate/parsed_responses/openai/o4-mini-2025-04-16.parquet

# o1
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai o1-2024-12-17 ../../../data/intermediate/raw_responses/openai/o1-2024-12-17

uv run parse_openai.py openai o1-2024-12-17 ../../../data/intermediate/raw_responses/openai/o1-2024-12-17 ../../../data/intermediate/parsed_responses/openai/o1-2024-12-17.parquet

# o3
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai o3-2025-04-16 ../../../data/intermediate/raw_responses/openai/o3-2025-04-16

uv run parse_openai.py openai o3-2025-04-16 ../../../data/intermediate/raw_responses/openai/o3-2025-04-16 ../../../data/intermediate/parsed_responses/openai/o3-2025-04-16.parquet

# GPT-5 nano (reasoning model, but honors the strict json_schema so its message text
# is already clean JSON -> skip extract_ratings.py and use reconcile_direct.py)
uv run query_openai.py ../../../data/source/dashboard_query_list.csv openai gpt-5-nano-2025-08-07 ../../../data/intermediate/raw_responses/openai/gpt-5-nano-2025-08-07_raw

uv run reconcile_direct.py ../../../data/intermediate/raw_responses/openai/gpt-5-nano-2025-08-07_raw ../../../data/intermediate/raw_responses/openai/gpt-5-nano-2025-08-07

uv run parse_openai.py openai gpt-5-nano-2025-08-07 ../../../data/intermediate/raw_responses/openai/gpt-5-nano-2025-08-07 ../../../data/intermediate/parsed_responses/openai/gpt-5-nano-2025-08-07.parquet