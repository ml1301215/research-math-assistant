"""
MIT License

Copyright (c) 2026 Lve Meng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from pickle import FALSE
import sys
import json
from textwrap import indent
import requests
import argparse
import logging

# --- CONFIGURATION ---
MODEL_NAME = "google/gemini-3-pro-preview"
BASE_URL = "https://llm-api-jpe.dou.chat"
API_URL = f"{BASE_URL}/v1/chat/completions"
TEMPERATURE = 0.1
MAX_TOKENS = 24576

def load_config(config_path):
    """Load config from JSON file, overriding global defaults."""
    global MODEL_NAME, BASE_URL, API_URL, TEMPERATURE, MAX_TOKENS
    global step1_prompt, self_improvement_prompt, correction_prompt
    global verification_system_prompt, verification_remider, check_verification_prompt

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_cfg = cfg.get("api", {})
    if api_cfg.get("base_url"):
        BASE_URL = api_cfg["base_url"]
        API_URL = f"{BASE_URL}/v1/chat/completions"
    if api_cfg.get("model_name"):
        MODEL_NAME = api_cfg["model_name"]
    if api_cfg.get("api_key"):
        os.environ["OPENAI_API_KEY"] = api_cfg["api_key"]
    if api_cfg.get("temperature") is not None:
        TEMPERATURE = float(api_cfg["temperature"])
    if api_cfg.get("max_tokens") is not None:
        MAX_TOKENS = int(api_cfg["max_tokens"])

    prompts_cfg = cfg.get("prompts", {})
    if prompts_cfg.get("step1_prompt") is not None:
        step1_prompt = prompts_cfg["step1_prompt"]
    if prompts_cfg.get("self_improvement_prompt") is not None:
        self_improvement_prompt = prompts_cfg["self_improvement_prompt"]
    if prompts_cfg.get("correction_prompt") is not None:
        correction_prompt = prompts_cfg["correction_prompt"]
    if prompts_cfg.get("verification_system_prompt") is not None:
        verification_system_prompt = prompts_cfg["verification_system_prompt"]
    if prompts_cfg.get("verification_remider") is not None:
        verification_remider = prompts_cfg["verification_remider"]
    if prompts_cfg.get("check_verification_prompt") is not None:
        check_verification_prompt = prompts_cfg["check_verification_prompt"]

# Global variables for logging
_log_file = None
original_print = print

def log_print(*args, **kwargs):
    """
    Custom print function that writes to both stdout and log file.
    """
    # Convert all arguments to strings and join them
    message = ' '.join(str(arg) for arg in args)
    
    # Add timestamp to lines starting with ">>>>>"
    if message.startswith('>>>>>'):
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[{timestamp}] {message}"
    
    # Print to stdout
    original_print(message)
    
    # Also write to log file if specified
    if _log_file is not None and not _log_file.closed:
        _log_file.write(message + '\n')
        _log_file.flush()  # Ensure immediate writing
        # Force OS-level flush so tailing tools see updates promptly on Windows
        try:
            os.fsync(_log_file.fileno())
        except (OSError, ValueError):
            pass

# Replace the built-in print function
print = log_print

def set_log_file(log_file_path):
    """Set the log file for output."""
    global _log_file
    if log_file_path:
        try:
            # Line-buffered to improve real-time log visibility
            _log_file = open(log_file_path, 'w', encoding='utf-8', buffering=1)
            return True
        except Exception as e:
            print(f"Error opening log file {log_file_path}: {e}")
            return False
    return True

def close_log_file():
    """Close the log file if it's open."""
    global _log_file
    if _log_file is not None:
        _log_file.close()
        _log_file = None

