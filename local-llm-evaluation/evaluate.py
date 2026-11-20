
#!/usr/bin/env python3
"""
Local LLM Evaluation
--------------------
Compares Qwen2.5 0.5B and Qwen2.5 1.5B through Ollama.

Outputs:
    evaluation_results.md
    evaluation_results.json

Requirements:
    pip install requests psutil
"""

import json
import re
import sys
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

import requests
import psutil


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:11434"

MODELS = [
    "qwen2.5:0.5b",
    "qwen2.5:1.5b",
]

CONTEXT_SIZE = 2048
MAX_GENERATED_TOKENS = 120
CPU_THREADS = 1
TEMPERATURE = 0

OUTPUT_MD = Path("evaluation_results.md")
OUTPUT_JSON = Path("evaluation_results.json")

REQUEST_TIMEOUT = 600
MEMORY_SAMPLE_INTERVAL = 0.25


# ============================================================
# TEST DATA
# ============================================================

# Each group contains terms that should appear in a reasonable
# answer. This is a simple heuristic, not semantic evaluation.

TESTS = [
    {
        "category": "General Knowledge",
        "name": "Computer Networking",
        "prompt": (
            "Explain what DNS does in computer networking. "
            "Explain how a domain name is translated into an IP "
            "address. Keep your answer concise."
        ),
        "groups": [
            ["domain name", "domain"],
            ["ip address", "ip"],
            ["dns server", "resolver", "name server"],
            ["translate", "resolve", "map"],
        ],
    },
    {
        "category": "Persian Comprehension",
        "name": "Persian Technical Explanation",
        "prompt": (
            "به زبان فارسی توضیح بده API چیست و چه کاربردی در "
            "ارتباط بین دو نرم‌افزار دارد. یک مثال ساده هم بزن."
        ),
        "groups": [
            ["رابط برنامه نویسی", "رابط برنامه‌نویسی", "api"],
            ["نرم افزار", "نرم‌افزار"],
            ["ارتباط", "درخواست"],
            ["پاسخ", "داده"],
        ],
    },
    {
        "category": "Programming",
        "name": "Python Code Explanation",
        "prompt": (
            "Explain the following Python code line by line. "
            "What does it calculate?\n\n"
            "numbers = [2, 4, 6, 8]\n"
            "result = sum(numbers) / len(numbers)\n"
            "print(result)"
        ),
        "groups": [
            ["list"],
            ["sum"],
            ["len", "length"],
            ["average", "mean"],
            ["5", "five"],
        ],
    },
    {
        "category": "Mathematics",
        "name": "Basic Mathematical Reasoning",
        "prompt": (
            "A store sells 3 notebooks for 15 dollars each and "
            "gives a 20 percent discount on the total price. "
            "What is the final price? Explain the calculation."
        ),
        "groups": [
            ["36"],
            ["45"],
            ["20"],
            ["discount", "دلار", "dollar"],
        ],
        "exact_number": "36",
    },
]


# ============================================================
# LONG-CONTEXT TEST
# ============================================================

# The document contains unique facts that the model must retrieve.
# The repeated neutral text increases the input length.

CONTEXT_FACTS = [
    ("Project name", "ORCHID"),
    ("Project identifier", "ORCHID-7319"),
    ("Primary color", "BLUE-COMET"),
    ("Database engine", "PostgreSQL"),
    ("Deployment region", "North-East-4"),
    ("Backup interval", "17 hours"),
    ("Monitoring service", "LANTERN"),
    ("Release code", "R-2048"),
]

FILLER = (
    "This document describes an imaginary software project. "
    "Its operational procedures include monitoring, maintenance, "
    "documentation, database administration, deployment planning, "
    "testing, access control, and regular backup verification. "
    "The information in this section is background material and "
    "should not be confused with the unique configuration facts. "
)

LONG_DOCUMENT = (
    "PROJECT TECHNICAL DOCUMENTATION\n\n"
    + "\n".join(f"{key}: {value}" for key, value in CONTEXT_FACTS)
    + "\n\n"
    + (FILLER * 18)
    + "\n\nEND OF DOCUMENT."
)

