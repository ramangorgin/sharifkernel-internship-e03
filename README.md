# Sharif Kernel Internship — Week 3

**Intern:** Raman Gorgin  
**Repository:** [sharifkernel-internship-e03](https://github.com/ramangorgin/sharifkernel-internship-e03)  
**Week:** 3  
**Status:** All five assigned tasks completed

This repository contains the reports, supporting evaluation files, and website deliverable for the third week of my Sharif Kernel internship.

## Weekly progress summary

All five tasks assigned for this week have been completed.

| # | Task | Deliverable | Status |
|---|---|---|---|
| 1 | Local Language Model Deployment and Evaluation | Technical report, evaluation script, and generated results | Completed |
| 2 | Research on what is token system on user payments on the platform | Markdown research report | Completed |
| 3 | Research on applying for remote work in international companies | Markdown research report | Completed |
| 4 | Introduction to a practical gadget for programmers | Markdown research report | Completed |
| 5 | Design a website for my startup idea | Published Kurdish AI landing page | Completed |

## Task 1 — Local Language Model Deployment and Evaluation

**Main report:** [`1.Local Language Model Deployment and Evaluation.md`](./1.Local%20Language%20Model%20Deployment%20and%20Evaluation.md)  
**Supporting files:** [`local-llm-evaluation/`](./local-llm-evaluation/)

For this task, I documented the deployment of a local language model on Debian 13 using Ollama and evaluated its behavior through Ollama's local API.

The task focused on deploying an existing model with at least one billion parameters. The selected model was **Qwen2.5 1.5B** (`qwen2.5:1.5b`). This was a deployment and configuration exercise; the model was not trained from scratch.

### Evaluation script: `evaluate.py`

The Python script in `local-llm-evaluation/` automates repeatable tests by sending prompts to the locally running Ollama API. It compares the smaller `qwen2.5:0.5b` baseline with `qwen2.5:1.5b` using the same test cases and settings.

The test cases cover:
- General knowledge and a DNS-related question.
- Explaining a software/API concept in Persian.
- Generating a Python code solution.
- Solving a discount calculation, including an exact-answer check.
- Retrieving information from a synthetic long-context input.

The script records model responses and evaluation information, including response latency, token-generation information reported by Ollama, estimated generation speed, and sampled Ollama memory usage. It also applies simple, task-specific checks to produce indicative scores.

**Why this script was created:** manual testing makes consistent model comparisons difficult. Automating the same prompts and collecting the same measurements makes the evaluation more repeatable, easier to inspect, and easier to report. It is a practical comparison tool, not a comprehensive scientific benchmark. Some task scores are heuristic and should be interpreted accordingly.

### Evaluation outputs

Running the script produces or updates:
- `evaluation_results.json` — structured results suitable for further processing or comparison.
- `evaluation_results.md` — a human-readable summary of the evaluation.

The script, generated results, and full deployment/evaluation explanation are included so the work can be reviewed and reproduced.

## Task 2 — Token system and user payments

**Report:** [`2.Research on how to build a token system and user payment on the platform.md`](./2.Research%20on%20how%20to%20build%20a%20token%20system%20and%20user%20payment%20on%20the%20platform.md)

The research task is completed and documented in the Markdown report linked above.

## Task 3 — Applying for remote work in international companies

**Report:** [`3.Research on applying for remote work in international companies.md`](./3.Research%20on%20applying%20for%20remote%20work%20in%20international%20companies.md)

The research task is completed and documented in the Markdown report linked above.

## Task 4 — A practical gadget for programmers

**Report:** [`4.Introduction to a practical gadget for programmers.md`](./4.Introduction%20to%20a%20practical%20gadget%20for%20programmers.md)

The research task is completed and documented in the Markdown report linked above.

## Task 5 — Website for my startup idea

**Project:** Kurdish AI  
**Live website:** [https://ramangorgin.github.io/sharifkernel-internship-e03/kurdish-ai-landing/](https://ramangorgin.github.io/sharifkernel-internship-e03/kurdish-ai-landing/)

For this task, I designed and published a landing page for **Kurdish AI**, an early-stage startup concept focused on building AI-powered language technology for Sorani Kurdish.

The website introduces the concept, its motivation, potential capabilities, relevant AI technologies, and a possible development roadmap. It presents the idea; it does not claim that the proposed platform or services are already operational.

The website is implemented as a static frontend using HTML, CSS, and JavaScript, and is published through GitHub Pages.

**Website source:** [`kurdish-ai-landing/`](./kurdish-ai-landing/)

The repository root also contains an `index.html` redirect so visitors opening the repository's GitHub Pages root are directed to the landing page.

## Repository structure

```text
.
├── 1.Local Language Model Deployment and Evaluation.md
├── 2.Research on how to build a token system and user payment on the platform.md
├── 3.Research on applying for remote work in international companies.md
├── 4.Introduction to a practical gadget for programmers.md
├── index.html
├── kurdish-ai-landing/
│   ├── index.html
│   ├── README.md
│   ├── script.js
│   └── styles.css
└── local-llm-evaluation/
    ├── evaluate.py
    ├── evaluation_results.json
    └── evaluation_results.md
```

## How to review the deliverables

1. Read the Task 1 report for the deployment procedure, configuration, and evaluation methodology.
2. Review `local-llm-evaluation/evaluate.py` to see how the model tests are automated.
3. Inspect `evaluation_results.md` for readable results and `evaluation_results.json` for structured data.
4. Open the Markdown reports for Tasks 2, 3, and 4.
5. Visit the [published Kurdish AI landing page](https://ramangorgin.github.io/sharifkernel-internship-e03/kurdish-ai-landing/) to review Task 5.

## Completion statement

All five tasks assigned for Week 3 have been completed. Task 1 includes its technical report, evaluation script, and generated evaluation outputs; Tasks 2, 3, and 4 are documented in individual Markdown reports; and Task 5 is implemented as a static website and published on GitHub Pages.

This repository serves as the consolidated record of the work and deliverables submitted for the third week of the internship.
