import inquirer

def select_url(img_list):

    questions = [
        inquirer.Checkbox("url",
                          message="Select which url to download from:",
                          choices=img_list, default=img_list,
        )
    ]

    answer = inquirer.prompt(questions)
    
    print("Selected URLs to download: %s" % len(answer["url"]))

    return answer["url"]