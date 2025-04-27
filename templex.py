import  requests ,re  ,os
from time import sleep
from  bs4 import BeautifulSoup
from termcolor import colored
from pyfiglet import Figlet

# Processing ----------------------------------->
def make_project_dir(dir_name):
    folder = dir_name if dir_name != '' else 'Project'
    if not os.path.exists(f"{folder}"):
        os.system(f'mkdir {folder}')
    else:
        os.system(f"rmdir  /s /q {folder}")
        os.system(f'mkdir {folder}')

def url_filter(url):

    if (re.findall("(https://.*)(/.*)",url)) != []:
        URL = (re.findall("(https://.*)(/.*)",url))
        return  URL[0][0]
    else:
        URL = (re.findall("(https://.*)",url))
        return URL[0]

def remove_all_links(list_of_items):
    pattern1,pattern2 = r"(https?://)",r"(.*)(www[^\s]+)"
    new_list = []
    for item in list_of_items:
        if not re.match(pattern1, item) and not re.match(pattern2, item):
                new_list.append(item)
    return new_list

def filter_path(Input):
    Input = Input.replace('/../', '')
    Input = Input.replace('../', '')
    Input = Input.replace('//', '')
    res = Input.replace('//', '')
    d = re.sub('(\\?.*)','',str(res),)
    return d

def exporter(url,dir_name):
    response = requests.get(url)
    HTMl = response.content
    HTMl = HTMl.replace(bytes('../','utf-8'),bytes('','utf-8'))
    folder = dir_name if dir_name != '' else 'Project'
    with open(f'{folder}/index.html', 'wb') as f:
        f.write(HTMl)
        f.close()

    soup = BeautifulSoup(response.content, 'html.parser')
    head = soup.head
    # For style resources
    link_tag = remove_all_links(list((re.findall(r'href="([^"]+)', str(head)))))

    # For scripts and images
    src_tag = remove_all_links(list((re.findall(r'src="([^"]+)', str(soup)))))
    link_tag.extend(src_tag)

    return link_tag

def dir_creator(url,links,dir_name):

    def file_creator(link,content):
            folder = dir_name if dir_name != '' else 'Project'
            with open(f"{folder}/{(link)}", 'wb') as file:
                file.write(content)
                file.close()


    def downloader(url,link):

        contents = requests.get(f"{url_filter(url)}/{link}")
        return contents.content


    for link in links:

        paths = link.split('/')[:-1]
        contents = downloader(url,link)
        mainPath = ''

        for dir in paths:
            mainPath = f"{mainPath}/{dir}"
        mainPath = mainPath[1:]
        folder = dir_name if dir_name != '' else 'Project'
        if os.path.exists(f"{folder}/{mainPath}"):

            try:
                file_creator(link, contents)
            except FileNotFoundError:
                continue

        else:

            os.makedirs(f"{folder}/{mainPath}", exist_ok=True)
            try:
                file_creator(link,contents)
            except FileNotFoundError :
                continue

def execute(url,dir_name):

    make_project_dir(dir_name)
    # print('Creating Main : Completed')

    linksList =[filter_path(link) for link in exporter(url,dir_name)]
    # print('Exporting Data : Completed')

    dir_creator(url,linksList,dir_name)
    os.system('msg * "Exporting is Completed"')


# Terminal ----------------------------------->

def terminal_input():

    Url = input(colored("[!] Enter The Target Address : ", 'light_blue'))
    dir_name = input(colored("[!] Output Folder's Name : ", 'light_blue'))
    # Direction = input('Change Direction To RTL [default = No]? (yes),(Y) | (no),(N): ')
    return Url,dir_name

def input_checker(url ):

    URL = colored(f"[+] Target Address : {url}", 'green')
    # Direction = colored(f"[+] The Direction : {direction}", 'green')
    return URL


def run_templex():

    F = Figlet(font='Big_Money-nw')
    print('\n')
    Logo = F.renderText('TEMPLEX')
    print(colored(Logo, color='magenta'))

    url,dir_name = terminal_input()


    print(colored("\n---------------------------------------------------- \n", 'yellow'))
    input_checker(url)

    for i in range(1, 4):
        print(colored(f"\rExporting start after {3 - i} second",'yellow'), end="")
        sleep(1)

    execute(url,dir_name)


if __name__ == '__main__':
    run_templex()

