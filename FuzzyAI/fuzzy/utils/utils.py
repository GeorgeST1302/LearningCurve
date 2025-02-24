import json
import logging
from datetime import datetime
from typing import Any, Optional, Type, Union

import plotly.express as px
import plotly.graph_objects as go
from tabulate import tabulate

from fuzzy.llm.providers.base import BaseLLMProvider, llm_provider_fm
from fuzzy.llm.providers.enums import LLMProvider
from fuzzy.models.fuzzer_result import FuzzerResult

logger = logging.getLogger(__name__)

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
REPORT_TEMPLATE = """<!DOCTYPE html><html lang="en" data-bs-theme="dark"><head><title>Fuzzer Report</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"></head><body>{content}<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script></body></html>"""

def llm_provider_model_sanity(provider: str, model: str) -> None:
    """
    Check if the model is supported by the provider.

    Args:
        provider (str): The flavor of the provider.
        model (str): The model to check.

    Raises:
        ValueError: If the model is not supported by the provider.
    """
    provider_class: Type[BaseLLMProvider] = llm_provider_fm[provider]
    supported_models: Union[str, list[str]] = provider_class.get_supported_models()
    if supported_models and isinstance(supported_models, list) and model not in supported_models:
        raise ValueError(f"Model {model} not supported by provider {provider}, supported models: {supported_models}")  
    
def llm_provider_factory(provider: LLMProvider, model: str, **extra: Any) -> BaseLLMProvider:
    """
    Factory method to create an instance of the language model provider.

    Args:
        provider_name (LLMProvider): The name of the language model provider.
        model (str): The model to use.
        **extra (Any): Additional arguments for the language model provider.

    Returns:
        BaseLLMProvider: An instance of the language model provider.
    """
    llm_provider_model_sanity(provider, model)
    return llm_provider_fm[provider](provider=provider, model=model, **extra)

def extract_json(s: str) -> Optional[dict[str, Any]]:
    """
    Given a string potentially containing JSON data, extracts and returns
    the values for `improvement` and `adversarial prompt` as a dictionary.

    Args:
        s (str): The string containing the potential JSON structure.

    Returns:
        dict: A dictionary containing the extracted values.
    """
    # Find the JSON substring
    start_pos = s.find("{")
    end_pos = s.find("}", start_pos) + 1  # Include the closing brace
    if end_pos == -1:
        logger.error("Error extracting potential JSON structure")
        logger.error(f"Input:\n {s}")
        return None

    json_str = s[start_pos:end_pos].replace("\n", "").replace("\r", "")

    try:
        parsed: dict[str, Any] = json.loads(json_str)
        if not all(key in parsed for key in ["improvement", "prompt"]):
            logger.error("Error in extracted structure. Missing keys.")
            logger.error(f"Extracted:\n {json_str}")
            return None
        return parsed
    except json.JSONDecodeError:
        logger.error("Error parsing extracted structure")
        logger.error(f"Extracted:\n {json_str}")
        return None

def print_report(report: FuzzerResult) -> None:
    headers = ["prompt", "model", "attack method", "adversarial prompt", "response", "jailbreak?"]
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    table_data = []
    green = f"{GREEN}✔{RESET}"
    red = f"{RED}\u2716{RESET}"

    for entry in report.attacking_techniques or []:
        for model_entry in entry.models:
            for failed_prompts in model_entry.failed_prompts:
                table_data.append([failed_prompts.original_prompt, model_entry.name, entry.attack_mode, failed_prompts.harmful_prompt or "-", failed_prompts.harmful_response, red])
            for successful_prompts in model_entry.harmful_prompts:
                table_data.append([successful_prompts.original_prompt, model_entry.name, entry.attack_mode, successful_prompts.harmful_prompt, successful_prompts.harmful_response, green])
            
    try:
        print(tabulate(table_data, headers, tablefmt="simple_grid", maxcolwidths=[40, 20, 20, 40, 50, 10], colalign=("center", "center", "center", "center", "center", "center")))
    except Exception as e:
        logger.error("Can't generating report")

