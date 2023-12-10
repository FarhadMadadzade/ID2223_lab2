# ID2223_lab2
This is the repository for whisper_romanian, a whisper-small model fine-tuned for Romanian language processing. The goal is to provide a model that can, with decent accuracy, provide transcriptions of Romanian speech.

## Model 
whisper_romanian is a fine-tuned version of openai/whisper-small on the Romanian voice 1.0 dataset. The best model achieves the following results on the evaluation set after 1500 rounds of training:

- Loss: 0.2557
- Wer: 23.87

Link to the model: [whisper-romanian](https://huggingface.co/Artanis1551/whisper_romanian)

## Ways in which model performance can be improved
Model-centric approach:
  - Disabled the use of reduced precision fp16;
  - Halved the learning rate from 1e-5 to 5e-6
  - Cut down the warmup steps to 50 and the overall steps to 1500 as we noticed very high overfitting after that point

Data-centric approach:
  - One way to improve upon the data would be to either figure out how to participate in the voting that's used to split the dataset into training, validation, test, and other and try to influence it so the "other" split is moved into either training or test so we can increase the dataset
  - Another way to get data for this kind of training is to create a type of captcha that requires the user to read a phrase in their native language and collect that data
  - Data rows can be created manually based on complaints from customers (assuming some kind of commercial product that uses this model)


## How we achieved our results by improving model performance
The first version of the model that we created used the hyperparameters that were used in the Python notebook that was provided together with the assignment (swedish_fine_tune_whisper.ipynb). Since we also had access to a computer with GPU computing power we fine-tuned for a total of 4000 rounds. This yielded poor results with WER upwards of 200+.

Next, we made model-centric improvements to get better results. The first improvement was seen with this model:[first improvement](https://huggingface.co/Artanis1551/whisper_romanian3). Here we increased the learning rate by a factor of 10 and halved the number of warmup steps, however, we kept training for 4000 rounds.
Although we saw a lot of improvements in the WER, we were not quite happy because the performance of the model in our UI was not optimal and often gave weird outputs. We noticed that at the first checkpoint at step 1000, the WER was already 88, which seemed high already, after which it approximately halved at the final 4000th step, which made us realize that the learning rate was too high. We instead used a learning rate of 5e-6 further decreased the number of warmup steps and noticed improvements right away. The final changes we made was to only train for 1500 rounds because we noticed that the model started overfitting past that, as well as disabling the use of reduced precision fp16. fp16 can often increase the speed of model training and requires less memory and computational resources but comes at the cost of model accuracy due to the reduced precision. Disabling this also yielded better results. The final version of the model hence became this model: [whisper_romanian](https://huggingface.co/Artanis1551/whisper_romanian)

Comparing the results on the Huggingface models we can see very clear improvements between the models.


# Huggingface UI
The UI developed to showcase the use of the model is intended for demonstration purposes. We wrote a script that given a specific date, navigates to the Romanian parliament's website and goes to their media archive where they have uploaded recordings from parliament meetings and downloads the video published on that date. The videos in the archive are much longer than 30 seconds which is the maximum audio input length the model takes. Hence, for demonstration purposes, we only transcribe and present the first 30 seconds of the video. In the UI, you write the date that the recording was published (in the format YYYYMMDD) and press submit. Given that there is a recording and everything goes smoothly, the output will be the video that is transcribed, as well as the transcription below it. If there is no video at the given date, a surprise will be shown to the user along with informative text in the output textbox. 

Link to the final UI: [Huggingface space](https://huggingface.co/spaces/ID2223-labs/romanian_parliament_transcription)

