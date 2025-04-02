import streamlit as st
import traceback
from typing import Dict, Optional
from src.youtube_assistant.state import BlogState


class BlogAggregatorNode:
    """
    Class for aggregating blog components into a final formatted blog.
    Combines title and content with proper formatting.
    """
    
    def __init__(self):
        """Initialize the BlogAggregatorNode."""
        pass
    
        
    def _format_blog(self, title: str, content: str) -> str:
        """
        Format blog title and content into final blog.
        
        Args:
            title (str): The validated blog title.
            content (str): The validated blog content.
            
        Returns:
            str: The formatted final blog.
        """
        # Remove any existing title formats from content to avoid duplicates
        if content.startswith("# ") or content.startswith("#"):
            content_lines = content.split("\n")
            # Skip the first line if it looks like a title
            if content_lines[0].startswith("# ") or content_lines[0].startswith("#"):
                content = "\n".join(content_lines[1:])
        
        # Check if content already has blank lines at the start
        if not content.startswith("\n\n"):
            # Ensure proper spacing between title and content
            return f"# {title}\n\n{content}"
        else:
            return f"# {title}{content}"
    
    def aggregate_blog_node(self, state: BlogState) -> Dict[str, str]:
        """
        Combine blog title and content into final formatted blog.
        
        Args:
            state (BlogState): The application state containing blog title and content.
            
        Returns:
            Dict[str, str]: A dictionary containing the final formatted blog.
            
        Raises:
            RuntimeError: If the blog aggregation process fails.
        """
        try:
            blog_title = state.get('blog_title')
            blog_content = state.get('blog_content')

            if not blog_title:
                error_msg = "Blog title is missing"
                st.error(error_msg)
                raise ValueError(error_msg)
            
            if not blog_content:
                error_msg = "Blog content is missing"
                st.error(error_msg)
                raise ValueError(error_msg)
            
            with st.spinner("Formatting final blog..."):
                final_blog = self._format_blog(blog_title, blog_content)
                
                if not final_blog.strip():
                    error_msg = "Generated final blog is empty"
                    st.error(error_msg)
                    raise ValueError(error_msg)
                
                return {'final_blog': final_blog}
                
        except Exception as e:
            error_msg = f"Failed to aggregate blog: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)