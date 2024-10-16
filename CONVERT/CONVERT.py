import re, os, colorama
from datetime import datetime


class EmailPasswordExtractor:
    def __init__(self): 
        self.total_entries = 0
        self.input_file = 'INPUT_FILE_PATH_HERE.txt' #       <<<<<<<<<<<<<<<<<<<<  HHHHHHHHHHHHHHEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRREEEEEEEEEE 
        self.output_file = 'sorted.txt' 

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def log(message):
        print(f"{colorama.Fore.LIGHTBLUE_EX}[ {EmailPasswordExtractor.get_time()} ] {colorama.Fore.LIGHTBLACK_EX} --->> {colorama.Fore.LIGHTMAGENTA_EX + colorama.Fore.LIGHTCYAN_EX}{message}{colorama.Fore.RESET}")

    def extract_emails_and_passwords(self):
        pattern = re.compile(
            r'^(?:https?://[^\s]+/(?:id/login|account)|(?:www\.)?[^\s]+):([^\s:]+):([^\s]+)|^(?:https?://[^\s]+/(?:id/login|account) )([^\s ]+)\s+([^\s]+)|([^\s]+):([^\s]+)'
        )

        if not os.path.exists(self.input_file):
            EmailPasswordExtractor.log(f"INVALID FILE >> '{self.input_file}'")
            return

        with open(self.input_file, 'r', encoding='utf-8') as infile, open(self.output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                match = pattern.search(line)
                if match:
                    email = password = None
                    if match.group(1):  
                        email, password = match.group(1), match.group(2)
                    elif match.group(3):
                        email, password = match.group(3), match.group(4)
                    elif match.group(5):  
                        email, password = match.group(5), match.group(6)
                    if email and password:
                        outfile.write(f"{email}:{password}\n")
                        EmailPasswordExtractor.log(f'{colorama.Fore.LIGHTBLUE_EX}[{colorama.Fore.LIGHTBLACK_EX}NEW{colorama.Fore.LIGHTBLUE_EX}] EMAIL {colorama.Fore.LIGHTBLACK_EX}>> {colorama.Fore.LIGHTGREEN_EX}{email}')
                        EmailPasswordExtractor.total_entries += 1
                    elif email: 
                        outfile.write(f"{email}:\n")  


    def clean_output_file(self):
        with open(self.output_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        cleaned_lines = [line for line in lines if re.match(r'^[^:]+:[^:]*$', line.strip())]
        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(cleaned_lines)


    def save_summary(self):
        EmailPasswordExtractor.log(f"FINISHED !! {EmailPasswordExtractor.total_entries} ")
        EmailPasswordExtractor.log(f"SAVED IN >> '{self.output_file}'.")

if __name__ == "__main__":
    colorama.init()
    email = EmailPasswordExtractor()
    email.log("LAUNCHING...")
    email.extract_emails_and_passwords()
    email.clean_output_file() 
    email.save_summary()
