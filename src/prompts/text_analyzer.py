from langchain.prompts import ChatPromptTemplate

def text_analyzer(video_text: str) -> ChatPromptTemplate:
    """Creates a prompt template for generating a video summary in JSON format."""
    prompt_text = (
        "Eres un asistente especializado en análisis de textos. Recibirás un texto en español, inglés o portugués de Brasil, "
        "y tu tarea es identificar los puntos más importantes del contenido.\n\n"
        "- Selecciona las ideas principales y detalles clave que ayuden a comprender el núcleo de la información.\n"
        "- El resumen debe ser breve y directo, manteniendo solo lo esencial del texto.\n"
        "- Responde exclusivamente en español.\n"
        "Ejemplos de cómo estructurar el resumen:\n"
        "- Si el texto describe un evento, explica qué ocurrió, quiénes estuvieron involucrados y cualquier consecuencia importante.\n"
        "- Si es un informe o artículo, identifica los hallazgos principales, conclusiones o cualquier dato significativo mencionado.\n\n"
        "Toma en cuenta que el texto puede estar en cualquiera de estos tres idiomas (español, inglés o portugués), pero la respuesta debe estar siempre en español."
    )
    return ChatPromptTemplate.from_messages([('system', prompt_text), ('user', video_text)])