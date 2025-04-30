import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# Configuración de la página con tema oscuro
st.set_page_config(
    page_title="Análisis de Texto",
    page_icon="📝",
    layout="centered"
)

# CSS personalizado para dark mode
st.markdown("""
    <style>
        /* Tema oscuro principal */
        :root {
            --primary-bg: #2D2D2D;
            --secondary-bg: #252525;
            --element-bg: #333333;
            --border-color: #444444;
            --text-color: #FFFFFF;
            --accent-color: #4F8BF9;
        }
        
        /* Todos los textos en blanco */
        * {
            color: var(--text-color) !important;
        }
        
        body {
            background-color: var(--primary-bg);
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Contenedor principal */
        .stApp {
            background-color: var(--primary-bg);
            padding: 1rem;
        }
        
        /* Sidebar */
        .stSidebar {
            background-color: var(--secondary-bg) !important;
            border-right: 1px solid var(--border-color);
        }
        
        /* Text areas e inputs */
        .stTextArea textarea, .stTextInput input {
            background-color: var(--element-bg) !important;
            border: 1px solid var(--border-color) !important;
            color: white !important;
        }
        
        /* Expanders */
        .stExpander {
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            margin-bottom: 1rem;
        }
        
        /* Títulos */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: var(--text-color) !important;
        }
        
        /* Resultados */
        .stAlert {
            background-color: var(--element-bg) !important;
            border: 1px solid var(--border-color) !important;
        }
    </style>
""", unsafe_allow_html=True)

translator = Translator()
st.title('📋 Uso de TextBlob')

st.subheader("Escribe la frase que deseas analizar")

with st.sidebar:
    st.subheader("📊 Polaridad y Subjetividad")
    st.markdown("""
    **Polaridad**:  
    Indica si el sentimiento es positivo, negativo o neutral.  
    Rango: -1 (muy negativo) a 1 (muy positivo)  
    
    **Subjetividad**:  
    Mide contenido subjetivo (opiniones) vs objetivo (hechos).  
    Rango: 0 (objetivo) a 1 (subjetivo)
    """)

with st.expander('🔍 Analizar Sentimiento', expanded=True):
    text1 = st.text_area('Escribe tu texto aquí:', height=100, 
                        placeholder="Ingresa el texto a analizar...")
    
    if text1:
        with st.spinner("Analizando..."):
            try:
                translation = translator.translate(text1, src="es", dest="en")
                trans_text = translation.text
                blob = TextBlob(trans_text)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Polaridad", round(blob.sentiment.polarity, 2))
                with col2:
                    st.metric("Subjetividad", round(blob.sentiment.subjectivity, 2))
                
                x = round(blob.sentiment.polarity, 2)
                if x >= 0.5:
                    st.success('Sentimiento Positivo 😊')
                elif x <= -0.5:
                    st.error('Sentimiento Negativo 😔')
                else:
                    st.info('Sentimiento Neutral 😐')
                
                st.markdown("---")
                st.markdown("**Texto traducido al inglés:**")
                st.code(trans_text, language='text')
                
            except Exception as e:
                st.error(f"Error en el análisis: {str(e)}")

with st.expander('✏️ Corrección en inglés'):
    text2 = st.text_area('Escribe texto en inglés para corregir:', 
                        height=100, key='corrector',
                        placeholder="Ingresa texto en inglés...")
    if text2:
        with st.spinner("Corrigiendo..."):
            try:
                blob2 = TextBlob(text2)
                corrected = blob2.correct()
                
                st.markdown("**Texto original:**")
                st.code(text2, language='text')
                
                st.markdown("**Texto corregido:**")
                st.code(str(corrected), language='text')
                
                if str(corrected).lower() != text2.lower():
                    st.success("Correcciones aplicadas ✅")
                else:
                    st.info("No se encontraron correcciones necesarias")
                    
            except Exception as e:
                st.error(f"Error en la corrección: {str(e)}")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con Streamlit y TextBlob | Análisis de texto")
