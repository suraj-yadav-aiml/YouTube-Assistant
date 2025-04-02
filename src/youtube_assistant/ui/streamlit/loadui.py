import os
import streamlit as st
from src.youtube_assistant.ui.streamlit import Config

class StreamlitUILoader:
    def __init__(self):
        self.config = Config()
        self.user_input = {}
    
    def _validate_api_key(self, api_key: str, service: str, reference_link: str) -> None:
        """
        Validate and display warning for API keys.
        
        Args:
            api_key (str): API key to validate
            service (str): Name of the service
            reference_link (str): Link for obtaining API key
        """
        if not api_key:
            st.warning(f"⚠️ Please enter your {service} API key to proceed. Don't have one? Refer: {reference_link}")
    
    def _setup_groq_configuration(self) -> None:
        """Set up Groq LLM configuration in the sidebar."""
        groq_model_options = self.config.get_groq_model_options()
        self.user_input['selected_groq_model'] = st.selectbox(label="Select Groq Model", options=groq_model_options)

        groq_api_key = st.text_input(label="GROQ API KEY", type='password')
        self.user_input['GROQ_API_KEY'] = groq_api_key
        st.session_state['GROQ_API_KEY'] = groq_api_key
        os.environ['GROK_API_KEY'] = groq_api_key

        self._validate_api_key(
            groq_api_key, 
            "GROQ", 
            "https://console.groq.com/keys"
        )
    
    def _setup_openai_configuration(self) -> None:
        """Set up OpenAI LLM configuration in the sidebar."""
        openai_model_options = self.config.get_openai_model_options()
        self.user_input['selected_openai_model'] = st.selectbox(label="Select OpenAI Model",options=openai_model_options)

        openai_api_key = st.text_input(label="OPENAI API KEY", type='password')
        self.user_input['OPENAI_API_KEY'] = openai_api_key
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key

        self._validate_api_key(
            openai_api_key, 
            "OpenAI", 
            "https://platform.openai.com/settings/organization/api-keys"
        )
    
    def _setup_anthropic_configuration(self) -> None:
        """Set up Anthropic LLM configuration in the sidebar."""
        anthropic_model_options = self.config.get_anthropic_model_options()
        self.user_input['selected_anthropic_model'] = st.selectbox(label="Select Anthropic Model",options=anthropic_model_options)

        anthropic_api_key = st.text_input(label="ANTHROPIC API KEY", type='password')
        self.user_input['ANTHROPIC_API_KEY'] = anthropic_api_key
        st.session_state['ANTHROPIC_API_KEY'] = anthropic_api_key
        os.environ['ANTHROPIC_API_KEY'] = anthropic_api_key

        self._validate_api_key(
           anthropic_api_key, 
            "Anthropic", 
            "https://console.anthropic.com/settings/keys"
        )
    
    def load_streamlit_ui(self) -> dict:
        page_title = self.config.get_page_title()
        st.set_page_config(page_title="🤖 " + page_title, layout="wide")
        st.header("🤖 " + page_title)

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            self.user_input['selected_llm'] = st.selectbox(label="Select LLM", options=llm_options)

            if self.user_input['selected_llm'] == "Groq":
                self._setup_groq_configuration()
            elif self.user_input['selected_llm'] == "OpenAI":
                self._setup_openai_configuration()
            elif self.user_input['selected_llm'] == "Anthropic":
                self._setup_anthropic_configuration()
            
            usecase_options = self.config.get_usecase_options()
            self.user_input['selected_usecase'] = st.selectbox(label="Select Usecase",options=usecase_options)

            # if self.user_input['selected_usecase'] == "Chatbot with Tools":
            #     self._setup_tavily_configuration()
        
        return self.user_input