def generate_report(report: FuzzerResult) -> None:
    try:
        template = "plotly_dark"
        model_total_prompts: dict[str, int] = {}
        model_success: dict[str, int] = {}
        heatmap_matrix: dict[str, dict[str, float]] = {}

        # Calculate model success rate
        for entry in report.attacking_techniques or []:
            for model_entry in entry.models:
                model_total_prompts[model_entry.name] = model_total_prompts.get(model_entry.name, 0) + len(model_entry.harmful_prompts) + len(model_entry.failed_prompts)
                model_success[model_entry.name] = model_success.get(model_entry.name, 0) + len(model_entry.harmful_prompts)

                # Calculate the success rate per attack mode per model
                if model_total_prompts.get(model_entry.name, 0) > 0:
                    heatmap_matrix[model_entry.name] = heatmap_matrix.get(model_entry.name, {})
                    heatmap_matrix[model_entry.name][entry.attack_mode] = model_success[model_entry.name] / model_total_prompts[model_entry.name]

        data = [[heatmap_matrix[model][attack.attack_mode] for model in heatmap_matrix.keys()] for attack in report.attacking_techniques] # type: ignore

        heatmap = px.imshow(data,
                    labels=dict(x="MODEL NAME", y="ATTACK MODE", color="ASR"),
                    x=list(heatmap_matrix.keys()),
                    y=[attack.attack_mode for attack in report.attacking_techniques], # type: ignore
                )
            
        # Plot a bar graph with plotly.express
        model_success_rate = {model: (success / total if total > 0 else 1) * 100 for model, success in model_success.items() for model2, total in model_total_prompts.items() if model == model2}
        model_success_graph = px.bar(x=list(model_success_rate.keys()), y=list(model_success_rate.values()), labels=["SUCCESS RATE", "MODEL NAME"], title="MODEL ASR")
        
        # Calculate success rate by attack mode
        attack_total: dict[str, int] = {}
        attack_success: dict[str, int] = {}

        for entry in report.attacking_techniques or []:
            attack_total[entry.attack_mode] = 0
            attack_success[entry.attack_mode] = 0
            for model_entry in entry.models:
                attack_total[entry.attack_mode] += len(model_entry.harmful_prompts) + len(model_entry.failed_prompts)
                attack_success[entry.attack_mode] += len(model_entry.harmful_prompts)

        # Plot a bar graph with plotly.express
        attack_success_rate = {attack: (success / total if total > 0 else 1) * 100 for attack, success in attack_success.items() for attack2, total in attack_total.items() if attack == attack2}
        attack_success_graph = px.bar(x=list(attack_success_rate.keys()), y=list(attack_success_rate.values()), labels=["SUCCESS RATE", "ATTACK MODE"], title="ASR by attack mode")

        # Curate a table of harmful_prompts with plotly
        harmful_prompts = []
        for entry in report.attacking_techniques or []:
            for model_entry in entry.models:
                for prompt in model_entry.harmful_prompts:
                    harmful_prompts.append((prompt.original_prompt, prompt.harmful_prompt))

        success_table = go.Figure(data=[go.Table(header=dict(values=['ORIGINAL PROMPTS', 'ADVERSARIAL PROMPTS'],), name="JAILBROKEN PROMPTS",
                        cells=dict(values=[[x[0] for x in harmful_prompts], [x[1] for x in harmful_prompts]]))
                            ])

        failed_prompts = []
        for entry in report.attacking_techniques or []:
            for model_entry in entry.models:
                for prompt in model_entry.failed_prompts:
                    failed_prompts.append((prompt.original_prompt, prompt.harmful_prompt or "-"))

        fail_table = go.Figure(data=[go.Table(header=dict(values=['ORIGINAL', 'ADVERSARIAL PROMPT'],), name="FAILED PROMPTS",
                    cells=dict(values=[[x[0] for x in failed_prompts], [x[1] for x in failed_prompts]]))
                        ])
        
        for fig in [model_success_graph, attack_success_graph, success_table, fail_table, heatmap]:
            fig.update_layout(template=template)
        
        content = str()
        content += "<h1>JAILBROKEN PROMPTS</h1>"
        content += success_table.to_html(full_html=False, include_plotlyjs='cdn')
        content += heatmap.to_html(full_html=False, include_plotlyjs=False)
        content += model_success_graph.to_html(full_html=False, include_plotlyjs=False)
        content += attack_success_graph.to_html(full_html=False, include_plotlyjs=False)
        content += "<h1>FAILED PROMPTS</h1>"
        content += fail_table.to_html(full_html=False, include_plotlyjs=False)

        html_data = REPORT_TEMPLATE.format(content=content)
        with open(f'results/{CURRENT_TIMESTAMP}/report.html', 'w') as f:
            f.write(html_data)
    except Exception as ex:
        logger.error("Error generating report")
        return
    
    logger.info(f"Report generated at results/{CURRENT_TIMESTAMP}/report.html")
