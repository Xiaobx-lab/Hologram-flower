import gradio as gr
import paho.mqtt.client as mqtt

from state_holder import state


def upload_file(file):

    # oh, the user uploaded an image.
    # continue to melting, loading
    #publish to next state here.
    print("try to publish")
    client.publish("IMAGE_PATH", file.name)
    client.publish("test/state", "UPLOAD_DONE")
    print("published the file")
    print(file.name)
    # may be organise the file.name to a location that your others codes need it.
    return file.name

with gr.Blocks() as demo:
    file_output = gr.File()
    upload_button = gr.UploadButton("Click to Upload a File", file_types=["image"], file_count="single")
    upload_button.upload(upload_file, upload_button, file_output)


client = mqtt.Client()
client.connect("localhost", 1883, 60)

demo.launch(server_port=8443)

