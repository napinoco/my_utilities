# Whisper template
This code uses OpenAI's Whisper to transcribe (for free, without using the API).

It finds audio files placed directly under the specified directory, transcribes them, and outputs the result as a txt file with the same name as the audio file.

You can also use the GPU runtime of Google Colab
https://colab.research.google.com/drive/1iC8dHZ2SlCykoAQu-yHAPzs8dZKPJrtr

## Installation
```
pip install tqdm git+https://github.com/openai/whisper.git
```
