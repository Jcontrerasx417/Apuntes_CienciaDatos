import os
import gradio as gr
from openai import OpenAI

# Cliente NVIDIA
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv(
        "NVIDIA_API_KEY",
        "TU_API_KEY_AQUI"
    )
)

# Función del chat
def responder(mensaje, historial):
    # Convertir historial al formato OpenAI
    mensajes = []

    for usuario, bot in historial:
        mensajes.append({"role": "user", "content": usuario})
        mensajes.append({"role": "assistant", "content": bot})

    mensajes.append({"role": "user", "content": mensaje})

    # Llamada al modelo
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=mensajes,
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": True
            },
            "reasoning_budget": 16384
        },
        stream=False
    )

    respuesta = completion.choices[0].message.content

    # Guardar historial
    historial.append((mensaje, respuesta))

    return historial, historial


# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("# mi_primer_chat")

    chatbot = gr.Chatbot()
    estado = gr.State([])

    with gr.Row():
        entrada = gr.Textbox(
            placeholder="Escribe tu mensaje...",
            show_label=False
        )

        boton_enviar = gr.Button("Enviar")

    boton_enviar.click(
        responder,
        inputs=[entrada, estado],
        outputs=[chatbot, estado]
    )

    entrada.submit(
        responder,
        inputs=[entrada, estado],
        outputs=[chatbot, estado]
    )

# Ejecutar
demo.launch()