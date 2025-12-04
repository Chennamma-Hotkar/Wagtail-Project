"""
Audio Processing Module
Handles waveform generation, metadata extraction, trimming, and audio manipulation
"""

import os
import subprocess
from datetime import timedelta
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import json
import numpy as np


class AudioProcessor:
    """
    Audio processing toolkit using FFmpeg, Pydub, and Librosa.
    """
    
    def __init__(self, audio_path):
        """
        Initialize with audio file path.
        """
        self.audio_path = audio_path
        self.metadata = None
        self.audio_data = None
        self.sample_rate = None
    
    def extract_metadata(self):
        """
        Extract audio metadata using FFprobe and Mutagen.
        Returns dict with duration, bitrate, sample rate, codec, etc.
        """
        try:
            # Use ffprobe to get audio information
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # Extract audio stream info
            audio_stream = next((s for s in data.get('streams', []) if s['codec_type'] == 'audio'), None)
            format_info = data.get('format', {})
            
            metadata = {
                'duration': float(format_info.get('duration', 0)),
                'duration_timedelta': timedelta(seconds=float(format_info.get('duration', 0))),
                'bitrate': int(format_info.get('bit_rate', 0)) // 1000,  # Convert to kbps
                'size': int(format_info.get('size', 0)),
            }
            
            if audio_stream:
                metadata.update({
                    'codec': audio_stream.get('codec_name', ''),
                    'sample_rate': int(audio_stream.get('sample_rate', 0)),
                    'channels': int(audio_stream.get('channels', 0)),
                    'channel_layout': audio_stream.get('channel_layout', ''),
                })
            
            # Try to extract ID3 tags using mutagen
            try:
                from mutagen import File
                audio_file = File(self.audio_path)
                
                if audio_file:
                    tags = {}
                    
                    # Common tag mappings
                    tag_mappings = {
                        'title': ['TIT2', 'title', '\xa9nam'],
                        'artist': ['TPE1', 'artist', '\xa9ART'],
                        'album': ['TALB', 'album', '\xa9alb'],
                        'album_artist': ['TPE2', 'albumartist', 'aART'],
                        'genre': ['TCON', 'genre', '\xa9gen'],
                        'year': ['TDRC', 'date', '\xa9day'],
                        'track_number': ['TRCK', 'tracknumber', 'trkn'],
                        'disc_number': ['TPOS', 'discnumber', 'disk'],
                        'composer': ['TCOM', 'composer', '\xa9wrt'],
                        'copyright': ['TCOP', 'copyright', 'cprt'],
                    }
                    
                    for key, tag_names in tag_mappings.items():
                        for tag_name in tag_names:
                            if tag_name in audio_file:
                                value = audio_file[tag_name]
                                if isinstance(value, list):
                                    value = value[0]
                                tags[key] = str(value)
                                break
                    
                    metadata['tags'] = tags
            
            except Exception as e:
                print(f"Error extracting ID3 tags: {e}")
            
            self.metadata = metadata
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
    
    def load_audio_data(self):
        """
        Load audio data using librosa for analysis.
        """
        try:
            import librosa
            
            # Load audio file
            self.audio_data, self.sample_rate = librosa.load(self.audio_path, sr=None)
            
            return self.audio_data, self.sample_rate
            
        except Exception as e:
            print(f"Error loading audio data: {e}")
            return None, None
    
    def generate_waveform_image(self, width=1200, height=200, color='#667eea', output_path=None):
        """
        Generate waveform visualization image.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            color: Waveform color (hex)
            output_path: Output file path (optional)
        
        Returns:
            Path to generated waveform image
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            import librosa
            import librosa.display
            
            # Load audio if not already loaded
            if self.audio_data is None:
                self.load_audio_data()
            
            if self.audio_data is None:
                return None
            
            # Create figure
            fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
            
            # Plot waveform
            librosa.display.waveshow(self.audio_data, sr=self.sample_rate, ax=ax, color=color)
            
            # Remove axes and margins
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            # Set background color
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            
            # Tight layout
            plt.tight_layout(pad=0)
            
            # Save
            if output_path is None:
                output_path = self.audio_path.rsplit('.', 1)[0] + '_waveform.png'
            
            plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='white')
            plt.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error generating waveform image: {e}")
            return None
    
    def generate_waveform_django(self, width=1200, height=200, color='#667eea'):
        """
        Generate waveform and return as Django ContentFile.
        
        Returns:
            ContentFile object
        """
        import tempfile
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Generate waveform
            self.generate_waveform_image(width, height, color, tmp_path)
            
            # Read and return as ContentFile
            with open(tmp_path, 'rb') as f:
                content = f.read()
            
            filename = os.path.basename(self.audio_path).rsplit('.', 1)[0] + '_waveform.png'
            return ContentFile(content, name=filename)
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def generate_waveform_data(self, samples=1000):
        """
        Generate waveform data for web visualization.
        
        Args:
            samples: Number of data points
        
        Returns:
            List of amplitude values
        """
        try:
            import librosa
            
            # Load audio if not already loaded
            if self.audio_data is None:
                self.load_audio_data()
            
            if self.audio_data is None:
                return []
            
            # Downsample to desired number of samples
            step = len(self.audio_data) // samples
            if step < 1:
                step = 1
            
            waveform_data = []
            for i in range(0, len(self.audio_data), step):
                chunk = self.audio_data[i:i+step]
                if len(chunk) > 0:
                    # Get RMS (root mean square) for this chunk
                    rms = np.sqrt(np.mean(chunk**2))
                    waveform_data.append(float(rms))
            
            # Normalize to 0-1 range
            if waveform_data:
                max_val = max(waveform_data)
                if max_val > 0:
                    waveform_data = [v / max_val for v in waveform_data]
            
            return waveform_data
            
        except Exception as e:
            print(f"Error generating waveform data: {e}")
            return []
    
    def trim_audio(self, start_time, end_time, output_path=None):
        """
        Trim audio to specified time range.
        
        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output file path
        
        Returns:
            Path to trimmed audio
        """
        try:
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(self.audio_path)
            
            # Convert to milliseconds
            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000)
            
            # Trim
            trimmed = audio[start_ms:end_ms]
            
            # Export
            if output_path is None:
                base, ext = os.path.splitext(self.audio_path)
                output_path = f"{base}_trimmed{ext}"
            
            # Determine format from extension
            format_map = {
                '.mp3': 'mp3',
                '.wav': 'wav',
                '.ogg': 'ogg',
                '.flac': 'flac',
                '.m4a': 'mp4',
            }
            
            ext = os.path.splitext(output_path)[1].lower()
            audio_format = format_map.get(ext, 'mp3')
            
            trimmed.export(output_path, format=audio_format)
            
            return output_path
            
        except Exception as e:
            print(f"Error trimming audio: {e}")
            return None
    
    def convert_format(self, output_format='mp3', bitrate='192k', output_path=None):
        """
        Convert audio to different format.
        
        Args:
            output_format: Target format (mp3, wav, ogg, flac, m4a)
            bitrate: Bitrate for lossy formats
            output_path: Output file path
        
        Returns:
            Path to converted audio
        """
        try:
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(self.audio_path)
            
            # Set output path
            if output_path is None:
                base = os.path.splitext(self.audio_path)[0]
                output_path = f"{base}.{output_format}"
            
            # Export with specified format and bitrate
            audio.export(output_path, format=output_format, bitrate=bitrate)
            
            return output_path
            
        except Exception as e:
            print(f"Error converting audio: {e}")
            return None
    
    def normalize_audio(self, target_dBFS=-20.0, output_path=None):
        """
        Normalize audio volume.
        
        Args:
            target_dBFS: Target loudness in dBFS
            output_path: Output file path
        
        Returns:
            Path to normalized audio
        """
        try:
            from pydub import AudioSegment
            from pydub.effects import normalize
            
            # Load audio
            audio = AudioSegment.from_file(self.audio_path)
            
            # Normalize
            normalized = normalize(audio)
            
            # Adjust to target dBFS
            change_in_dBFS = target_dBFS - normalized.dBFS
            normalized = normalized.apply_gain(change_in_dBFS)
            
            # Export
            if output_path is None:
                base, ext = os.path.splitext(self.audio_path)
                output_path = f"{base}_normalized{ext}"
            
            ext = os.path.splitext(output_path)[1].lower()
            format_map = {
                '.mp3': 'mp3',
                '.wav': 'wav',
                '.ogg': 'ogg',
                '.flac': 'flac',
                '.m4a': 'mp4',
            }
            audio_format = format_map.get(ext, 'mp3')
            
            normalized.export(output_path, format=audio_format)
            
            return output_path
            
        except Exception as e:
            print(f"Error normalizing audio: {e}")
            return None
    
    def fade_in_out(self, fade_in_duration=1000, fade_out_duration=1000, output_path=None):
        """
        Apply fade in and fade out effects.
        
        Args:
            fade_in_duration: Fade in duration in milliseconds
            fade_out_duration: Fade out duration in milliseconds
            output_path: Output file path
        
        Returns:
            Path to processed audio
        """
        try:
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(self.audio_path)
            
            # Apply fades
            audio = audio.fade_in(fade_in_duration).fade_out(fade_out_duration)
            
            # Export
            if output_path is None:
                base, ext = os.path.splitext(self.audio_path)
                output_path = f"{base}_faded{ext}"
            
            ext = os.path.splitext(output_path)[1].lower()
            format_map = {
                '.mp3': 'mp3',
                '.wav': 'wav',
                '.ogg': 'ogg',
                '.flac': 'flac',
                '.m4a': 'mp4',
            }
            audio_format = format_map.get(ext, 'mp3')
            
            audio.export(output_path, format=audio_format)
            
            return output_path
            
        except Exception as e:
            print(f"Error applying fades: {e}")
            return None
    
    def change_speed(self, speed=1.0, output_path=None):
        """
        Change audio playback speed.
        
        Args:
            speed: Speed multiplier (0.5 = half speed, 2.0 = double speed)
            output_path: Output file path
        
        Returns:
            Path to processed audio
        """
        try:
            from pydub import AudioSegment
            from pydub.effects import speedup
            
            # Load audio
            audio = AudioSegment.from_file(self.audio_path)
            
            # Change speed
            if speed != 1.0:
                audio = speedup(audio, playback_speed=speed)
            
            # Export
            if output_path is None:
                base, ext = os.path.splitext(self.audio_path)
                output_path = f"{base}_speed{speed}{ext}"
            
            ext = os.path.splitext(output_path)[1].lower()
            format_map = {
                '.mp3': 'mp3',
                '.wav': 'wav',
                '.ogg': 'ogg',
                '.flac': 'flac',
                '.m4a': 'mp4',
            }
            audio_format = format_map.get(ext, 'mp3')
            
            audio.export(output_path, format=audio_format)
            
            return output_path
            
        except Exception as e:
            print(f"Error changing speed: {e}")
            return None
    
    def extract_segment(self, start_time, duration, output_path=None):
        """
        Extract a segment of audio.
        
        Args:
            start_time: Start time in seconds
            duration: Duration in seconds
            output_path: Output file path
        
        Returns:
            Path to extracted segment
        """
        end_time = start_time + duration
        return self.trim_audio(start_time, end_time, output_path)
    
    def get_audio_info(self):
        """
        Get comprehensive audio information.
        
        Returns:
            Dict with all audio properties
        """
        if not self.metadata:
            self.extract_metadata()
        
        return self.metadata


# Convenience functions

def process_uploaded_audio(audio_instance):
    """
    Process newly uploaded audio: extract metadata and generate waveform.
    
    Args:
        audio_instance: Audio model instance
    """
    if audio_instance.file:
        processor = AudioProcessor(audio_instance.file.path)
        
        # Extract metadata
        metadata = processor.extract_metadata()
        if metadata:
            audio_instance.duration_seconds = metadata.get('duration', 0)
            audio_instance.duration = metadata.get('duration_timedelta')
            audio_instance.bitrate = metadata.get('bitrate')
            audio_instance.sample_rate = metadata.get('sample_rate')
            audio_instance.channels = metadata.get('channels')
            audio_instance.codec = metadata.get('codec')
            
            # Extract ID3 tags if available
            tags = metadata.get('tags', {})
            if tags:
                if 'title' in tags and not audio_instance.title:
                    audio_instance.title = tags['title']
                if 'artist' in tags:
                    audio_instance.artist = tags['artist']
                if 'album' in tags:
                    audio_instance.album = tags['album']
                if 'album_artist' in tags:
                    audio_instance.album_artist = tags['album_artist']
                if 'genre' in tags:
                    audio_instance.genre = tags['genre']
                if 'year' in tags:
                    try:
                        audio_instance.year = int(tags['year'][:4])
                    except:
                        pass
                if 'track_number' in tags:
                    try:
                        # Handle "1/12" format
                        track = tags['track_number'].split('/')[0]
                        audio_instance.track_number = int(track)
                    except:
                        pass
                if 'composer' in tags:
                    audio_instance.composer = tags['composer']
                if 'copyright' in tags:
                    audio_instance.copyright_holder = tags['copyright']
            
            audio_instance.metadata_extracted = True
        
        # Generate waveform if not exists
        if not audio_instance.waveform_image:
            try:
                waveform_file = processor.generate_waveform_django()
                if waveform_file:
                    audio_instance.waveform_image.save(waveform_file.name, waveform_file, save=False)
                    audio_instance.waveform_generated = True
            except Exception as e:
                print(f"Error generating waveform: {e}")
        
        # Generate waveform data for web player
        if not audio_instance.waveform_data:
            try:
                waveform_data = processor.generate_waveform_data(samples=1000)
                if waveform_data:
                    audio_instance.waveform_data = waveform_data
            except Exception as e:
                print(f"Error generating waveform data: {e}")
        
        audio_instance.save()


def generate_waveform_for_audio(audio_instance):
    """
    Generate waveform for existing audio instance.
    
    Args:
        audio_instance: Audio model instance
    """
    if audio_instance.file:
        processor = AudioProcessor(audio_instance.file.path)
        
        # Generate waveform image
        waveform_file = processor.generate_waveform_django()
        if waveform_file:
            audio_instance.waveform_image.save(waveform_file.name, waveform_file, save=False)
            audio_instance.waveform_generated = True
        
        # Generate waveform data
        waveform_data = processor.generate_waveform_data(samples=1000)
        if waveform_data:
            audio_instance.waveform_data = waveform_data
        
        audio_instance.save()
