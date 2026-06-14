# meta-llama/Llama-3.3-70B-Instruct-Turbo
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together meta-llama/Llama-3.3-70B-Instruct-Turbo ../../../data/intermediate/raw_responses/together/Llama-3.3-70B-Instruct-Turbo

uv run parse_together.py together Llama-3.3-70B-Instruct-Turbo ../../../data/intermediate/raw_responses/together/Llama-3.3-70B-Instruct-Turbo ../../../data/intermediate/parsed_responses/together/Llama-3.3-70B-Instruct-Turbo.parquet

# meta-llama/Llama-4-Scout-17B-16E-Instruct
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together meta-llama/Llama-4-Scout-17B-16E-Instruct ../../../data/intermediate/raw_responses/together/Llama-4-Scout-17B-16E-Instruct

uv run parse_together.py together Llama-4-Scout-17B-16E-Instruct ../../../data/intermediate/raw_responses/together/Llama-4-Scout-17B-16E-Instruct ../../../data/intermediate/parsed_responses/together/Llama-4-Scout-17B-16E-Instruct.parquet

# meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8 ../../../data/intermediate/raw_responses/together/Llama-4-Maverick-17B-128E-Instruct-FP8

uv run parse_together.py together Llama-4-Maverick-17B-128E-Instruct-FP8 ../../../data/intermediate/raw_responses/together/Llama-4-Maverick-17B-128E-Instruct-FP8 ../../../data/intermediate/parsed_responses/together/Llama-4-Maverick-17B-128E-Instruct-FP8.parquet

# deepseek-ai/DeepSeek-V3
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together deepseek-ai/DeepSeek-V3 ../../../data/intermediate/raw_responses/together/DeepSeek-V3

uv run parse_together.py together DeepSeek-V3 ../../../data/intermediate/raw_responses/together/DeepSeek-V3 ../../../data/intermediate/parsed_responses/together/DeepSeek-V3.parquet

# deepseek-ai/DeepSeek-R1
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together deepseek-ai/DeepSeek-R1 ../../../data/intermediate/raw_responses/together/DeepSeek-R1

uv run parse_together.py together DeepSeek-R1 ../../../data/intermediate/raw_responses/together/DeepSeek-R1 ../../../data/intermediate/parsed_responses/together/DeepSeek-R1.parquet

# deepseek-ai/DeepSeek-V4-Pro
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together deepseek-ai/DeepSeek-V4-Pro ../../../data/intermediate/raw_responses/together/DeepSeek-V4-Pro

uv run parse_together.py together DeepSeek-V4-Pro ../../../data/intermediate/raw_responses/together/DeepSeek-V4-Pro ../../../data/intermediate/parsed_responses/together/DeepSeek-V4-Pro.parquet

# deepseek-ai/DeepSeek-V4-Flash (verify serverless availability + pricing first)
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together deepseek-ai/DeepSeek-V4-Flash ../../../data/intermediate/raw_responses/together/DeepSeek-V4-Flash

uv run parse_together.py together DeepSeek-V4-Flash ../../../data/intermediate/raw_responses/together/DeepSeek-V4-Flash ../../../data/intermediate/parsed_responses/together/DeepSeek-V4-Flash.parquet

# openai/gpt-oss-20b
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together openai/gpt-oss-20b ../../../data/intermediate/raw_responses/together/gpt-oss-20b

uv run parse_together.py together gpt-oss-20b ../../../data/intermediate/raw_responses/together/gpt-oss-20b ../../../data/intermediate/parsed_responses/together/gpt-oss-20b.parquet

# openai/gpt-oss-120b
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together openai/gpt-oss-120b ../../../data/intermediate/raw_responses/together/gpt-oss-120b

uv run parse_together.py together gpt-oss-120b ../../../data/intermediate/raw_responses/together/gpt-oss-120b ../../../data/intermediate/parsed_responses/together/gpt-oss-120b.parquet

# moonshotai/Kimi-K2.6
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together moonshotai/Kimi-K2.6 ../../../data/intermediate/raw_responses/together/Kimi-K2.6

uv run parse_together.py together Kimi-K2.6 ../../../data/intermediate/raw_responses/together/Kimi-K2.6 ../../../data/intermediate/parsed_responses/together/Kimi-K2.6.parquet

# MiniMaxAI/MiniMax-M2.7
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together MiniMaxAI/MiniMax-M2.7 ../../../data/intermediate/raw_responses/together/MiniMax-M2.7

uv run parse_together.py together MiniMax-M2.7 ../../../data/intermediate/raw_responses/together/MiniMax-M2.7 ../../../data/intermediate/parsed_responses/together/MiniMax-M2.7.parquet

# MiniMaxAI/MiniMax-M3
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together MiniMaxAI/MiniMax-M3 ../../../data/intermediate/raw_responses/together/MiniMax-M3

uv run parse_together.py together MiniMax-M3 ../../../data/intermediate/raw_responses/together/MiniMax-M3 ../../../data/intermediate/parsed_responses/together/MiniMax-M3.parquet

# zai-org/GLM-5.1
uv run ../openai/query_openai.py ../../../data/source/dashboard_query_list.csv together zai-org/GLM-5.1 ../../../data/intermediate/raw_responses/together/GLM-5.1

uv run parse_together.py together GLM-5.1 ../../../data/intermediate/raw_responses/together/GLM-5.1 ../../../data/intermediate/parsed_responses/together/GLM-5.1.parquet
