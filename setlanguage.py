import subprocess

def CMDIFY(spec):
    cmd = ["setxkbmap", "-option"]
    cmd += ["-model", spec.get("model", "")]
    cmd += ["-layout", spec.get("layout", "")]
    cmd += ["-variant", spec.get("variant", "")]

    if "options" in spec and spec["options"]:
        for option in spec["options"].split(" "):
            cmd += ["-option", option]

    return cmd

spec = {
    "model": "pc104",
    "layout": "us",
    "variant": "intl",
    #"options": "",
 
}
result = subprocess.run(CMDIFY(spec), capture_output=True, check=True)
