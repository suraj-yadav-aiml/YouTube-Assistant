from typing import Dict
from pydantic import BaseModel, Field
import streamlit as st
import traceback
from src.youtube_assistant.llm import get_llm
from src.youtube_assistant.state import BlogState
from langchain_core.messages import SystemMessage, HumanMessage


class BlogTitle(BaseModel):
    """Pydantic model for blog title generation."""
    
    title: str = Field(
        description=(
            "A compelling, SEO-friendly blog title derived from video transcript content.\n"
            "Should be:\n"
            "- Between 40-60 characters long\n"
            "- Contain main keywords from the transcript\n"
            "- Be engaging but not clickbait\n"
            "- Use proper capitalization\n"
            "- Avoid special characters except '?', ':', '-'"
        )
    )


class GenerateBlogTitleNode:
    """Node for generating blog titles from YouTube video transcripts."""
    
    def __init__(self, user_input: Dict[str, str]):
        """
        Initialize the blog title generator.
        
        Args:
            user_input (Dict[str, str]): User configuration for the LLM.
        """
        try:
            self.llm = get_llm(user_input)
        except Exception as e:
            error_msg = f"Failed to initialize LLM: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)
    
    def _create_messages(self, transcript: str) -> list:
        """
        Create the system and human messages for the LLM.
        
        Args:
            transcript (str): The validated transcript.
            
        Returns:
            list: A list of messages for the LLM.
        """
        system_msg = SystemMessage(
            content=(
                "You are an expert blog title generator optimizing for both engagement and SEO.\n\n"
                "Guidelines for title generation:\n"
                "1. Analyze the transcript for main topic, key points, and unique insights\n"
                "2. Create a title that accurately reflects the content\n"
                "3. Use power words that drive engagement\n"
                "4. Include relevant keywords for SEO\n"
                "5. Maintain professional tone - no clickbait or sensationalism\n"
                "6. Use proper grammar and capitalization\n"
                "7. Keep length between 40-60 characters\n"
                "8. Make it compelling but honest\n\n"
                "Focus on creating a title that would make readers want to learn more while "
                "accurately representing the content."
            )
        )
        
        human_msg = HumanMessage(
            content=(
                "Please analyze this video transcript and generate an optimal blog title.\n\n"
                "Consider these aspects while analyzing:\n"
                "- Main topic and key message\n"
                "- Target audience\n"
                "- Unique insights or valuable information\n"
                "- Professional context\n\n"
                f"Transcript:\n{transcript}"
            )
        )
        
        return [system_msg, human_msg]
    
    def generate_blog_title_node(self, state: BlogState) -> Dict[str, str]:
        """
        Generate a blog title based on the transcript in the state.
        
        Args:
            state (BlogState): The application state containing the transcript.
            
        Returns:
            Dict[str, str]: A dictionary containing the generated blog title.
            
        Raises:
            RuntimeError: If the title generation process fails.
        """
        try:
            transcript = state.get("youtube_transcript")
            if not transcript:
                error_msg = "Transcript is missing or empty"
                st.error(error_msg)
                raise ValueError(error_msg)
            
            messages = self._create_messages(transcript)
            
            try:
                with st.spinner("Generating blog title..."):
                    title_generator_llm = self.llm.with_structured_output(schema=BlogTitle)
                
                    response = title_generator_llm.invoke(input=messages)
                    
                    if not response or not hasattr(response, 'title'):
                        error_msg = "Failed to generate a title - empty response from LLM"
                        st.error(error_msg)
                        raise RuntimeError(error_msg)
                    
                    st.toast("Blog title generated successfully!")
                    
                    return {'blog_title': response.title}
                
            except Exception as e:
                error_msg = f"Title generation failed: {str(e)}"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
                
        except Exception as e:
            error_msg = f"Blog title generation process failed: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)