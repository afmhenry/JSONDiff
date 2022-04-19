from audioop import tostereo
import json
from pprint import PrettyPrinter
from black import out
from deepdiff import DeepDiff


def FileToDict(name):
    with open(name) as f:
        data = json.load(f)
    return data  # .get("Data")[0]


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
    file2 = FileToDict("data/live-closed-positions-cs.json")
    file1 = FileToDict("data/live-closed-positions-hist.json")
    ddiff = DeepDiff(file1, file2, ignore_order=True)
    print(dict(ddiff).keys())

    for key in dict(ddiff).keys():
        print(key)
        diff_items = dict(ddiff)[key]
        output = ""
        for entry in diff_items:
            pretty_diff = ""
            if key == "values_changed":
                pretty_diff = (
                    "("
                    + str(diff_items[entry]["old_value"])
                    + " => "
                    + str(diff_items[entry]["new_value"])
                    + ")"
                )
            output += PathPretty(entry) + pretty_diff + "\n"

        ToTxt(output, key)
