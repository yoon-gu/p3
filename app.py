import gradio as gr
import numpy as np
import pandas as pd
import subprocess
from datetime import datetime, timedelta

def preprocess_rawdata(files):
    print(files)
    dfs = []
    for file in files:
        print(file)
        df = pd.read_html(file, header=2)[0]
        dfs.append(df)
    return pd.concat(dfs)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            input_files = gr.File(label="Upload Multiple Files Output", file_count="multiple")
        with gr.Column(scale=1):
            a = 1
    with gr.Row():
        df = gr.Dataframe(interactive=True)

    input_files.upload(preprocess_rawdata, input_files, df)

if __name__ == "__main__":
    demo.launch()
