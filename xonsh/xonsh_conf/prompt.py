from typing import Tuple
import yaml
from .xonsh_builtin import x_env, x_aliases, x_events, x_exitcode
from .lib import HOSTNAME, HOME, run, silent_run
import os

kubeconf_ctime = 0.0
kubeclient_current_context = ""

def current_kubernetes_context() -> str:
    global kubeconf_ctime
    global kubeclient_current_context

    config_path = os.path.join(HOME, ".kube", "config")
    if not os.path.exists(config_path):
        return ""

    current_kubeconf_ctime = os.stat(config_path).st_ctime
    if current_kubeconf_ctime == kubeconf_ctime:
        return kubeclient_current_context
    kubeconf_ctime = current_kubeconf_ctime

    with open(config_path) as f:
        if hasattr(yaml, "CLoader"):
            kubeconf = yaml.load(f.read().strip(), Loader=yaml.CLoader)
        else:
            kubeconf = yaml.load(f.read().strip(), Loader=yaml.Loader)
    context_name = kubeconf.get("current-context", "")

    namespace_display_name = ""

    if context_name.startswith("gke"):
        context_display_name = context_name.split("_")[-1]
    else:
        context_display_name = context_name

    for context in kubeconf["contexts"]:
        if context["name"] == context_name:
            namespace_display_name = context["context"].get("namespace", "default")
            break
    kubeclient_current_context = f"{context_display_name}:{namespace_display_name}"

    return kubeclient_current_context


def set_prompt():

    prompt = "{RED}{exit}{WHITE}"

    # user
    if x_env.get("USER", "nnyn") == "root":
        prompt += "{RED}"
    else:
        prompt += "{GREEN}"
    prompt += "{user}{WHITE}@"

    if HOSTNAME in ["nagisa", "methyl", "mini", "patty"]:
        prompt += "{PURPLE}"
    elif HOSTNAME in ["violet"]:
        prompt += "{CYAN}"
    elif HOSTNAME in ["mbp"]:
        prompt += "{YELLOW}"
    else:
        prompt += "{WHITE}"
    prompt += "{hostname}"
    prompt += "{NO_COLOR}"
    prompt += " "
    prompt += "{cwd} "
    prompt += "{git} "
    prompt += "{BLUE}{kubernetes}{WHITE} "
    prompt += "\n"
    prompt += "{prompt_end}"

    x_env["PROMPT"] = prompt
    x_env["PROMPT_FIELDS"]["exit"] = lambda: "" if x_exitcode() == 0 else str(x_exitcode()) + " "
    from .gitstatus import gitstatus_prompt
    x_env["PROMPT_FIELDS"]["git"] = gitstatus_prompt
    x_env["PROMPT_FIELDS"]["kubernetes"] = current_kubernetes_context
