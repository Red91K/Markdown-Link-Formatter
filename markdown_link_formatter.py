import requests
import re
import subprocess

def return_formatted_url(url: str):
   print(f"\nFORMATTING URL [{url}]")
   # making requests instance
   reqs = requests.get(url)

   # search for title elements
   # IGNORECASE flag is needed to catch miscapitalisations of title elements
   titlear = re.findall('<title>(.*?)</title>', reqs.text, flags=re.IGNORECASE)

   formatted = ""

   if len(titlear) > 1:
      print()
      print("There seems to be multiple titles for this resource.")
      for i in range(len(titlear)):
         print(f'[{i}] - {titlear[i]}')

      correct_title_pos = int(input("Please select one by typing in the number next to the title:\n"))
      formatted = f'[{titlear[correct_title_pos].get_text()}]({url})'

   elif len(titlear) < 1:
      print()
      print("There seems to be no titles for this resource")
      correct_title = input("Please type the title for this resource:\n")
      formatted = f'[{correct_title}]({url})'
   
   else: # only one title
      formatted = f'[{titlear[0]}]({url})'

   # determine if the link points to an image w/ content-type header
   if "image" in reqs.headers['Content-Type']:
      formatted = "!" + formatted
   print(f"Formatting Succesful! Result: {formatted}\n")
   return formatted
 
if __name__ == '__main__':
   print("<-----\tMarkdown-Link-Formatter\t----->")

   url = input("Paste your URL here, if multiple URLs, type [multiple]:\ntype [help] for instructions\n")

   if url.lower() == "help" or url.lower() == "[help]":
      print("\n\n<-----\tHelp\t----->")
      print("The Markdown Link Formatter turns links to websites and images into a markdown-compatible format.")
      print("Enter the link, and the script will automatically grab the title of the website and detect if it is an image.")
      print("The script automatically copies the output to your clipboard.")
      print("If the script detects more than one title or none at all, it will prompt the user to choose / enter a title")
      print("<-----\tMarkdown-Link-Formatter\t----->\n\n")

   elif url.lower() == "multiple" or url.lower() == "[multiple]":
      urlar = []
      print("Paste multiple urls, separated by a newline character, Ctrl+D or enter a blank line to save:")
      
      while True:
         try:
            line = input()
         except EOFError:
            break
         if not line.replace(" ",""):
            break
         urlar.append(line)

      print()
      formatted_str = ""
      for url in urlar:
         formatted = return_formatted_url(url)
         formatted_str += formatted + "\n"

      subprocess.run("pbcopy", text=True, input=formatted_str)
      print("Copied to Clipboard!")

   
   else:
      formatted = return_formatted_url(url)
      print()

      subprocess.run("pbcopy", text=True, input=formatted)
      print("Copied to Clipboard!")