def save_memory(memory_file, problem_statement, other_prompts, current_iteration, max_runs, solution=None, verify=None):
    """
    Save the current state to a memory file.
    """
    memory = {
        "problem_statement": problem_statement,
        "other_prompts": other_prompts,
        "current_iteration": current_iteration,
        "max_runs": max_runs,
        "solution": solution,
        "verify": verify,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    
    try:
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        print(f"Memory saved to {memory_file}")
        return True
    except Exception as e:
        print(f"Error saving memory to {memory_file}: {e}")
        return False

def load_memory(memory_file):
    """
    Load the state from a memory file.
    """
    try:
        with open(memory_file, 'r', encoding='utf-8') as f:
            memory = json.load(f)
        print(f"Memory loaded from {memory_file}")
        return memory
    except Exception as e:
        print(f"Error loading memory from {memory_file}: {e}")
        return None

step1_prompt = """
### Core Instructions ###

*   **Target:** Solve research-level mathematical problem.
*   **Rigor is Paramount:** Your primary goal is to solve the problem and produce new mathematics. 
*   **Honesty About Completeness:** If you cannot find a complete solution(hope not), you must **explicitly state that no complete solution is found**. A partial result is significant if it represents a substantial advancement toward a full solution. Examples include:
    *   Proving a new key lemma.
    *   Establishing a critical new property of the mathematical objects in the problem.
    *   Proving a new result about the problem.
*   **Use TeX for All Mathematics:** All mathematical variables, expressions, and relations must be enclosed in TeX delimiters (e.g., `Let $n$ be an integer.`).

### Output Format ###

Your response MUST be a complete LaTeX document that compiles in Overleaf and matches this exact structure.

**Required LaTeX Skeleton**

*   Start with `\\documentclass[reqno]{amsart}`.
*   Use this package block (same order):
    `\\usepackage{amsmath, amsthm, amsfonts, amssymb, mathrsfs, hyperref}`
    `\\usepackage[utf8]{inputenc}`
    `\\usepackage[T1]{fontenc}`
*   Define theorem environments: `theorem, lemma, proposition, corollary, definition, remark, example`.
*   Include `\\title{...}`, `\\author{AI Researcher}`, `\\date{\\today}`.
*   Use `\\begin{document}` ... `\\end{document}`, and call `\\maketitle` after the abstract.

**Document Sections**

*   `\\begin{abstract} ... \\end{abstract}`: Summary (verdict + method sketch).
*   `\\section{Problem}`: State the problem in LaTeX.
*   `\\section{Solution}`: Full, step-by-step rigorous proof or partial results.
*   If a complete solution is not found, state it clearly in the Solution section. 
*   End with `\\begin{thebibliography}{99}` ... `\\end{thebibliography}`.

**Citations and References**

*   Every formula or theorem must be accompanied by a citation using `\\cite{...}` with the corresponding bibitem if necessary.
*   Each bibitem should include enough bibliographic detail and (if available) a URL.

### Self-Correction Instruction ###

Before finalizing your output, carefully review your Abstract, Solution, and References to ensure they are clean, rigorous, and strictly adhere to all instructions provided above. Verify that every statement contributes directly to the final, coherent mathematical argument and that any incompleteness is explicitly stated. Additionally, ensure that all references are accurate and relevant:
*   Verify that each reference URL is valid and points to a reputable mathematical resource.
*   Must verify that the propositions used are exactly the same as those in the corresponding cited application literature.
*   Check that important formulas and theorems are properly referenced with appropriate sources.

"""

self_improvement_prompt = """
You have an opportunity to improve your solution. Please review your solution carefully. Correct errors and fill justification gaps if any. If a complete proof is not found, continue to explore deeper towards the solution. Your second round of output should strictly follow the instructions in the system prompt.
"""

check_verification_prompt = """
Can you carefully review each item in your list of findings? Are they valid or overly strict? An expert grader must be able to distinguish between a genuine flaw and a concise argument that is nonetheless sound, and to correct their own assessment when necessary.

Additionally, please verify the accuracy and relevance of all references cited in your verification:
*   Check that each reference URL is valid and points to a reputable mathematical resource
*   Ensure that the cited references actually support the mathematical concepts or results mentioned
*   Must verify that the propositions used are exactly the same as those in the corresponding cited application literature.

 If you feel that modifications to any item or its justification is necessary, or if you find issues with the references, please produce a new list and updated references. In your final output, please directly start with **Summary** (no need to justify the new list).
"""

correction_prompt = """
Below is the bug report. If you agree with certain item in it, improve your solution towards the solution of the problem. Note that the evaluator who generates the bug report can misunderstand your solution and thus make mistakes. If you do not agree with certain item in the bug report, please add detailed explanations to avoid such misunderstanding. Your new solution should strictly follow the instructions in the system prompt.
"""

verification_system_prompt = """
You are an expert mathematician. Your primary task is to rigorously verify the provided mathematical work. A solution is to be judged correct **only if every claimed result is rigorously justified. And the solution must contain some new mathematics.(Not being proved in any references)** A solution that arrives at a correct final answer through flawed reasoning, educated guesses, or with gaps in its arguments must be flagged as incorrect or incomplete.

### Instructions ###

**1. Core Instructions**
*   Your sole task is to find and report all issues in the provided solution. You must act as a **verifier**, NOT a solver. **Do NOT attempt to correct the errors or fill the gaps you find.**
*   You must perform a **step-by-step** check of the entire solution. This analysis will be presented in a **Detailed Verification Log**, where you justify your assessment of each step: for correct steps, a brief justification suffices; for steps with errors or gaps, you must provide a detailed explanation.

**2. How to Handle Issues in the Solution**
When you identify an issue in a step, you MUST first classify it into one of the following two categories and then follow the specified procedure.

*   **a. Critical Error:**
    This is any error that breaks the logical chain of the proof. This includes both **logical fallacies** (e.g., claiming that `A>B, C>D` implies `A-C>B-D`) and **factual errors** (e.g., a calculation error like `2+3=6`).
    *   **Procedure:**
        *   Explain the specific error and state that it **invalidates the current line of reasoning**.
        *   Do NOT check any further steps that rely on this error.
        *   You MUST, however, scan the rest of the solution to identify and verify any fully independent parts. For example, if a proof is split into multiple cases, an error in one case does not prevent you from checking the other cases.

*   **b. Justification Gap:**
    This is for steps where the conclusion may be correct, but the provided argument is incomplete, hand-wavy, or lacks sufficient rigor.
    *   **Procedure:**
        *   Explain the gap in the justification.
        *   State that you will **assume the step's conclusion is true** for the sake of argument.
        *   Then, proceed to verify all subsequent steps to check if the remainder of the argument is sound.

**3. Output Format**
Your response MUST be structured into two main sections: a **Summary** followed by the **Detailed Verification Log**.

*   **a. Summary**
    This section MUST be at the very beginning of your response. It must contain two components:
    *   **Final Verdict**: A single, clear sentence declaring the overall validity of the work. For example: "The solution is correct," "The solution contains a Critical Error and is therefore invalid," or "The work provides correct partial results but no complete proof."
    *   **List of Findings**: A bulleted list that summarizes **every** issue you discovered. For each finding, you must provide:
        *   **Location:** A direct quote of the key phrase or equation where the issue occurs.
        *   **Issue:** A brief description of the problem and its classification (**Critical Error** or **Justification Gap**).

*   **b. Detailed Verification Log**
    Following the summary, provide the full, step-by-step verification log as defined in the Core Instructions. When you refer to a specific part of the solution, **quote the relevant text** to make your reference clear before providing your detailed analysis of that part. 
**Example of the Required Summary Format**
*This is a generic example to illustrate the required format. Your findings must be based on the actual solution provided below.*

**Final Verdict:** The solution is **invalid** because it only provides  partial results but no complete proof towards the solution of the problem.

**List of Findings:**
*   **Location:** "By interchanging the limit and the integral, we get..."
    *   **Issue:** Justification Gap - The solution interchanges a limit and an integral without providing justification, such as proving uniform convergence.
*   **Location:** "From $A > B$ and $C > D$, it follows that $A-C > B-D$"
    *   **Issue:** Critical Error - This step is a logical fallacy. Subtracting inequalities in this manner is not a valid mathematical operation.

**Detailed Verification Log:**
[Step-by-step analysis would go here...]


"""

verification_remider = """
### Verification Task Reminder ###

Your task is to act as a research-level problem referee. The solution above is provided in LaTeX paper format. Focus on the mathematical content in the document body, especially the Solution section. Now, generate the **summary** and the **step-by-step verification log** for the solution above. In your log, justify each correct step and explain in detail any errors or justification gaps you find, as specified in the instructions above. If the work is partial, you should indicate the limitations of the solution and the parts that are not proved.
"""

def get_api_key():
    """
    Retrieves the API key from environment variables.
    Exits if the key is not found.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set the variable, e.g., 'export OPENAI_API_KEY=\"your_api_key\"'")
        sys.exit(1)
    return api_key

def read_file_content(filepath):
    """
    Reads and returns the content of a file.
    Exits if the file cannot be read.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)

