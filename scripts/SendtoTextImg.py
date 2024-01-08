import contextlib
import gradio as gr
import json
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
                send_text_button = gr.Button(value='Random Artist', variant='primary')

        with contextlib.suppress(AttributeError):  # Ignore the error if the attribute is not present
            if is_img2img:
                send_text_button.click(fn=self.get_artist, inputs=[self.boxxIMG], outputs=[self.boxxIMG])
            else:
                send_text_button.click(fn=self.get_artist, inputs=[self.boxx], outputs=[self.boxx])
        return [send_text_button]

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








