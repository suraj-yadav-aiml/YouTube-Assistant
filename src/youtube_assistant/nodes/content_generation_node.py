from typing import Dict, Optional
import streamlit as st
import traceback
from src.youtube_assistant.llm import get_llm
from src.youtube_assistant.state import BlogState
from langchain_core.messages import SystemMessage, HumanMessage


class GenerateBlogContentNode:
    """Node for generating comprehensive blog content from YouTube video transcripts."""
    
    def __init__(self, user_input: Dict[str, str]):
        """
        Initialize the blog content generator.
        
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
    
    def _validate_transcript(self, transcript: Optional[str]) -> str:
        """
        Validate the transcript data.
        
        Args:
            transcript (Optional[str]): The transcript to validate.
            
        Returns:
            str: The validated transcript.
            
        Raises:
            ValueError: If the transcript is invalid.
        """
        if not transcript:
            error_msg = "YouTube transcript is missing"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise ValueError(error_msg)
            
        return transcript
    
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
                "You are an expert blog content writer specializing in creating engaging, "
                "informative, and well-structured articles from youtube video transcript.\n\n"
                "Use only provided youtube transcript for blog generation.\n\n"
                "Guidelines for blog generation:\n"
                "1. Create clear section hierarchy with relevant subheadings\n"
                "2. Maintain consistent tone and style throughout\n"
                "3. Expand on key points with examples and context\n"
                "4. Use transitional phrases between sections\n"
                "5. Include relevant examples and explanations\n"
                "6. Optimize content for both readability and SEO\n"
                "7. Ensure each section provides unique value\n"
                "8. Write in an engaging but professional tone\n"
                "9. Use short paragraphs and clear language\n"
                "10. Add relevant context where the video may lack detail\n\n"
                "Focus on creating content that is both informative and engaging while "
                "maintaining the original message of the video.\n\n"
                "Format your response using markdown for better readability."
            )
        )
        
        human_msg = HumanMessage(
            content=(
                f"Please generate a comprehensive blog post based on this video transcript.\n\n"
                "Requirements:\n"
                "- Create an engaging introduction\n"
                "- Create clear section hierarchy with relevant subheadings (use ## for headings)\n"
                "- Write a strong conclusion\n"
                "- Add value beyond the transcript\n"
                "- Ensure smooth transitions between sections\n"
                "- Use markdown formatting for structure\n\n"
                f"Transcript:\n{transcript}\n\n"
                "Note: Don't write a title for the blog, as it's already provided separately."
            )
        )
        
        return [system_msg, human_msg]
    
    def _check_content_quality(self, content: str) -> None:
        """
        Check the quality of generated blog content.
        
        Args:
            content (str): The generated blog content.
            
        Raises:
            ValueError: If the content fails quality checks.
        """
        if not content or not content.strip():
            error_msg = "Generated blog content is empty"
            st.error(error_msg)
            raise ValueError(error_msg)
        
        # Check for minimum content length (approximately 300 words)
        if len(content.split()) < 300:
            st.warning("Generated content is shorter than expected. It might not be comprehensive enough.")
        
        # Check for markdown headings
        if "##" not in content:
            st.warning("Generated content may lack proper section headings.")
    
    def generate_blog_content_node(self, state: BlogState) -> Dict[str, str]:
        """
        Generate blog content based on the transcript in the state.
        
        Args:
            state (BlogState): The application state containing the transcript.
            
        Returns:
            Dict[str, str]: A dictionary containing the generated blog content.
            
        Raises:
            RuntimeError: If the blog content generation process fails.
        """
        try:
            transcript = state.get("youtube_transcript")
            if not transcript:
                error_msg = "YouTube transcript is missing"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise ValueError(error_msg)

            messages = self._create_messages(transcript)
            
            st.info("Starting blog content generation. This may take a few moments...")
            
            try:
                with st.spinner("Generating comprehensive blog content..."):
                    blog_content_response = self.llm.invoke(
                        input=messages,
                    )
                    
                    if not hasattr(blog_content_response, 'content'):
                        error_msg = "Unexpected response format from LLM"
                        st.error(error_msg)
                        st.code(traceback.format_exc(), language="python")
                        raise ValueError(error_msg)
                    
                    content = blog_content_response.content
                    if not content or not content.strip():
                        error_msg = "Generated blog content is empty"
                        st.error(error_msg)
                        raise ValueError(error_msg)
                    
                    st.success("Blog content generated successfully!")
                    
                    return {'blog_content': content}
                
            except Exception as e:
                error_msg = f"Blog generation failed: {str(e)}"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
                
        except Exception as e:
            error_msg = f"Blog content generation process failed: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)