def build_request_payload(system_prompt, question_prompt, other_prompts=None):
    """
    Builds the JSON payload for the OpenAI compatible API request.
    """
    messages = []
    
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": question_prompt
    })

    if other_prompts:
        for prompt in other_prompts:
            messages.append({
                "role": "user",
                "content": prompt
            })

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }

    return payload

def send_api_request(api_key, payload):
    """
    Sends the request to the OpenAI compatible API and returns the response.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    print("Sending request to API...")
    print(f"API URL: {API_URL}")
    log_headers = headers.copy()
    if "Authorization" in log_headers:
        log_headers["Authorization"] = "Bearer ***"
    print(f"Headers: {log_headers}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = None
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()

        def _safe_int(v):
            try:
                return int(v or 0)
            except (TypeError, ValueError):
                return 0

        def _find_usage(obj):
            """Recursively find a usage-like dict in provider-specific response shapes."""
            if isinstance(obj, dict):
                has_any = any(k in obj for k in ("prompt_tokens", "completion_tokens", "total_tokens"))
                if has_any:
                    return obj
                for vv in obj.values():
                    found = _find_usage(vv)
                    if found is not None:
                        return found
            elif isinstance(obj, list):
                for vv in obj:
                    found = _find_usage(vv)
                    if found is not None:
                        return found
            return None

        usage = _find_usage(response_json)
        if usage is not None:
            prompt_tokens = _safe_int(usage.get("prompt_tokens", 0))
            completion_tokens = _safe_int(usage.get("completion_tokens", 0))
            total_tokens = _safe_int(usage.get("total_tokens", 0))
            if total_tokens == 0 and (prompt_tokens > 0 or completion_tokens > 0):
                total_tokens = prompt_tokens + completion_tokens
            print(f">>>>>>> TOKEN_USAGE: prompt={prompt_tokens} completion={completion_tokens} total={total_tokens}")
        return response_json
    except requests.exceptions.HTTPError as e:
        print(f"Error during API request: {e}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Raw API Response: {response.text}")
        raise e
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        raise e

def extract_text_from_response(response_data):
    """
    Extracts the generated text from the API response JSON.
    Handles potential errors if the response format is unexpected.
    """
    try:
        return response_data['choices'][0]['message']['content']
    except (KeyError, IndexError, TypeError) as e:
        print("Error: Could not extract text from the API response.")
        print(f"Reason: {e}")
        print("Full API Response:")
        print(json.dumps(response_data, indent=2))
        raise e 

def extract_detailed_solution(solution, marker='Detailed Solution', after=True):
    """
    Extracts the text after '### Detailed Solution ###' from the solution string.
    Returns the substring after the marker, stripped of leading/trailing whitespace.
    If the marker is not found, returns an empty string.
    """
    doc_start = solution.find("\\begin{document}")
    doc_end = solution.find("\\end{document}")
    if doc_start != -1 and doc_end != -1 and doc_end > doc_start:
        return solution[doc_start + len("\\begin{document}") : doc_end].strip()

    begin_marker = "<<BEGIN_DETAILED_SOLUTION>>"
    end_marker = "<<END_DETAILED_SOLUTION>>"
    begin_idx = solution.find(begin_marker)
    if begin_idx != -1:
        end_idx = solution.find(end_marker, begin_idx + len(begin_marker))
        if end_idx != -1:
            return solution[begin_idx + len(begin_marker) : end_idx].strip()
        return solution[begin_idx + len(begin_marker):].strip()

    idx = solution.find(marker)
    if idx == -1:
        return solution.strip()
    if(after):
        return solution[idx + len(marker):].strip()
    else:
        return solution[:idx].strip()

def verify_solution(problem_statement, solution, verbose=True):

    dsol = extract_detailed_solution(solution)

    newst = f"""
