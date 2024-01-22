import contextlib
import gradio as gr
import json
import jsonlines
import random
from modules import scripts
from modules import script_callbacks

def get_random_artist_prompt():
    with open('extensions/artjiggler/artist.json', 'r') as file:
        data = json.load(file)
        selected_artist = random.choice(data)
        return selected_artist.get('prompt')

class ArtJiggler(scripts.Script):
    def __init__(self) -> None:
        super().__init__()
        self.last_artist = None

    def title(self):
        return "ArtJiggler"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("ArtJiggler", open=False):
                artist_button = gr.Button(value='Random Artist', variant='primary')
                jiggle_button = gr.Button(value='Jiggle Prompt', variant='primary')

        with contextlib.suppress(AttributeError):  # Ignore the error if the attribute is not present
            if is_img2img:
                artist_button.click(fn=self.get_artist, inputs=[self.boxxIMG], outputs=[self.boxxIMG])
                jiggle_button.click(fn=self.jiggle_prompt, inputs=[self.boxxIMG], outputs=[self.boxxIMG])
            else:
                artist_button.click(fn=self.get_artist, inputs=[self.boxx], outputs=[self.boxx])
                jiggle_button.click(fn=self.jiggle_prompt, inputs=[self.boxx], outputs=[self.boxx])
        return [artist_button]

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt": #postive prompt textbox
            self.boxx = component
        if kwargs.get("elem_id") == "img2img_prompt":  #postive prompt textbox
            self.boxxIMG = component

    def get_artist(self, old_prompt):
        if old_prompt == "":
            artist = get_random_artist_prompt()
            self.last_artist = artist
            return artist
        else:
            if self.last_artist is not None:
                old_prompt = old_prompt.replace(f'. {self.last_artist}', '')
            artist = get_random_artist_prompt()
            self.last_artist = artist
            return old_prompt + ". " + artist

    def jiggle_prompt(self, search_string):
        found_words = {}
        updated_string = search_string.split()  # Create a list to store updated words
        with jsonlines.open('extensions/artjiggler/thesaurus.jsonl') as reader:
            for line in reader:
                for i, word in enumerate(updated_string):
                    if len(word) >= 3:  # Check if word is 3 letters or longer
                        if 'word' in line and word == line['word']:
                            if 'synonyms' in line and line['synonyms'] and isinstance(line['synonyms'], list):
                                if word not in found_words:
                                    found_words[word] = random.choice(line['synonyms'])
                                else:
                                    existing_synonym = found_words[word]
                                    new_synonym = random.choice(line['synonyms'])
                                    selected_synonym = random.choice([existing_synonym, new_synonym])
                                    found_words[word] = selected_synonym
                                    updated_string[i] = selected_synonym

        return ' '.join(updated_string)  # Return the updated string








