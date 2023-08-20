import os
import whisper
import tqdm

work_dir = 'path_to_dir'  # change this


def get_untranscribed_files(work_dir: str):
    all_files = os.listdir(work_dir)
    audio_ext = {'.wav', '.mp3', '.m4a', '.mp4'}
    audio_files = {f for f in all_files if os.path.splitext(f)[1] in audio_ext}
    text_files = {f for f in all_files if f.endswith('.txt')}

    return {f for f in audio_files if (os.path.splitext(f)[0] + '.txt') not in text_files}


def main():
    model = whisper.load_model('large')
    untranscribed_files = get_untranscribed_files(work_dir)
    print(untranscribed_files)
    for filename in tqdm.tqdm(untranscribed_files):
        result = model.transcribe(os.path.join(work_dir, filename))
        with open(os.path.join(work_dir, os.path.splitext(filename)[0] + '.txt'), 'w') as f:
            f.write(result['text'])


if __name__ == '__main__':
    main()
