import gradio as gr
from script.gemini_extarction import gemini_extraction

# Gradio Interface
iface = gr.Interface(
    fn=gemini_extraction,
    inputs=[
        gr.Textbox(label="Input Directory(EML File Location)"),
        gr.Textbox(label="Output Directory"),
        gr.Textbox(label="System Message"),
        gr.Textbox(label="User Requirement"),
        gr.Textbox(label="User Input"),
        gr.Number(label="temperature")


    ],
    outputs=gr.Textbox("Output"),
    live=False,
)
# Set default values directly in the Interface constructor
iface.launch()
