# Local LLM Evaluation Results

**Date:** 2026-11-20T09:41:02.802166+00:00

**API:** `http://127.0.0.1:11434`

**Context size:** 2048 tokens

**Maximum generated tokens:** 120

**CPU threads:** 1

## 1. Performance Comparison

| Metric | qwen2.5:0.5b | qwen2.5:1.5b |
|---|---:|---:|
| Average heuristic score | 82.0% | 70.0% |
| Average generation speed | 1.47 tokens/sec | 1.13 tokens/sec |
| Average request latency | 197.056 sec | 133.783 sec |
| Peak Ollama process RSS | 533.7 MB | 1326.2 MB |
| Successful tests | 5 | 4 |

## 2. Individual Test Results

### qwen2.5:0.5b

#### General Knowledge — Computer Networking

- Heuristic score: 100.0%
- Latency: 91.884 seconds
- Generation speed: 1.48 tokens/sec
- Prompt tokens: 55
- Generated tokens: 112

**Model response:**

```text
DNS (Domain Name System) is a network protocol that translates domain names into IP addresses. It works by mapping each domain name to a corresponding IP address. When you type a domain name into a web browser, the browser sends a request to the DNS server to resolve the domain name to an IP address. The DNS server then translates the domain name into an IP address and sends it back to the browser. This process is called "forwarding," and it allows users to access websites and other online resources by using their domain names instead of their IP addresses.
```

#### Persian Comprehension — Persian Technical Explanation

- Heuristic score: 75.0%
- Latency: 115.714 seconds
- Generation speed: 1.46 tokens/sec
- Prompt tokens: 86
- Generated tokens: 120

**Model response:**

```text
API (Application Programming Interface) یکی از جهت ارتباط بین دو نرم‌افزار، به عنوان یکی از جهت ارتباط بین دو نرم‌افزار، به عنوان یکی از جهت ارتباط بین دو نرم‌افزار، به عنوان یکی از جهت ارتباط بین دو نرم‌افزار، به عنوان یکی از جهت ا
```

#### Programming — Python Code Explanation

- Heuristic score: 60.0%
- Latency: 96.87 seconds
- Generation speed: 1.62 tokens/sec
- Prompt tokens: 70
- Generated tokens: 120

**Model response:**

```text
The Python code provided calculates the sum of a list of numbers and then divides the sum by the length of the list. Here's a step-by-step explanation of each line of code:

1. `numbers = [2, 4, 6, 8]`: This line initializes a list called `numbers` with the values [2, 4, 6, 8]. Each element in the list represents a number.

2. `result = sum(numbers) / len(numbers)`: This line performs two operations:
   - `sum(numbers)` calculates the sum of all the numbers
```

#### Mathematics — Basic Mathematical Reasoning

- Heuristic score: 75.0%
- Latency: 92.976 seconds
- Generation speed: 1.64 tokens/sec
- Prompt tokens: 64
- Generated tokens: 120
- Exact mathematical answer check: FAIL

**Model response:**

```text
To calculate the final price after a 20% discount, we need to follow these steps:

1. **Calculate the total cost without the discount:**
   - Each notebook costs 15 dollars.
   - There are 3 notebooks.
   - Therefore, the total cost without the discount is:
     \[
     15 \text{ dollars/notebook} \times 3 \text{ notebooks} = 45 \text{ dollars}
     \]

2. **Apply the 20% discount:**
   - The discount is 20% of
```

#### Context — Long Context Retrieval

- Heuristic score: 100.0%
- Latency: 587.835 seconds
- Generation speed: 1.13 tokens/sec
- Prompt tokens: 1117
- Generated tokens: 60

**Model response:**

```text
1. The project identifier is ORCHID-7319.
2. The primary color code is BLUE-COMET.
3. The database engine used is PostgreSQL.
4. The backup interval is 17 hours.
5. The release code is R-2048.
```

### qwen2.5:1.5b

#### General Knowledge — Computer Networking

- Heuristic score: 100.0%
- Latency: 123.799 seconds
- Generation speed: 1.15 tokens/sec
- Prompt tokens: 55
- Generated tokens: 120

**Model response:**

```text
DNS (Domain Name System) is a crucial component of computer networking that translates human-readable domain names into the numerical IP addresses that computers can understand. This process is essential for making the internet accessible and user-friendly.

Here's how it works:

1. **Domain Name System (DNS) Functionality**:
   - DNS is a hierarchical system that maps domain names to IP addresses.
   - It operates on a distributed network of servers, which are called DNS servers.
   - These servers store the mapping between domain names and IP addresses.

2. **How Domain Names are Translated to IP Addresses**
```

#### Persian Comprehension — Persian Technical Explanation

- Heuristic score: 75.0%
- Latency: 146.056 seconds
- Generation speed: 1.11 tokens/sec
- Prompt tokens: 86
- Generated tokens: 120

**Model response:**

```text
API (Application Programming Interface) یک سیستم تکنولوژی است که برای ارتباط بین دو نرم‌افزار می‌باشد. این سیستم به طور کلی شامل چند فرمت است که می‌توانند به صورت اولیه در نرم‌افزارهای مختلف اعمال شوند. این فرمت‌ها می‌توانند شامل فرمت‌های JSON، XML، پ
```

#### Programming — Python Code Explanation

- Heuristic score: 80.0%
- Latency: 135.638 seconds
- Generation speed: 1.12 tokens/sec
- Prompt tokens: 70
- Generated tokens: 120

**Model response:**

```text
Let's break down the Python code line by line:

1. `numbers = [2, 4, 6, 8]`
   - This line initializes a list called `numbers` with the elements `[2, 4, 6, 8]`.

2. `result = sum(numbers) / len(numbers)`
   - This line calculates the average (mean) of the elements in the `numbers` list.
   - `sum(numbers)` calculates the sum of all elements in the list.
   - `len(numbers)` calculates the number of elements in the list.
```

#### Mathematics — Basic Mathematical Reasoning

- Heuristic score: 25.0%
- Latency: 129.639 seconds
- Generation speed: 1.14 tokens/sec
- Prompt tokens: 64
- Generated tokens: 120
- Exact mathematical answer check: FAIL

**Model response:**

```text
To determine the final price of the notebooks after the discount, we need to follow these steps:

1. Calculate the total price before the discount.
2. Apply the discount to the total price.
3. The final price will be the total price minus the discount.

Let's go through each step in detail:

1. **Calculate the total price before the discount:**
   The store sells 3 notebooks for $15 each. Therefore, the total price before the discount is:
   \[
   3 \text{ notebooks} \times \$15 \text{ per notebook} =
```

## 3. Measurement Notes

- Generation speed is calculated using Ollama's `eval_count / eval_duration` statistics.
- Request latency includes API request overhead and generation time.
- Peak memory is a sampled sum of RSS for detected Ollama processes. Shared memory may be counted more than once.
- Heuristic scores are keyword-based and are not equivalent to human evaluation.
- Results are specific to this machine, runtime configuration, and test set.
