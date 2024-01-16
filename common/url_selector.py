import inquirer
import sys


def select_url(img_list):
    try:
        questions = [
            inquirer.Checkbox("url",
                              message="Select which url to download from:",
                              choices=img_list, default=img_list,
                              )
        ]

        answer = inquirer.prompt(questions)
        print("Selected URLs to download: %s" % len(answer["url"]))

        return answer["url"]
    except (TypeError):
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)
