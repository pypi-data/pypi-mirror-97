# n0vault
Vault for secure storage of passwords and other sensitive data

## Usage from command line:
    python -m n0vault [-h] [-v VAULT_FILE] [-e] [-p PASSWORD] [-d] [-u KEY VALUE] [-r KEY] [-s XPATH]

    optional arguments:
      -h, --help            show this help message and exit
      -v VAULT_FILE, --vault VAULT_FILE
                            use VAULT_FILE as storage. By default: 'n0vault.vault'
      -e, --encrypt         save into ENCRYPTED vault file
      -p PASSWORD, --password PASSWORD
                            use password
      -d, --decrypt         save into DECRYPTED vault file
      -u KEY VALUE, --update KEY VALUE
                            add/update value for the key
      -r KEY, --remove KEY  remove KEY with value
      -s XPATH, --show XPATH
                            show value for the KEY

## Usage from python code:
    import os
    import n0vault

    my_vault = n0vault.n0Vault(os.path.splitext(os.path.split(__file__)[1])[0]+".vault")

    my_vault["group/subgroup/key1"] = "value1"
    my_vault.update("group/subgroup/key2", "value2")
    my_vault.update({"group/subgroup/key3": "value3"})

    print(my_vault["group/subgroup/key1"])
    print(my_vault.get("group/subgroup/key2"))
    print(my_vault.get("group/subgroup/key3", "Not exists"))
    print(my_vault.get("group/subgroup/key4", "Not exists"))

    print(my_vault.show())

    my_vault.save()

>>value1
>>value2
>>value3
>>Not exists
>>{
>>    "__sign": "n0Vault1",
>>    "group": {
>>        "subgroup": {
>>            "key1": "value1",
>>            "key2": "value2",
>>            "key3": "value3"
>>        }
>>    }
>>}
