import gradio as gr
import uvicorn
from fastapi import FastAPI

description = """
# Test FastAPI to do awesome stuff. 🚀
## Usage
- POST to **/path-to-test**
- with body/message
## Security
- Rate Limit : **3/second max**
## Author
- Damien Chauvet
"""

app = FastAPI(
    title="FastAPI-gradio",
    description=description,
    version="0.0.1",
)


@app.get("/", tags=["Root"])
async def root():
    """
    Page d'accueil
    :return:
    """
    return {"message": "Hello World, updated by CI/CD"}


def sample_input_fn():
    return "eqsffqeqef", "segfùms gs egs eg sge"


def select_tag_fn(_tags):
    tags_out = []
    for tag in _tags:
        tags_out.append(tag.split(" ")[0])
    return " ".join(tags_out)


def prediction_fn(title_input, body_input):
    print("query ", title_input, body_input)
    predictions = [("c#", ".86"), ("java", ".92")]
    results = [f"{p[0]} ({float(p[1]):.0%})" for p in predictions]
    chk_grp = gr.Checkboxgroup(
        label="Tags",
        info="Liste des Tags prédits + probabilitéss.",
        choices=results,
        interactive=True,
    )
    return chk_grp


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            gr.HTML("<h1>Bienvenue !</h1>")
            gr.HTML("<p>Tags prédiction !</p>")
            gr.HTML("<hr>")
    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            gr.HTML("<b>1</b> Entrer votre question ici 👇")
            title_input = gr.Text(label="Title")
            body_input = gr.TextArea(label="Body")
            tags_selected = gr.Text(label="Tags", interactive=False)
        with gr.Column(scale=1, min_width=200):
            gr.HTML("<b>2</b> Ou choisissez des exemples ci-dessous 👇")
            sample_input1 = gr.Button("Exemple 1", min_width=600)
            sample_input2 = gr.Button("Exemple 2", min_width=600)
            sample_input3 = gr.Button("Exemple 3", min_width=600)
            gr.HTML("<b>3</b> Puis lancez la prédiction 🚀")
            predict_button = gr.Button("Prédire des Tags")
            tags_output = gr.Checkboxgroup(label="Résultats", interactive=True)

predict_button.click(
    fn=prediction_fn,
    inputs=[title_input, body_input],
    outputs=[tags_output],
)
sample_input1.click(fn=sample_input_fn, outputs=[title_input, body_input])
sample_input1.click(fn=sample_input_fn, outputs=[title_input, body_input])
sample_input1.click(fn=sample_input_fn, outputs=[title_input, body_input])
tags_output.select(fn=select_tag_fn,
                   inputs=[tags_output],
                   outputs=[tags_selected])

app = gr.mount_gradio_app(app, demo, path="/gradio-demo")

if __name__ == "__main__":
    uvicorn.run(app)
