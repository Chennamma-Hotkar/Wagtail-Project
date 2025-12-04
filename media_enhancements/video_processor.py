"""
Video Processing Module
Handles thumbnail generation, metadata extraction, trimming, and S3 upload
"""

import os
import subprocess
from datetime import timedelta
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import json
import re


class VideoProcessor:
    """
    Video processing toolkit using FFmpeg and MoviePy.
    """
    
    def __init__(self, video_path):
        """
        Initialize with video file path.
        """
        self.video_path = video_path
        self.metadata = None
    
    def extract_metadata(self):
        """
        Extract video metadata using FFprobe.
        Returns dict with duration, resolution, codecs, fps, bitrate, etc.
        """
        try:
            # Use ffprobe to get video information
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # Extract video stream info
            video_stream = next((s for s in data.get('streams', []) if s['codec_type'] == 'video'), None)
            audio_stream = next((s for s in data.get('streams', []) if s['codec_type'] == 'audio'), None)
            format_info = data.get('format', {})
            
            metadata = {
                'duration': float(format_info.get('duration', 0)),
                'duration_timedelta': timedelta(seconds=float(format_info.get('duration', 0))),
                'bitrate': int(format_info.get('bit_rate', 0)) // 1000,  # Convert to kbps
                'size': int(format_info.get('size', 0)),
            }
            
            if video_stream:
                metadata.update({
                    'width': int(video_stream.get('width', 0)),
                    'height': int(video_stream.get('height', 0)),
                    'resolution': f"{video_stream.get('width')}x{video_stream.get('height')}",
                    'codec': video_stream.get('codec_name', ''),
                    'fps': eval(video_stream.get('r_frame_rate', '0/1')),  # Convert fraction to float
                })
            
            if audio_stream:
                metadata['audio_codec'] = audio_stream.get('codec_name', '')
            
            self.metadata = metadata
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
    
    def generate_thumbnail(self, time_position='00:00:01', output_path=None):
        """
        Generate thumbnail from video at specified time position.
        
        Args:
            time_position: Time position (e.g., '00:00:01' or '5' for 5 seconds)
            output_path: Output file path (optional)
        
        Returns:
            Path to generated thumbnail or BytesIO object
        """
        try:
            # Create temporary output if no path provided
            if output_path is None:
                output_path = self.video_path.rsplit('.', 1)[0] + '_thumb.jpg'
            
            # Use ffmpeg to extract frame
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-ss', str(time_position),
                '-vframes', '1',
                '-q:v', '2',  # High quality
                '-y',  # Overwrite
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
    
    def generate_thumbnail_django(self, time_position='00:00:01'):
        """
        Generate thumbnail and return as Django ContentFile.
        
        Args:
            time_position: Time position for thumbnail
        
        Returns:
            ContentFile object
        """
        import tempfile
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Generate thumbnail
            self.generate_thumbnail(time_position, tmp_path)
            
            # Read and return as ContentFile
            with open(tmp_path, 'rb') as f:
                content = f.read()
            
            filename = os.path.basename(self.video_path).rsplit('.', 1)[0] + '_thumb.jpg'
            return ContentFile(content, name=filename)
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def generate_multiple_thumbnails(self, count=4):
        """
        Generate multiple thumbnails at different time positions.
        
        Args:
            count: Number of thumbnails to generate
        
        Returns:
            List of thumbnail paths
        """
        if not self.metadata:
            self.extract_metadata()
        
        duration = self.metadata.get('duration', 0)
        if duration == 0:
            return []
        
        thumbnails = []
        interval = duration / (count + 1)
        
        for i in range(1, count + 1):
            time_pos = interval * i
            output_path = self.video_path.rsplit('.', 1)[0] + f'_thumb_{i}.jpg'
            thumb = self.generate_thumbnail(time_pos, output_path)
            if thumb:
                thumbnails.append(thumb)
        
        return thumbnails
    
    def trim_video(self, start_time, end_time, output_path=None):
        """
        Trim video to specified time range.
        
        Args:
            start_time: Start time in seconds or 'HH:MM:SS' format
            end_time: End time in seconds or 'HH:MM:SS' format
            output_path: Output file path
        
        Returns:
            Path to trimmed video
        """
        try:
            if output_path is None:
                base, ext = os.path.splitext(self.video_path)
                output_path = f"{base}_trimmed{ext}"
            
            # Calculate duration
            if isinstance(start_time, (int, float)):
                start_time = str(timedelta(seconds=start_time))
            if isinstance(end_time, (int, float)):
                end_time = str(timedelta(seconds=end_time))
            
            # Use ffmpeg to trim
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-ss', start_time,
                '-to', end_time,
                '-c', 'copy',  # Copy codec (fast, no re-encoding)
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            print(f"Error trimming video: {e}")
            return None
    
    def compress_video(self, output_path=None, crf=23, preset='medium'):
        """
        Compress video using H.264 codec.
        
        Args:
            output_path: Output file path
            crf: Constant Rate Factor (18-28, lower = better quality)
            preset: Encoding preset (ultrafast, fast, medium, slow, veryslow)
        
        Returns:
            Path to compressed video
        """
        try:
            if output_path is None:
                base, ext = os.path.splitext(self.video_path)
                output_path = f"{base}_compressed.mp4"
            
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-c:v', 'libx264',
                '-crf', str(crf),
                '-preset', preset,
                '-c:a', 'aac',
                '-b:a', '128k',
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            print(f"Error compressing video: {e}")
            return None
    
    def convert_to_web_format(self, output_path=None):
        """
        Convert video to web-optimized MP4 format.
        
        Args:
            output_path: Output file path
        
        Returns:
            Path to converted video
        """
        try:
            if output_path is None:
                base = os.path.splitext(self.video_path)[0]
                output_path = f"{base}_web.mp4"
            
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-c:v', 'libx264',
                '-profile:v', 'main',
                '-level', '4.0',
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-movflags', '+faststart',  # Enable streaming
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            print(f"Error converting video: {e}")
            return None
    
    def extract_audio(self, output_path=None):
        """
        Extract audio track from video.
        
        Args:
            output_path: Output file path
        
        Returns:
            Path to extracted audio
        """
        try:
            if output_path is None:
                base = os.path.splitext(self.video_path)[0]
                output_path = f"{base}_audio.mp3"
            
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-q:a', '2',  # High quality
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def create_gif(self, start_time=0, duration=3, output_path=None, fps=10, width=480):
        """
        Create animated GIF from video segment.
        
        Args:
            start_time: Start time in seconds
            duration: Duration in seconds
            output_path: Output file path
            fps: Frames per second for GIF
            width: Width of GIF (height auto-calculated)
        
        Returns:
            Path to created GIF
        """
        try:
            if output_path is None:
                base = os.path.splitext(self.video_path)[0]
                output_path = f"{base}.gif"
            
            cmd = [
                'ffmpeg',
                '-ss', str(start_time),
                '-t', str(duration),
                '-i', self.video_path,
                '-vf', f'fps={fps},scale={width}:-1:flags=lanczos',
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            print(f"Error creating GIF: {e}")
            return None


class S3VideoUploader:
    """
    Upload videos to S3 and configure CloudFront.
    """
    
    def __init__(self, bucket_name=None, cloudfront_domain=None):
        """
        Initialize S3 uploader.
        
        Args:
            bucket_name: S3 bucket name
            cloudfront_domain: CloudFront distribution domain
        """
        import boto3
        from django.conf import settings
        
        self.bucket_name = bucket_name or settings.AWS_STORAGE_BUCKET_NAME
        self.cloudfront_domain = cloudfront_domain or getattr(settings, 'CLOUDFRONT_DOMAIN', None)
        self.s3_client = boto3.client('s3')
    
    def upload_video(self, file_path, s3_key=None):
        """
        Upload video to S3.
        
        Args:
            file_path: Local file path
            s3_key: S3 object key (path in bucket)
        
        Returns:
            Dict with s3_url and cloudfront_url
        """
        try:
            if s3_key is None:
                s3_key = f"videos/{os.path.basename(file_path)}"
            
            # Upload file
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': 'video/mp4',
                    'CacheControl': 'max-age=31536000',  # 1 year
                }
            )
            
            # Generate URLs
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            cloudfront_url = None
            
            if self.cloudfront_domain:
                cloudfront_url = f"https://{self.cloudfront_domain}/{s3_key}"
            
            return {
                's3_key': s3_key,
                's3_url': s3_url,
                'cloudfront_url': cloudfront_url
            }
            
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return None


