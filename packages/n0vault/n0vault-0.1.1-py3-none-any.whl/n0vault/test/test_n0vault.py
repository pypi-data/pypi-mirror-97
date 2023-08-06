import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

import n0vault

def test_1():
    my_vault = n0vault.n0Vault(os.path.splitext(os.path.split(__file__)[1])[0]+".vault")

    my_vault["group/subgroup/key1"] = "value1"
    my_vault.update("group/subgroup/key2", "value2")
    my_vault.update({"group/subgroup/key3": "value3"})

    print(my_vault["group/subgroup/key1"])
    print(my_vault.get("group/subgroup/key2"))
    print(my_vault.get("group/subgroup/key3", "Not exists"))
    print(my_vault.get("group/subgroup/key4", "Not exists"))

    print(my_vault.show())
    # my_vault.save()

def main():
    test_1()

if __name__ == '__main__':
    main()