======================================================================
### Problem ###

{problem_statement}

======================================================================
### Solution ###

{dsol}

{verification_remider}
"""
    if(verbose):
        print(">>>>>>> Start verification.")
    p2 = build_request_payload(system_prompt=verification_system_prompt, 
        question_prompt=newst
        )
    
    if(verbose):
        print(">>>>>>> Verification prompt:")
        print(json.dumps(p2, indent=4))

    res = send_api_request(get_api_key(), p2)
    out = extract_text_from_response(res) 

    if(verbose):
        print(">>>>>>> Verification results:")
        print(json.dumps(out, indent=4))

    check_correctness = """Response in "yes" or "no". Is the following statement saying the solution is correct and complete(not a partial solution)? """ \
            + "\n\n" + out 
    prompt = build_request_payload(system_prompt="", question_prompt=check_correctness)
    r = send_api_request(get_api_key(), prompt)
    o = extract_text_from_response(r) 

    if(verbose):
        print(">>>>>>> Is verification good?")
        print(json.dumps(o, indent=4))
        
    bug_report = ""

    if("yes" not in o.lower()):
        bug_report = extract_detailed_solution(out, "Detailed Verification", False)

        """p2["contents"].append(
            {"role": "model",
            "parts": [{"text": bug_report}]
            }
        )
        p2["contents"].append(
            {"role": "user",
            "parts": [{"text": check_verification_prompt}]
            }
        )

        if(verbose):
            print(">>>>>>> Review bug report prompt:")
            print(json.dumps(p2["contents"][-2:], indent=4))

        res = send_api_request(get_api_key(), p2)
        out = extract_text_from_response(res) 
    """

    if(verbose):
        print(">>>>>>>Bug report:")
        print(json.dumps(bug_report, indent=4))
    
    return bug_report, o

def check_if_solution_claimed_complete(solution):
    check_complete_prompt = f"""
