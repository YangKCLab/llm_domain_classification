# o3-mini-2025-01-31
uv run extract_ratings.py ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31_raw ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31_extracted

uv run reconcile_extracted_ratings.py ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31_raw ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31_extracted ../../../data/intermediate/raw_responses/openai/o3-mini-2025-01-31

# o3-2025-04-16
uv run extract_ratings.py ../../../data/intermediate/raw_responses/openai/o3-2025-04-16_raw ../../../data/intermediate/raw_responses/openai/o3-2025-04-16_extracted

uv run reconcile_extracted_ratings.py ../../../data/intermediate/raw_responses/openai/o3-2025-04-16_raw ../../../data/intermediate/raw_responses/openai/o3-2025-04-16_extracted ../../../data/intermediate/raw_responses/openai/o3-2025-04-16

# o4-mini-2025-04-16
uv run extract_ratings.py ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16_raw ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16_extracted

uv run reconcile_extracted_ratings.py ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16_raw ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16_extracted ../../../data/intermediate/raw_responses/openai/o4-mini-2025-04-16

# o1-2024-12-17
uv run extract_ratings.py ../../../data/intermediate/raw_responses/openai/o1-2024-12-17_raw ../../../data/intermediate/raw_responses/openai/o1-2024-12-17_extracted

uv run reconcile_extracted_ratings.py ../../../data/intermediate/raw_responses/openai/o1-2024-12-17_raw ../../../data/intermediate/raw_responses/openai/o1-2024-12-17_extracted ../../../data/intermediate/raw_responses/openai/o1-2024-12-17

# NOTE: gpt-5-nano-2025-08-07 returns clean schema-valid JSON, so it does NOT use the
# extract/reconcile pass above. Its query/reconcile/parse lines live in commands.sh and
# use reconcile_direct.py instead.