CONTEXT_TEST = {
    "category": "Context",
    "name": "Long Context Retrieval",
    "prompt": (
        "Read the following technical document carefully.\n\n"
        + LONG_DOCUMENT
        + "\n\nAnswer these questions:\n"
        "1. What is the project identifier?\n"
        "2. What is the primary color code?\n"
        "3. Which database engine is used?\n"
        "4. What is the backup interval?\n"
        "5. What is the release code?\n"
        "Return the five answers clearly."
    ),
    "groups": [
        ["ORCHID-7319"],
        ["BLUE-COMET"],
        ["PostgreSQL"],
        ["17 hours"],
        ["R-2048"],
    ],
}

TESTS.append(CONTEXT_TEST)


# ============================================================
# TEXT AND SCORING UTILITIES
# ============================================================

def normalize(text):
    """Normalize text for simple keyword matching."""
    text = text.lower()
    text = text.replace("ي", "ی").replace("ك", "ک")
    return re.sub(r"\s+", " ", text)


def calculate_score(answer, groups):
    """
    Percentage of expected keyword groups found in the answer.
    Each group is considered passed if at least one alternative
    keyword is present.
    """
    normalized = normalize(answer)

    if not groups:
        return 0

    passed = 0

    for group in groups:
        if any(normalize(word) in normalized for word in group):
            passed += 1

    return round((passed / len(groups)) * 100, 1)


# ============================================================
# MEMORY MONITOR
# ============================================================

class MemoryMonitor:
    """
    Samples the RSS of processes associated with Ollama.

    RSS is an approximate process-memory measurement.
    Summing RSS can double-count shared memory between processes.
    """

    def __init__(self):
        self.peak_mb = 0.0
        self.running = False
        self.thread = None

    @staticmethod
    def get_ollama_memory():
        total = 0

        for proc in psutil.process_iter(
            ["name", "cmdline", "memory_info"]
        ):
            try:
                name = (proc.info["name"] or "").lower()
                cmdline = " ".join(
                    proc.info["cmdline"] or []
                ).lower()

                if (
                    "ollama" in name
                    or "ollama" in cmdline
                ):
                    total += proc.info["memory_info"].rss

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                TypeError,
                AttributeError,
            ):
                continue

        return total / (1024 * 1024)

    def sample(self):
        while self.running:
            current = self.get_ollama_memory()
            self.peak_mb = max(self.peak_mb, current)
            time.sleep(MEMORY_SAMPLE_INTERVAL)

    def start(self):
        self.peak_mb = self.get_ollama_memory()
        self.running = True
        self.thread = threading.Thread(
            target=self.sample,
            daemon=True,
        )
        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        self.peak_mb = max(
            self.peak_mb,
            self.get_ollama_memory(),
        )

        return round(self.peak_mb, 1)


# ============================================================
# OLLAMA API
# ============================================================

def check_api():
    try:
        response = requests.get(
            f"{API_URL}/api/version",
            timeout=5,
        )
        response.raise_for_status()

        print(
            f"[OK] Ollama API version: "
            f"{response.json().get('version', 'unknown')}"
        )

    except requests.RequestException as error:
        print(f"[ERROR] Cannot connect to Ollama: {error}")
        print("Make sure the Ollama service is running.")
        sys.exit(1)


def check_model(model):
    try:
        response = requests.post(
            f"{API_URL}/api/show",
            json={"name": model},
            timeout=15,
        )
        response.raise_for_status()
        return True

    except requests.RequestException:
        return False


