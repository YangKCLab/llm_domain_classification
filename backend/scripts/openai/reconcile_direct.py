import sys
import os
import json

# For reasoning models that already honor the strict json_schema (e.g. gpt-5*),
# the message item's text is already clean, schema-valid JSON. There is nothing
# to extract, so we skip the extra extract_ratings.py LLM round-trip and pull the
# message text straight into the shape parse_openai.py expects:
# output[0].content[0].text. The original response's `usage` is preserved so the
# cost calculation uses the queried model's real token counts.

if __name__ == "__main__":
    raw_resp_dir = sys.argv[1]
    output_dir = sys.argv[2]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    n_written = 0
    n_skipped = 0
    for file in os.listdir(raw_resp_dir):
        if not file.endswith(".txt"):
            continue
        domain = file[:-4]
        with open(os.path.join(raw_resp_dir, file), "r") as f:
            old_resp = json.load(f)

        # Find the assistant message item (output[0] is the reasoning block).
        resp_text = None
        for item in old_resp.get("output", []):
            if item.get("type") == "message" and item.get("role") == "assistant":
                resp_text = item["content"][0]["text"]
                break
        if resp_text is None:
            print(f"No message item found for {file}")
            n_skipped += 1
            continue

        # Validate it is clean JSON and stamp the domain from the filename.
        try:
            parsed = json.loads(resp_text)
        except json.JSONDecodeError as e:
            print(f"Message text is not valid JSON for {file}: {e}")
            n_skipped += 1
            continue
        parsed["domain"] = domain

        new_resp = {
            "usage": old_resp["usage"],
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "text": json.dumps(parsed),
                            "type": "text",
                        }
                    ],
                }
            ],
        }
        with open(os.path.join(output_dir, file), "w") as f:
            json.dump(new_resp, f, indent=2)
        n_written += 1

    print(f"Reconciled {n_written} files, skipped {n_skipped}")
