from audioop import tostereo
import json
from pprint import PrettyPrinter
from black import out
from deepdiff import DeepDiff


def FileToDict(name):
    with open(name) as f:
        data = json.load(f)
    return data.get("Data")[0]


def ToTxt(changes, name):
    with open("data/" + name + ".txt", "w") as f:
        f.write(changes)


def PathPretty(entry):
    return (
        entry.replace("']['", ".")
        .replace("root[", "Root.")
        .replace("]", "")
        .replace("'", "")
    )


if __name__ == "__main__":
    file1 = FileToDict("data/SIM-EXT-DATA.json")
    file2 = FileToDict("data/LIVE-EXT-DATA.json")
    ddiff = DeepDiff(file1, file2, ignore_order=True)

    print("Fields added")
    diff_items = dict(ddiff)["dictionary_item_added"]
    output = ""
    for entry in diff_items:
        output += PathPretty(entry) + "\n"
    ToTxt(output, "attr_missing")
    output = ""
    print("Values changed")
    diff_items = dict(ddiff)["values_changed"]
    for entry in diff_items:
        # todo: logic to determine if change is actually an issue
        pretty_diff = (
            "("
            + str(diff_items[entry]["old_value"])
            + " => "
            + str(diff_items[entry]["new_value"])
            + ")"
        )
        output += PathPretty(entry) + pretty_diff + "\n"
    ToTxt(output, "value_changed")
