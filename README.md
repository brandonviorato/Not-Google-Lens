# Not Google Lens

Not Google Lens is an image translation tool that extracts text from images using local OCR and translates it using offline large language models and then overlays the translated text over the original image.

## Table of Contents
- [Features](#features)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and use](#setup-and-use)
    - [Cloning the repository](#cloning-the-repository)
    - [Creating a virtual environment](#creating-a-virtual-environment)
    - [Installing packages](#installing-packages)
    - [Running Not Google Lens](#running-not-google-lens)
    - [Additional setup](#additional-setup)
        - [Changing translation prompt](#changing-translation-prompt)
        - [Changing translation languages](#changing-translation-languages)
        - [Changing the translation LLM](#changing-the-translation-llm)
- [Capabilities and limitations](#capabilities-and-limitations)
- [Potential future improvements](#potential-future-improvements)

## Features

- All processing done locally via OCR and LLM translation
- Translated text overlayed ontop of original image
- No data sent externally

## Prerequisites

**Not Google Lens was developed on a Windows machine. There has been no testing for compatibility on other operating systems. There is no guaranteee that following these instructions will result in a functional application.**

Before you can use Not Google Lens, you must first complete the following:

1. Install [Ollama](https://ollama.com/download) - The text translation is done using an LLM.
    1. After installing Ollama, download the [llama-translate](https://ollama.com/7shi/llama-translate) model.
    2. Verify functionality by running `ollama run 7shi/llama-translate:8b-q4_K_M` in a terminal and asking it to translate some Japanese text into English or vice versa.

2. Install [EasyOCR](https://www.jaided.ai/easyocr/install/) - This is the OCR software which extracts text from images. Please note that if installing on Windows, you may need to install pytorch manually. You should follow their instructions [here](https://pytorch.org/get-started/locally/)

After completing these steps, you can proceed to the [Setup and use](#setup-and-use)

## Setup and use

**Not Google Lens was developed on a Windows machine. There has been no testing for compatibility on other operating systems. There is no guaranteee that following these instructions will result in a functional application.**

To setup and use Not Google Lens, you should first complete the steps outline in the [Prerequisites](#prerequisites). Failure to do so may result in issues with OCR and translation.

### Cloning the repository

Clone the Not Google Lens repository to a suitable location on your local disk.

```https://github.com/brandonviorato/Not-Google-Lens.git```

### Creating a virtual environment

In a terminal, navigate into the project root and create a virtual environment.

```python -m venv venv```

After creating a virtual environment, you will need to activate it.

```.\venv\Scripts\Activate.ps1```

### Installing packages

In the same terminal window, install the required packages by running:

```pip install -r requirements.txt```

Please note that this may take several minutes depending on your internet connection speed.

### Running Not Google Lens

After successfully completing all previous steps, run:

```python app.py```

Then just select an image by clicking `Open File` and then click `Translate Image` to translate the selected image.

### Additional setup

#### Changing translation prompt

Since the text translation is done using an LLM, you can adjust the prompt for the LLM in the `translation_prompt.txt` file. Through my testing, concise prompts tend to yield better results.

#### Changing translation languages

The [llama-translate](https://ollama.com/7shi/llama-translate) model supports translation between **English, French, Chinese(Mandarin) and Japanese**. To change the translation language, you will need to change the following:

1. In `image_translator.py` adjust the [language codes](https://www.jaided.ai/easyocr/) in line 19 to the desired languages: ```reader = easyocr.Reader(['ja', 'en'])  # e.g., Japanese + English```

2. In the `translation_prompt.txt` file, specify the source and target languages the LLM will be translating the text to and from.

#### Changing the translation LLM

Ollama allows for easy swapping of LLM.

To change the LLM for translation, find a suitable LLM from the [Ollama model search](https://ollama.com/search) and download it using the provided command. Then, in the `translator.py` file, on line 4, change the value of the `model` variable to the name of the model you would like to use.

**Dont forget you can change the translation prompt too!**

## Capabilities and limitations

Not Google Lens is currently capable of:

- Accepting an image and extracting text via OCR
- Translating the extracted text using an LLM
- Overlaying the translated text on top of the original image

So far, it is quite good at doing what it was designed to do. During development, I focused on hardware compatibility. Large Language Models are notorious for requiring a beefy GPU with tons of VRAM. I was able to find a [model](https://qiita.com/7shi/items/ae0da373184b82d53fcc#%E5%8B%95%E4%BD%9C%E7%A2%BA%E8%AA%8D) that was optimized for performance using CPU only.

Although you will still likely want to use a GPU for quality of life. My RX 7800XT can process each image in less than 15 seconds on average.

Additionally, easyOCR runs decently on CPU only. I did not bother with setting up pytorch to use an AMD GPU since easyOCR can OCR each image in less than a couple seconds on a Ryzen 9 9600X.

So if you have a lower-end machine or one without a GPU at all, you should still be able to find Not Google Lens usable at best.

Unfortunately, these performance optimizations come with tradeoffs.

The selected LLM is inconsistent with its translations. Translating the same image repeatedly will result in varying translations. Occassionally, it will hallucinate if text from the source langage is sent to it for translation.

The way in which the text is sent to the LLM for translation also negatively affects the quality of the translation. EasyOCR is good at recognizing words, which results in the OCR text looking something like this:

```
[([[448, 111], [917, 111], [917, 243], [448, 243]],'高鐵左營站',0.9247),
([[454, 214], [629, 214], [629, 290], [454, 290]], 'HSR', 0.9931),
([[664, 222], [925, 222], [925, 302], [664, 302]],'Station',0.3260),
([[312, 306], [937, 306], [937, 445], [312, 445]],'汽車臨停接送區',0.7417),
([[482, 418], [633, 418], [633, 494], [482, 494]],'Kiss',0.9577),
([[331, 421], [453, 421], [453, 487], [331, 487]], 'Car', 0.9630),
([[653, 429], [769, 429], [769, 495], [653, 495]], 'and', 0.9243),
([[797, 429], [939, 429], [939, 497], [797, 497]],'Ride',0.6400)]
```

Because of this, each recognized word is sent on its own to the LLM for translation. This negatively affects the quality of the translation for context-dependent languages such as Japanese.

There is no easy way to go about this as sending a large amount of tokens to an LLM will increase the response times, but improve the translation quality because of the additional context.

Sending each individual word greatly speeds up the response times of an LLM because it only needs to process a couple tokens.

## Potential future improvements

As mentioned earlier the biggest future improvement that is possible for this app is with how the text is processed for translation. Once a method that has a good balance of speed and quality is figured out, the translation quality will be far superior than what it is now.

Presentation (link)[https://docs.google.com/presentation/d/1nY8YbidIbbHJV5MF6GZc0imnnbX5EX8tn8kWIAEj2fM/edit?usp=sharing]
