import google.generativeai as genai
import os

# Configura tu API key
os.environ["API_KEY"] = "Insert Your API Key"
genai.configure(api_key=os.environ["API_KEY"])

# Definir la configuración del modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Inicializar el modelo del asistente médico
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Eres un asesor médico que recomienda con qué especialidad médica sacar cita "
        "en función de los síntomas proporcionados por el usuario. No das diagnósticos, "
        "pero ayudas a dirigir al paciente a la especialidad adecuada. "
        "Haz una pregunta por vez para recopilar datos adicionales del usuario, tomando en cuenta sus respuestas anteriores."
    ),
)

# Función que maneja la conversación
def start_conditional_chat():
    max_questions = 5
    questions_asked = 0
    conversation_history = []  # Almacena la conversación completa
    
    # Pregunta inicial sobre los síntomas generales
    print("Asistente: Buen día, estoy aqui para ayudarte a elegir tu especialidad médica a visitar. Por favor, describe tus síntomas principales.")
    user_input = input("Usuario: ")
    conversation_history.append(f"Usuario: {user_input}")
    
    # Generar y procesar hasta 5 preguntas dinámicas basadas en las respuestas
    while questions_asked < max_questions:
        # El prompt se genera usando el historial de conversación
        prompt = " ".join(conversation_history) + " Con base en esto, haz una pregunta más para obtener más información sobre los síntomas."
        response = model.generate_content(prompt)
        print(f"Asistente: {response.text}")
        
        # Recibir la respuesta del usuario
        user_input = input("Usuario: ")
        conversation_history.append(f"Asistente: {response.text}")
        conversation_history.append(f"Usuario: {user_input}")
        questions_asked += 1
    
    # Generar la recomendación final
    symptoms_summary = " ".join(conversation_history)  # Unir toda la conversación
    final_prompt = f"{symptoms_summary} Basado en esta información, ¿qué especialidad médica debería consultar el usuario?"
    final_response = model.generate_content(final_prompt)
    print(f"Recomendación final: {final_response.text}")

# Iniciar la conversación
start_conditional_chat()
