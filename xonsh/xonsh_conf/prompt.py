from typing import Any, Dict, cast
import yaml
from .xonsh_builtin import x_env, x_exitcode
from .lib import HOSTNAME, HOME
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
        prompt += "{WHITE}"
    prompt += "{user}{WHITE}@"

    if HOSTNAME in ["mini", "patty"]:
        prompt += "{GREEN}"
    elif HOSTNAME in [
        "violet",
        "violet-gopher",
        "miriam",
        "penguin",
        "arcueid",
        "ciel",
    ]:
        prompt += "{CYAN}"
    elif HOSTNAME in ["lewill", "sirius"]:
        prompt += "{BLUE}"
    elif (
        HOSTNAME.count("mbp")
        or HOSTNAME.count("charlotte")
        or HOSTNAME.count("mac")
        or HOSTNAME.startswith("O-")
        or HOSTNAME.startswith("kukrushka")
    ):
        prompt += "{WHITE}"
    elif HOSTNAME.count("prod") > 0:
        prompt += "{RED}"
    elif HOSTNAME.count("bastion") > 0:
        prompt += "{PURPLE}"
    else:
        prompt += "{RED}"
    prompt += "{hostname}"
    prompt += "{RESET}"
    prompt += " "
    prompt += "{cwd} "
    prompt += "{git} "
    prompt += "{BLUE}{kubernetes}{WHITE} "
    prompt += "\n"
    prompt += "{prompt_end}"

    x_env["PROMPT"] = prompt
    prompt_fields = cast(Dict[str, Any], x_env["PROMPT_FIELDS"])
    prompt_fields["exit"] = lambda: "" if x_exitcode() == 0 else str(x_exitcode()) + " "
    from .gitstatus import gitstatus_prompt

    prompt_fields["git"] = gitstatus_prompt
    prompt_fields["kubernetes"] = current_kubernetes_context