def generate(model, prompt, num_predict=MAX_GENERATED_TOKENS):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "5m",
        "options": {
            "temperature": TEMPERATURE,
            "num_ctx": CONTEXT_SIZE,
            "num_predict": num_predict,
            "num_thread": CPU_THREADS,
        },
    }

    started = time.perf_counter()

    response = requests.post(
        f"{API_URL}/api/generate",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    elapsed = time.perf_counter() - started
    response.raise_for_status()

    data = response.json()

    generated_tokens = data.get("eval_count", 0)
    generation_duration = data.get("eval_duration", 0)

    tokens_per_second = (
        generated_tokens / (generation_duration / 1e9)
        if generation_duration > 0
        else 0
    )

    return {
        "answer": data.get("response", "").strip(),
        "latency_seconds": round(elapsed, 3),
        "generation_seconds": round(
            generation_duration / 1e9, 3
        ),
        "prompt_tokens": data.get("prompt_eval_count", 0),
        "generated_tokens": generated_tokens,
        "tokens_per_second": round(tokens_per_second, 2),
        "load_seconds": round(
            data.get("load_duration", 0) / 1e9, 3
        ),
        "total_seconds": round(
            data.get("total_duration", 0) / 1e9, 3
        ),
    }


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_model(model):
    print("\n" + "=" * 65)
    print(f"MODEL: {model}")
    print("=" * 65)

    if not check_model(model):
        print(f"[ERROR] Model not found: {model}")
        print(f"Run: ollama pull {model}")
        return None

    monitor = MemoryMonitor()
    monitor.start()

    results = []

    try:
        # Warm-up: excluded from answer quality and speed statistics.
        print("[INFO] Warming up model...")

        generate(
            model,
            "Reply with the word READY.",
            num_predict=8,
        )

        for index, test in enumerate(TESTS, start=1):
            print(
                f"\n[{index}/{len(TESTS)}] "
                f"{test['category']}: {test['name']}"
            )

            try:
                result = generate(
                    model,
                    test["prompt"],
                )

                score = calculate_score(
                    result["answer"],
                    test["groups"],
                )

                if "exact_number" in test:
                    exact = test["exact_number"]
                    exact_match = bool(
                        re.search(
                            rf"(?<!\d){re.escape(exact)}(?!\d)",
                            result["answer"],
                        )
                    )
                    result["exact_match"] = exact_match

                else:
                    result["exact_match"] = None

                result["score"] = score
                result["category"] = test["category"]
                result["test_name"] = test["name"]

                results.append(result)

                print(f"  Score: {score}%")
                print(
                    f"  Speed: {result['tokens_per_second']} "
                    "tokens/sec"
                )
                print(
                    f"  Latency: {result['latency_seconds']} sec"
                )
                print(
                    f"  Generated tokens: "
                    f"{result['generated_tokens']}"
                )
                print(
                    "  Answer: "
                    + result["answer"][:250].replace("\n", " ")
                )

            except requests.RequestException as error:
                print(f"  [ERROR] Request failed: {error}")

    finally:
        peak_memory = monitor.stop()

    successful = len(results)

    average_speed = (
        sum(r["tokens_per_second"] for r in results)
        / successful
        if successful else 0
    )

    average_latency = (
        sum(r["latency_seconds"] for r in results)
        / successful
        if successful else 0
    )

    average_score = (
        sum(r["score"] for r in results)
        / successful
        if successful else 0
    )

    total_generated = sum(
        r["generated_tokens"] for r in results
    )

    summary = {
        "model": model,
        "successful_tests": successful,
        "total_tests": len(TESTS),
        "average_score_percent": round(average_score, 1),
        "average_tokens_per_second": round(average_speed, 2),
        "average_latency_seconds": round(average_latency, 3),
        "peak_ollama_process_rss_mb": peak_memory,
        "total_generated_tokens": total_generated,
        "results": results,
    }

    print("\n" + "-" * 65)
    print("MODEL SUMMARY")
    print("-" * 65)
    print(f"Average heuristic score: {average_score:.1f}%")
    print(f"Average speed: {average_speed:.2f} tokens/sec")
    print(f"Average latency: {average_latency:.3f} sec")
    print(f"Peak Ollama process RSS: {peak_memory:.1f} MB")

    return summary


# ============================================================
# REPORT GENERATION
# ============================================================

def generate_markdown(all_results):
    lines = [
        "# Local LLM Evaluation Results",
        "",
        f"**Date:** {datetime.now(timezone.utc).isoformat()}",
        "",
        f"**API:** `{API_URL}`",
        "",
        f"**Context size:** {CONTEXT_SIZE} tokens",
        "",
        f"**Maximum generated tokens:** {MAX_GENERATED_TOKENS}",
        "",
        f"**CPU threads:** {CPU_THREADS}",
        "",
        "## 1. Performance Comparison",
        "",
        "| Metric | " + " | ".join(
            item["model"] for item in all_results
        ) + " |",
        "|---|" + "|".join(
            "---:" for _ in all_results
        ) + "|",
    ]

    metrics = [
        (
            "Average heuristic score",
            "average_score_percent",
            "%",
        ),
        (
            "Average generation speed",
            "average_tokens_per_second",
            " tokens/sec",
        ),
        (
            "Average request latency",
            "average_latency_seconds",
            " sec",
        ),
        (
            "Peak Ollama process RSS",
            "peak_ollama_process_rss_mb",
            " MB",
        ),
        (
            "Successful tests",
            "successful_tests",
            "",
        ),
    ]

    for label, key, suffix in metrics:
        values = [
            f"{item[key]}{suffix}"
            for item in all_results
        ]
        lines.append("| " + label + " | " + " | ".join(values) + " |")

    lines.extend([
        "",
        "## 2. Individual Test Results",
        "",
    ])

    for item in all_results:
        lines.extend([
            f"### {item['model']}",
            "",
        ])

        for result in item["results"]:
            lines.extend([
                f"#### {result['category']} — {result['test_name']}",
                "",
                f"- Heuristic score: {result['score']}%",
                f"- Latency: {result['latency_seconds']} seconds",
                f"- Generation speed: {result['tokens_per_second']} tokens/sec",
                f"- Prompt tokens: {result['prompt_tokens']}",
                f"- Generated tokens: {result['generated_tokens']}",
            ])

            if result["exact_match"] is not None:
                lines.append(
                    f"- Exact mathematical answer check: "
                    f"{'PASS' if result['exact_match'] else 'FAIL'}"
                )

            lines.extend([
                "",
                "**Model response:**",
                "",
                "```text",
                result["answer"].replace("```", "'''"),
                "```",
                "",
            ])

    lines.extend([
        "## 3. Measurement Notes",
        "",
        "- Generation speed is calculated using Ollama's "
        "`eval_count / eval_duration` statistics.",
        "- Request latency includes API request overhead and "
        "generation time.",
        "- Peak memory is a sampled sum of RSS for detected "
        "Ollama processes. Shared memory may be counted more "
        "than once.",
        "- Heuristic scores are keyword-based and are not "
        "equivalent to human evaluation.",
        "- Results are specific to this machine, runtime "
        "configuration, and test set.",
        "",
    ])

    return "\n".join(lines)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 65)
    print("LOCAL LANGUAGE MODEL EVALUATION")
    print("=" * 65)

    check_api()

    print(f"\nModels: {', '.join(MODELS)}")
    print(f"Context: {CONTEXT_SIZE}")
    print(f"CPU threads: {CPU_THREADS}")

    all_results = []

    for model in MODELS:
        result = evaluate_model(model)

        if result:
            all_results.append(result)

    if not all_results:
        print("\n[ERROR] No models were successfully evaluated.")
        sys.exit(1)

    OUTPUT_JSON.write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    OUTPUT_MD.write_text(
        generate_markdown(all_results),
        encoding="utf-8",
    )

    print("\n" + "=" * 65)
    print("EVALUATION COMPLETED")
    print("=" * 65)

    print(f"\nMarkdown report: {OUTPUT_MD.resolve()}")
    print(f"JSON results:    {OUTPUT_JSON.resolve()}")

    print("\nYou can copy evaluation_results.md into your main report.")


if __name__ == "__main__":
    main()
