import argparse
from n0vault import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "n0vault")
    parser.add_argument("-v", "--vault",    nargs=1,        
        default=(
            VAULT_FILE:=
                (
                    VAULT_FILE_NAME
                    if (VAULT_FILE_NAME:=os.path.splitext(os.path.split(__file__)[1])[0]) != "__init__" 
                    else "n0vault"
                )  + ".vault"
        ),
                                                            metavar="VAULT_FILE",    action='store',       help=f"use VAULT_FILE as storage. By default: '{VAULT_FILE}'")
    parser.add_argument("-e", "--encrypt",  dest="encrypt", default=None,            action='store_true',  help="save into ENCRYPTED vault file")
    parser.add_argument("-p", "--password", nargs=1,                                                       help="use PASSWORD")
    parser.add_argument("-d", "--decrypt",  dest="encrypt",                          action='store_false', help="save into DECRYPTED vault file")
    parser.add_argument("-u", "--update",   nargs=2,        metavar=("KEY","VALUE"), action='append',      help="add/update VALUE for the KEY")
    parser.add_argument("-r", "--remove",   nargs=1,        metavar="KEY",           action='extend',      help="remove KEY with value")
    parser.add_argument("-s", "--show",     nargs=1,        metavar="XPATH",         action='extend',      help="show value for the KEY")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    
    args = parser.parse_args(sys.argv[1:])

    my_vault = n0Vault(vault_file_name = args.vault[0] if args.vault else None,
                       password = args.password[0] if args.password else None,
                       encrypted = args.encrypt
    )

    for pair in args.update or []:
        my_vault.update(pair[0],pair[1])

    for key in args.remove or []:
        my_vault.delete(key)

    if args.show:
        if args.show[0][0] == "*":
            print(my_vault.show())
        else:
            for start_xpath in args.show or []:
                start_xpath = start_xpath[0]
                for key in my_vault._vault.get(start_xpath, []):
                    print("%s=%s" % (key, my_vault[key]))

    if not args.encrypt is None:
        print(f"Saving '{my_vault.vault_file_name}' as %s..." % ["DECRYPTED", "ENCRYPTED"][int(my_vault._encrypted)])
        my_vault.save()
