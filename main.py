from scanner import Scanner
if __name__=="__main__":
    scanner = Scanner()
    token = scanner.get_next_token()
    while token:
        with open('tokens.txt', 'a') as file:
            file.write('\n' + token)
        token = scanner.get_next_token()