Is the following text claiming that the solution is complete?
==========================================================

{solution}

==========================================================

Response in exactly "yes" or "no". No other words.
    """

    p1 = build_request_payload(system_prompt="",    question_prompt=check_complete_prompt)
    r = send_api_request(get_api_key(), p1)
    o = extract_text_from_response(r)

    print(o)
    return "yes" in o.lower()


def init_explorations(problem_statement, verbose=True, other_prompts=[]):
    p1  = build_request_payload(
            system_prompt=step1_prompt,
            question_prompt=problem_statement,
            #other_prompts=["* Please explore all methods for solving the problem, including casework, induction, contradiction, and analytic geometry, if applicable."]
            #other_prompts = ["You may use analytic geometry to solve the problem."]
            other_prompts = other_prompts
        )

    print(f">>>>>> Initial prompt.")
    print(json.dumps(p1, indent=4))

    response1 = send_api_request(get_api_key(), p1)
    output1 = extract_text_from_response(response1)

    print(f">>>>>>> First solution: ") 
    print(json.dumps(output1, indent=4))

    print(f">>>>>>> Self improvement start:")
    p1["messages"].append(
        {"role": "assistant",
        "content": output1
        }
    )
    p1["messages"].append(
        {"role": "user",
        "content": self_improvement_prompt
        }
    )

    response2 = send_api_request(get_api_key(), p1)
    solution = extract_text_from_response(response2)
    print(f">>>>>>> Corrected solution: ")
    print(json.dumps(solution, indent=4))
    
    #print(f">>>>>>> Check if solution is complete:"  )
    #is_complete = check_if_solution_claimed_complete(output1)
    #if not is_complete:
    #    print(f">>>>>>> Solution is not complete. Failed.")
    #    return None, None, None, None
    
    print(f">>>>>>> Vefify the solution.")
    verify, good_verify = verify_solution(problem_statement, solution, verbose)

    print(f">>>>>>> Initial verification: ")
    print(json.dumps(verify, indent=4))
    print(f">>>>>>> verify results: {good_verify}")
    
    return p1, solution, verify, good_verify

def agent(problem_statement, other_prompts=[], memory_file=None, resume_from_memory=False):
    if resume_from_memory and memory_file:
        # Load memory and resume from previous state
        memory = load_memory(memory_file)
        if memory:
            problem_statement = memory.get("problem_statement", problem_statement)
            other_prompts = memory.get("other_prompts", other_prompts)
            current_iteration = memory.get("current_iteration", 0)
            solution = memory.get("solution", None)
            verify = memory.get("verify", None)
            print(f"Resuming from iteration {current_iteration}")
        else:
            print("Failed to load memory, starting fresh")
            current_iteration = 0
            solution = None
            verify = None
    else:
        # Start fresh
        current_iteration = 0
        solution = None
        verify = None
    
    if solution is None:
        p1, solution, verify, good_verify = init_explorations(problem_statement, True, other_prompts)
        if(solution is None):
            print(">>>>>>> Failed in finding a complete solution.")
            return None
    else:
        # We have a solution from memory, need to get good_verify
        _, good_verify = verify_solution(problem_statement, solution)

    error_count = 0
    correct_count = 1
    success = False
    for i in range(current_iteration, 30):
        print(f"Number of iterations: {i}, number of corrects: {correct_count}, number of errors: {error_count}")

        if("yes" not in good_verify.lower()):
            # clear
            correct_count = 0
            error_count += 1

            #self improvement
            print(">>>>>>> Verification does not pass, correcting ...")
            # establish a new prompt that contains the solution and the verification

            p1 = build_request_payload(
                system_prompt=step1_prompt,
                question_prompt=problem_statement,
                #other_prompts=["You may use analytic geometry to solve the problem."]
                other_prompts=other_prompts
            )

            p1["messages"].append(
                {"role": "assistant",
                "content": solution
                }
            )
            
            p1["messages"].append(
                {"role": "user",
                "content": f"{correction_prompt}\n\n{verify}"
                }
            )

            print(">>>>>>> New prompt:")
            print(json.dumps(p1, indent=4))
            response2 = send_api_request(get_api_key(), p1)
            solution = extract_text_from_response(response2)

            print(">>>>>>> Corrected solution:")
            print(json.dumps(solution, indent=4))


            #print(f">>>>>>> Check if solution is complete:"  )
            #is_complete = check_if_solution_claimed_complete(solution)
            #if not is_complete:
            #    print(f">>>>>>> Solution is not complete. Failed.")
            #    return None

        print(f">>>>>>> Verify the solution.")
        verify, good_verify = verify_solution(problem_statement, solution)

        if("yes" in good_verify.lower()):
            print(">>>>>>> Solution is good, verifying again ...")
            correct_count += 1
            error_count = 0
 

        # Save memory every iteration
        if memory_file:
            save_memory(memory_file, problem_statement, other_prompts, i, 30, solution, verify)
        
        if(correct_count >= 2):
            print(">>>>>>> Correct solution found.")
            print(json.dumps(solution, indent=4))
            return solution

        elif(error_count >= 5):
            print(">>>>>>> Failed in finding a correct solution.")
            # Save final state before returning
            if memory_file:
                save_memory(memory_file, problem_statement, other_prompts, i, 30, solution, verify)
            return None

    if(not success):
        print(">>>>>>> Failed in finding a correct solution.")
        # Save final state before returning
        if memory_file:
            save_memory(memory_file, problem_statement, other_prompts, 30, 30, solution, verify)
        return None
        
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='IMO Problem Solver Agent')
    parser.add_argument('problem_file', nargs='?', default='problem_statement.txt', 
                       help='Path to the problem statement file (default: problem_statement.txt)')
    parser.add_argument('--log', '-l', type=str, help='Path to log file (optional)')
    parser.add_argument('--other_prompts', '-o', type=str, help='Other prompts (optional)')
    parser.add_argument("--max_runs", '-m', type=int, default=10, help='Maximum number of runs (default: 10)')
    parser.add_argument('--memory', '-mem', type=str, help='Path to memory file for saving/loading state (optional)')
    parser.add_argument('--resume', '-r', action='store_true', help='Resume from memory file if provided')
    parser.add_argument('--config', '-c', type=str, help='Path to JSON config file to override defaults')
    
    args = parser.parse_args()

    if args.config:
        load_config(args.config)
        print(f"Config loaded from: {args.config}")

    max_runs = args.max_runs
    memory_file = args.memory
    resume_from_memory = args.resume
    
    other_prompts = []
    if args.other_prompts:
        other_prompts = args.other_prompts.split(',')

    print(">>>>>>> Other prompts:")
    print(other_prompts)
    
    if memory_file:
        print(f"Memory file: {memory_file}")
        if resume_from_memory:
            print("Resume mode: Will attempt to load from memory file")

    problem_statement = read_file_content(args.problem_file)

    for i in range(max_runs):
        # Reopen log file each run to fully overwrite
        if args.log:
            close_log_file()
            if not set_log_file(args.log):
                sys.exit(1)
            print(f"Logging to file: {args.log}")
        print(f"\n\n>>>>>>>>>>>>>>>>>>>>>>>>>> Run {i} of {max_runs} ...")
        try:
            sol = agent(problem_statement, other_prompts, memory_file, resume_from_memory)
            if(sol is not None):
                print(f">>>>>>> Found a correct solution in run {i}.")
                print(json.dumps(sol, indent=4))
                break
        except Exception as e:
            print(f">>>>>>> Error in run {i}: {e}")
            continue
    
    # Close log file if it was opened
    close_log_file()
