import yara_validator
import plyara
import yara
from collections import Counter
import pytablewriter
from pytablewriter.style import Style
import os
import html


def parseRule(pathRule):
    global yaraRule, rules
    validator = yara_validator.YaraValidator(auto_clear=False)
    validator.add_rule_file(pathRule)
    valid, broken, repaired = validator.check_all()
    validator.clear_tmp()
    if valid:
        parser = plyara.Plyara()
        rules = parser.parse_string(valid[0].source)
        patched = ""
        for rule in rules:
            patched += "rule " + rule["rule_name"] + " {\n"
            patched += rule["raw_strings"]
            patched += "condition:\nany of them\n}\n"
            useless = [
                "raw_meta",
                "raw_strings",
                "raw_condition",
                "start_line",
                "stop_line",
                "metadata",
                "condition_terms",
                "comments",
            ]
            for u in useless:
                if u in rule:
                    del rule[u]
            for string in rule["strings"]:
                string["files"] = []
        yaraRule = yara.compile(source=patched)
        return len(rules)
    else:
        return "invalid"


def scanYARA(files):
    global rules
    for file in files:
        with open(file, "rb") as f:
            matches = yaraRule.match(data=f.read())
        for m in matches:
            for rule in rules:
                if rule["rule_name"] == m.rule:
                    for s in rule["strings"]:
                        for item in m.strings:
                            if s["name"] == item[1] and rule["rule_name"] == str(m):
                                s["files"].append(file)


def tableHTML(files):
    table = ""
    writer = pytablewriter.HtmlTableWriter()
    filenames = []
    for file in files:
        fn = os.path.basename(file)
        if len(fn) <= 18:
            filenames.append(f"<div><span>{fn}</span></div>")
        else:
            filenames.append(f"<div><span title='{fn}'>{fn[:18]}...</span></div>")
    writer.headers = ["", ""] + filenames
    writer.column_styles = [Style(align="center", vertical_align="middle")] * (
        len(files) + 2
    )
    writer.column_styles[1] = Style(align="left", vertical_align="middle")
    for rule in rules:
        writer.table_name = rule["rule_name"]
        writer.value_matrix = []
        for string in rule["strings"]:
            cntr = Counter(string["files"])
            lst = list()
            lst.append(string["name"])
            mod = " <i>" + "  ".join(string.get("modifiers", "")) + "</i>"
            lst.append(html.escape(string["value"]) + mod)
            for file in files:
                lst.append(str(cntr.get(file, "")))
            writer.value_matrix.append(lst)
        table += writer.dumps()
    return table
