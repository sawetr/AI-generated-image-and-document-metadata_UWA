# UWA Library Metadata Generation App

A step-by-step walkthrough to installing and running the UWA Library Metadata Generation App. Before you run the application, it is crucial to follow the prerequisite steps.

---

# Prerequisites
[LLM Studio](https://lmstudio.ai/download) 
---
- Download the LLM Studio launcher that is compatible with your operating system. Run the launcher as you would a normal installer.
  
- Click on the LLM Studio Shortcut to open the application. Upon initial start up, it will return the dashboard below.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/llm1.png)

- Click on the purple magnifying glass icon and it will redirect you to **Model Search**, allowing you to search for the model you need. After searching for the
  model, click the green button to download the model.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/llm3.png)

- Once the download is complete, click the red folder icon and then the **three dots**. This will open a dropdown of options, then click on **"Open in File Explorer"**.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/llm3dots.png)

- It will redirect you to this screen. Click on **"Open in File Explorer"** one more time.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/llm4.png)

- This is the **path** where your model is saved. Click on the bar so that it highlights the path in blue, then "Copy" the path and **save it for later**.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/llm5.png)

For example, it will probably look like this

```bash
C:\Jodi\.lmstudio\models\lmstudio-community\Qwen2.5-VL-7B-Instruct-GGUF
```

- You can repeat this steps to download all three of the models you want (i.e. Gemma3 13B, Gemma3 27B, Qwen2.5 7B)

[Docker Desktop](https://lmstudio.ai/download](https://www.docker.com/products/docker-desktop/)) 
---
- After installing the models, you need to now install Docker Desktop to install MongoDB and run the Dockerfile. Upon initial start up,
click on Docker Hub.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/docker1.png)

- In the search bar, query and click on the one that says "The Official MongoDB Community Server".

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/docker2.png)

- Click on "Pull" and, after a few minutes, you will see a status message on the lower right indicating that it was a success.
  
![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/docker3-pull.png)

- Click on **"Images"** and, in the row with the green circle, click "Run".

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/docker4.png)

- It will redirect you to this interface where, in the "Host Port" field, specify `27017`. Then click "Run".

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/docker5-port.png)

- Click on **"Containers"** and you should see your newly created contained (with the green circle icon showing that it is active)
with the port successfully specified.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/docker5success.png)

# Required Files
---
For the next step, ensure you have the following files downloaded in the same folder.

- **Dockerfile**
- **.dockerignore**
- **.env**
- **requirements.txt**

Once that is done, we will now execute the Dockerfile to install and run the application.

# Run Commands
---

- Open the Terminal and change to the directory (i.e. folder) that contains the required files.
  
```bash
cd "C:\Jodi\Downloads"
```

- Type the following command to run the Dockerfile.
  
```bash
docker build --no-cache --progress=plain -t uwa_artifact_processor .
```

The image is successfully created when you see a similar output appear on your terminal.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/df1.png)

- When the image is successfully created, you can now run the command to run the application.
From the path we copied from the LLM Studio section, paste it inside the quotations before the
`:/app/models`.

```bash
docker run -d -p 5000:5000 `
  -v "[PASTE PATH HERE]:/app/models" `
  --env-file .env `
  --name flask_app `
  uwa_artifact_processor
```

For example

```bash
docker run -d -p 5000:5000 `
  -v "C:\Jodi\.lmstudio\models\lmstudio-community\Qwen2.5-VL-7B-Instruct-GGUF:/app/models" `
  --env-file .env `
  --name flask_app `
  uwa_artifact_processor
```
- The image is successfully running when you are able to see this interface.
  
![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/df2.png)


- To verify if your model is running you can use two different commands

```bash
docker logs -f flask_app

#OR

curl http://localhost:5000/health
```
![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/df3.png)


![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/df4.png)

Initially the status of "model_loaded" or Model loaded is **False** -- this is normal as it takes a while to load the model. Once the status has changed to **True** 
then you can finally, use the application.

- Keep on monitoring the status using either of the two commands.

# Using the Application
---

Assuming you did not shut down your computer or stop the container, you can copy paste the port `http://127.0.0.1:5000/` to your search engine and it will return this
interface

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/app1.png)

- Upload the image of the artifact you want to process, then click the "Process" button.

- After awhile, it will generate the metadata in a JSON format as the one shown below.

![Description](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/main/install_imgs/app2.png)

---
This marks the end of the walkthrough, thank you!







