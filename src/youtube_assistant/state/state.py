from typing_extensions import TypedDict
from typing import Optional


class BlogState(TypedDict):
    youtube_url: str
    youtube_transcript: str
    
    blog_title: str
    blog_content: str
    final_blog: str

    video_notes: str

    video_summary: str
    