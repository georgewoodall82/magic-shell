import requests
import json
import os

from requests import api



print("Welcome to Magic Shell by georgewoodall82")
print("\n")
print("Note: you can type <shell> then a command to run a shell command without magic shell")
print("\n")



if os.path.exists("config.json"):
    with open("config.json") as configfile:
        configjson = json.load(configfile)

        apikey = configjson['apikey']
        model = configjson['model']
else:

    print("Config file not found, please fill in these details:")
    print("\n")

    print("This is the api key you get from https://studio.ai21.com/account")
    apikey = input("AI21 Studio API Key:")
    print("\n")


    print("The this is the model you want to use (use 'j1-jumbo' if you dont know what this is)")
    model = input("Model Name:")
    print("\n")



    config = {
        "apikey": apikey,
        "model": model
    }

    with open("config.json", "w") as configfile:
        configfile.write(json.dumps(config))






while True:
    command = input("<Magic Shell>")

    if command.startswith("<shell>"):
        print(os.popen(command.removeprefix("<shell>")).read())
        continue


    with open("AI21.txt") as prompt1:
        prompt2 = prompt1.read()


    prompt = prompt2 + command



    response1 = requests.post(
    "https://api.ai21.com/studio/v1/" + model + "/complete",
    headers={"Authorization": "Bearer " + apikey},
    json={
        "prompt": prompt, 
        "numResults": 1, 
        "maxTokens": 64, 
        "stopSequences": ["Q:"],
        "topKReturn": 0,
        "temperature": 0.0
    }
    )
    responsejson = json.loads(response1.text)
    
    completed = responsejson['completions'][0]['data']['text']



    #output = os.popen(str(completed).replace("A:", "", 1)).read()
    output = str(completed).replace("A:", "", 1)
    output = "\n".join([ll.rstrip() for ll in output.splitlines() if ll.strip()])



    editedcommand = input(output)
    finaloutput = os.popen(output).read()

    print(finaloutput)