class RemoteVideoEmbedder:
    """
    Handle remote video embedding (YouTube, Vimeo).
    """
    
    @staticmethod
    def extract_youtube_id(url):
        """Extract YouTube video ID from URL."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def extract_vimeo_id(url):
        """Extract Vimeo video ID from URL."""
        pattern = r'vimeo\.com\/(\d+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def get_youtube_embed_code(video_id, width=560, height=315):
        """Generate YouTube embed code."""
        return f'''<iframe width="{width}" height="{height}" 
src="https://www.youtube.com/embed/{video_id}" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen></iframe>'''
    
    @staticmethod
    def get_vimeo_embed_code(video_id, width=640, height=360):
        """Generate Vimeo embed code."""
        return f'''<iframe src="https://player.vimeo.com/video/{video_id}" 
width="{width}" height="{height}" 
frameborder="0" 
allow="autoplay; fullscreen; picture-in-picture" 
allowfullscreen></iframe>'''
    
    @staticmethod
    def get_youtube_thumbnail(video_id):
        """Get YouTube thumbnail URL."""
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    @staticmethod
    def get_vimeo_thumbnail(video_id):
        """Get Vimeo thumbnail URL."""
        import requests
        try:
            response = requests.get(f"https://vimeo.com/api/v2/video/{video_id}.json")
            data = response.json()
            return data[0]['thumbnail_large']
        except:
            return None


# Convenience functions

def process_uploaded_video(video_instance):
    """
    Process newly uploaded video: extract metadata and generate thumbnail.
    
    Args:
        video_instance: Video model instance
    """
    if video_instance.video_type == 'local' and video_instance.file:
        processor = VideoProcessor(video_instance.file.path)
        
        # Extract metadata
        metadata = processor.extract_metadata()
        if metadata:
            video_instance.duration_seconds = int(metadata.get('duration', 0))
            video_instance.duration = metadata.get('duration_timedelta')
            video_instance.width = metadata.get('width')
            video_instance.height = metadata.get('height')
            video_instance.resolution = metadata.get('resolution')
            video_instance.fps = metadata.get('fps')
            video_instance.bitrate = metadata.get('bitrate')
            video_instance.codec = metadata.get('codec')
            video_instance.audio_codec = metadata.get('audio_codec')
        
        # Generate thumbnail if not exists
        if not video_instance.thumbnail:
            thumb_file = processor.generate_thumbnail_django()
            if thumb_file:
                video_instance.thumbnail.save(thumb_file.name, thumb_file, save=False)
                video_instance.thumbnail_auto_generated = True
        
        video_instance.save()
    
    elif video_instance.video_type in ['youtube', 'vimeo'] and video_instance.remote_url:
        embedder = RemoteVideoEmbedder()
        
        if video_instance.video_type == 'youtube':
            video_id = embedder.extract_youtube_id(video_instance.remote_url)
            if video_id:
                video_instance.embed_code = embedder.get_youtube_embed_code(video_id)
                # Optionally download thumbnail
                if not video_instance.thumbnail:
                    thumb_url = embedder.get_youtube_thumbnail(video_id)
                    # Download and save thumbnail
        
        elif video_instance.video_type == 'vimeo':
            video_id = embedder.extract_vimeo_id(video_instance.remote_url)
            if video_id:
                video_instance.embed_code = embedder.get_vimeo_embed_code(video_id)
                # Optionally download thumbnail
                if not video_instance.thumbnail:
                    thumb_url = embedder.get_vimeo_thumbnail(video_id)
                    # Download and save thumbnail
        
        video_instance.save()
