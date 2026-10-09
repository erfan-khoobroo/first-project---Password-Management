from tabulate import tabulate
from pathlib import Path
import csv
import sys
import string
import secrets

class CsvFile:
    def __init__(self, name_file:str ,dir_file = Path.cwd()):
        self.name_file = name_file + f"{'' if name_file.endswith('.csv') else '.csv'}"
        self.dir_file = dir_verify(dir_file)
        self.path_file = Path(self.dir_file) / self.name_file

    def __str__(self):
        try:
            with open(self.path_file,"r", encoding="utf-8") as f:
                lines = f.readlines()
                reader = csv.reader(lines)
            if len(reader := list(reader)) <= 1:
                return "You haven't added an account yet⚠️"
            result = []
            for web_app , email, user_name , password in reader:
                result.append([web_app, email, user_name, password])
            return tabulate(result[1:], headers = result[0], tablefmt="grid")
        except (OSError, csv.Error):
            print("❌Error reading file")
            return ""

    @staticmethod
    def all_cat(dir_file = Path.cwd()):
        address = Path(dir_file)
        files = [x for x in address.glob('*.csv') if x.is_file()]
        return files

    def create_cat(self):
        try:
            with open(self.path_file,"x",newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["web/app", "email", "username", "password"])
            print(f"\n{self.name_file} ---- created ---->> " 
                f"{'by defulte(the program execution path)'if self.dir_file =='.' else self.dir_file}✅")
            return True
        except FileExistsError:
            print(f"❌ {self.name_file} already exists.")
            return False

    def add_data_to_cat(self):
        with open(self.path_file,"a",newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            web = input("website/app: ").strip()
            email = input("email: ").strip()
            username = input("username: ").strip()
            while 1 :
                if y_or_n(x := input("Do you want to use the password generator tool❓(y/n):")):
                    password = get_pass()
                    print(f"your password : '{password}'")
                    break
                elif x.lower() not in ["yes", "y" , "no", "n"]:
                    print(f"❌Invalid '{x}' input; please try again.\n")
                    continue
                else:
                    password = input("password: ").strip()
                    break
            writer.writerow([web, email, username, password])
            print(f"\nSuccessfully added to {self.name_file} ✅\n")
            return True
        
    @staticmethod
    def search(dir_file = Path.cwd()):
        files = CsvFile.all_cat(dir_file)
        if not files:
            print("❌ No CSV files found in this directory.")
            return False
        web = input("Website/App (press Enter to skip): ").strip()
        username = input("Username (press Enter to skip): ").strip()
        email = input("Email (press Enter to skip): ").strip()

        criteria = {
            0: web.casefold(),
            1: email.casefold(),
            2: username.casefold()}
        criteria = {column: value for column, value in criteria.items() if value}

        if not criteria:
            print("❌ Please enter at least one search criterion.")
            return False

        results = []
        for file in files:
            try:
                with open(file, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Skip header

                    for row in reader:
                        if len(row) != 4:
                            print(f"Value count error : {row}")
                            continue

                        if all(value in row[column].casefold() for column, value in criteria.items()):
                            results.append((file.name, row))

            except (OSError, csv.Error) as e:
                print(f"❌ Could not read {file.name}: {e}")

        if not results:
            print("No matching accounts found.")
            return False

        print(f"\nFound {len(results)} matching account(s):\n")
        
        res=[]
        for filename, row in results:
            web, email, username, password = row
            res.append([Path(filename).stem, web, email, username, password])
        print(tabulate(res, headers =["Category", "Web/App", "Email", "User Name", "Password"] , tablefmt="grid"))                
            
        return True

class PassGen:
    def __init__(self, difficulty_level = 2 , pass_length = 8):
        self._difficulty_level = difficulty_level
        self._pass_length = pass_length

        self.__L_letters = string.ascii_lowercase
        self.__U_letters = string.ascii_uppercase
        self.__Symbol = string.punctuation
        self.__num = string.digits


    def generate(self) -> str:
        match self._difficulty_level :
            case 1:
                characters = [self.__num , self.__L_letters]
            case 2:
                characters = [self.__num , self.__L_letters , self.__U_letters]
            case 3:
                characters = [self.__num , self.__L_letters , self.__U_letters , self.__Symbol]

        password = ""
        for _ in range(self._pass_length):
            group = secrets.choice(characters)
            password += secrets.choice(group)

        return password

welcome_msg = "\n*-*-*-*-*-*-*-*-*Welcome to Password Management *-*-*-*-*-*-*-*-*\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
home_options = [
"\n1.View or create account and password categories.",
"2.Add account-password",
"3.Password generation",
"4.Search this directory",
"5.Change directory",
"6.Exit\n"
]

def main():
    try:
        print(welcome_msg)  
        menu = "\n".join(home_options)
        select_dir = input("\nWhich directory's categories do you want to examine❓"
                        "\n(The default is the application's execution path): ").strip()
        select_dir = dir_verify(select_dir)
        print(f"Current directory: {select_dir} ✅")
        while 1:
                print(menu)
                option = select_home_options(home_options)
                match option:
                    case "1":
                        vc_cat(select_dir)
                    case "2":
                        add_ap(select_dir)
                    case "3":
                        password = get_pass()
                        print(f"your password : '{password}'")
                    case "4":
                        CsvFile.search(select_dir)
                    case "5":
                        print("\n***📁change directory***")
                        select_dir = input("(The default is the application's execution path): ").strip()
                        select_dir = dir_verify(select_dir)
                        print(f"Current directory: {select_dir} ✅")
                    case "6":
                        sys.exit("\nThank you for using the app👋")
                    case _:
                        print(f"❌Invalid '{option}' input")
    except KeyboardInterrupt:
        sys.exit("\nThank you for using the app👋\n")
    except EOFError:
        sys.exit("\nThank you for using the app👋\n")

def select_home_options(options):
    while 1:
        try:
            entry = int(x := input("What do you want to do❓\n 📋Please make a selection: ").strip())
            if 1 <= entry <= len(options):
                return x
            else :
                raise ValueError
        except ValueError:
            print(f"❌Invalid '{x}' input; please try again.")
            continue

def vc_cat(select_dir):
    files = CsvFile.all_cat(select_dir)
    for i, file in enumerate(files , 1):
        print(f"{i}. {file.name}")
    select_cat = input(f"{i+1 if files else "1"}. Creating a new category at this same path ...\n\n📋Select an option: ").strip()
    try:
        select_cat = int(select_cat)
        if 1 <= select_cat <= len(files) :
            name_file = files[select_cat-1].stem
            new_file = CsvFile(name_file, select_dir)
            print(new_file)
            answer = input("Do you want to add an account and password to this category❓(y/n):").strip()
            if y_or_n(answer):
                new_file.add_data_to_cat()
        elif select_cat == len(files) + 1 :
            new_file = CsvFile(input("📋Enter the name of your new category: ").strip(), select_dir)
            if new_file.create_cat():
                answer = input("Do you want to add an account and password to this category❓(y/n):").strip()
                if y_or_n(answer):
                    new_file.add_data_to_cat()
    except ValueError:
        print("❌Invalid input.")

def add_ap(select_dir):
    files = CsvFile.all_cat(select_dir)
    if len(files) == 0:
        print("\nYou haven't created any categories in this path yet☹️"
            "\n\nReturn to the main menu\nchoose another path, or create a new category.\n")
        return
    menu = "\nlist of category\n"
    for i, file in enumerate(files, 1):
        menu += f"{i}. {file.name}\n"
    while 1:
        print(menu)
        select_cat = input("\n📋Enter the number of the desired category: ").strip()
        try:
            select_cat = int(select_cat)
            if 1 <= select_cat <= len(files):
                name_file = files[select_cat-1].stem
                new_file = CsvFile(name_file, select_dir)
                new_file.add_data_to_cat()
                if y_or_n(input("Do you add other accounts❓(y/n):")):
                    while 1:
                        try:
                            n = int(input("How many accounts do you want to add❓"))
                            if n <= 0:
                                print("❌ Please enter a positive number.")
                                continue
                            for _ in range(n):
                                new_file.add_data_to_cat()
                            return
                        except ValueError:
                            print("❌Invalid input.")
                            if y_or_n(input("Do you want to return to the main menu❓(y/n):")):
                                return
                            continue
                else:
                    return
            else :
                print("❌Invalid input.")
                continue
        except ValueError:
            print("\n❌Invalid input.\n🔄️Try again.\n")
            continue

def get_pass():
    levels = ["easy", "normal", "hard"]
    while 1:
        info ="\nEasy : num + lowercase latters\nNormal : num + lowercase latters + uppercase latters\nHard : num + lowercase latters + uppercase latters + symbols\n"
        print(info)
        level = input("What level should your password be❓\n(Easy/Normal/Hard):").strip().lower()
        if level in levels:
            while 1 :
                try:
                    length = int(x := input("How many characters should your password have?❓").strip().lower())
                    if length > 0:
                        break
                    else:
                        print(f"❌Invalid '{x}' input; please try again.")
                        continue
                except ValueError :
                    print(f"❌Invalid '{x}' input; please try again.")
                    continue
            if level == "easy":
                level = 1
            elif level == "normal":
                level = 2
            elif level == "hard":
                level = 3
            return PassGen(level, length).generate()
        else:
            print("\n❌Invalid input.\n🔄️Try again.\n")
            continue

def dir_verify(select_dir, n_try=5):
    for _ in range(n_try):
        if not select_dir:
            return Path.cwd()
        elif Path(select_dir).is_dir():
            return Path(select_dir)
        else :
            select_dir = input("❌The entered path is incorrect.\n🔄️Try again: ")
            continue
    else:
        print("\nDue to the high number of errors, the default program execution path was selected✅")
        return Path.cwd()

def y_or_n(answer):
    if answer.strip().lower() in ["y", "yes"]:
        return True
    else:
        return False

if __name__ == "__main__":
    main()