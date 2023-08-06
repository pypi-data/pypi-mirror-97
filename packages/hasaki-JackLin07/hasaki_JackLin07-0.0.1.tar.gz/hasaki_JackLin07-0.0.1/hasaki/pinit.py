import argparse



template = """
{
    "global_cflag": {
        "ccfront": ["add global cflag in front"],
        "ccrear": ["add global clfag in rear"]
    },
    "global_link_flag": {
        "ldfront": ["add link flag in front"],
        "ldrear": ["add link flag in rear"]
    },
    "action": [{
        "name": "action name",
        "type": "exe",
        "cc": "gcc",
        "ar": "ar",
        "ld": "ld",
        "src_file_filter_suffix": [
            ".c", ".C", ".s", ".S"
        ],
        "src_path": [
            "./add"
        ],
        "src_args": [
            "add src sub-cflag in there"
        ],
        "inc_path": [
            "input inc path"
        ],
        "obj_file_suffix": ".o",
        "output_dir": "build",
        "use_ld_flag": "False"
    }],
    "prebuild_action": [
        ""
    ],
    "postbuild_action": [
        ""
    ]
}
"""


def add_arguments(parser: argparse.ArgumentParser) -> None:
    pass

def run(options: argparse.Namespace) -> int:
    with open("config.json","w") as f:
        f.write(template)
    print("please input your project info in config.json.and use projbuild gen to generate build.ninja.enjoy it.")
    return 0