from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable
)
import re
import streamlit as st
import traceback
from src.youtube_assistant.state import BlogState


class TranscriptNode:
    """Class for extracting and processing YouTube video transcripts."""
    
    def _extract_video_id(self, url: str) -> str:
        """
        Extract the video ID from a YouTube URL.
        
        Args:
            url (str): The YouTube URL.
            
        Returns:
            str: The extracted video ID.
            
        Raises:
            ValueError: If the URL format is invalid or extraction fails.
        """
        try:
            if not url:
                error_msg = "YouTube URL is missing"
                st.error(error_msg)
                raise ValueError(error_msg)
                
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            
            parsed_url = urlparse(url)
            if 'youtube.com' in parsed_url.netloc:
                if '/watch' in parsed_url.path:
                    return parse_qs(parsed_url.query)['v'][0]
                elif '/embed/' in parsed_url.path or '/v/' in parsed_url.path:
                    return parsed_url.path.split('/')[-1]
                
            raise ValueError("Invalid YouTube URL format")
            
        except Exception as e:
            error_msg = f"Failed to extract video ID: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise ValueError(error_msg)

    def _clean_transcript_text(self, text: str) -> str:
        """
        Clean transcript text by removing unnecessary characters and formatting.
        
        Args:
            text (str): The transcript text to clean.
            
        Returns:
            str: The cleaned transcript text.
        """
        if not text:
            return ""
            
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text
    
    def get_transcript_node(self, state: BlogState) -> dict:
        """
        Extract and process the transcript for a YouTube video.
        
        Args:
            state (BlogState): The application state containing the YouTube URL.
            
        Returns:
            dict: A dictionary containing the cleaned transcript.
            
        Raises:
            RuntimeError: If the transcript extraction process fails.
        """
        try:
            url = state.get('youtube_url')
            if not url:
                error_msg = "YouTube URL is missing from state"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise ValueError(error_msg)

            video_id = self._extract_video_id(url)
            
            try:
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id=video_id,
                    languages=['en', 'en-US', 'en-GB'] 
                )
                
                content = "\n".join(subtitle.get('text', '').strip() 
                                   for subtitle in transcript 
                                   if subtitle.get('text'))
                
                cleaned_content = self._clean_transcript_text(content)
                
                if not cleaned_content:
                    error_msg = "Empty transcript after processing"
                    st.error(error_msg)
                    raise ValueError(error_msg)
                    
                return {'youtube_transcript': cleaned_content}
                
            except NoTranscriptFound:
                error_msg = "No transcript available for this video"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
            except TranscriptsDisabled:
                error_msg = "Transcripts are disabled for this video"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
            except VideoUnavailable:
                error_msg = "Video is unavailable or private"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
            except Exception as e:
                error_msg = f"Failed to extract transcript: {str(e)}"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
                
        except Exception as e:
            error_msg = f"Transcript extraction process failed: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)