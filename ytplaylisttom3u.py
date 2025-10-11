import requests
import xml.etree.ElementTree as ET
import re
import sys

def extract_playlist_id(url):
    """Extract playlist ID from YouTube URL."""
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube playlist URL. Could not extract playlist ID.")

def get_playlist_video_urls(playlist_id):
    """Fetch video URLs from YouTube playlist RSS feed."""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
    response = requests.get(rss_url)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    video_urls = []
    video_info = []  # List of (title, url) for m3u
    
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
        link_elem = entry.find(".//{http://www.w3.org/2005/Atom}link[@rel='alternate']")
        
        if title_elem is not None and link_elem is not None:
            title = title_elem.text or "Unknown Title"
            href = link_elem.get('href', '')
            video_id_match = re.search(r'v=([a-zA-Z0-9_-]+)', href)
            if video_id_match:
                video_id = video_id_match.group(1)
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_urls.append(video_url)
                video_info.append((title, video_url))
    
    return video_urls, video_info

def save_to_m3u(video_info, filename):
    """Save video info to .m3u file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for title, url in video_info:
            f.write(f'#EXTINF:-1,{title}\n')
            f.write(f'{url}\n')
    print(f"Saved to {filename}")

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter YouTube playlist URL: ").strip()
    
    try:
        playlist_id = extract_playlist_id(url)
        video_urls, video_info = get_playlist_video_urls(playlist_id)
        
        if not video_urls:
            print("No videos found in the playlist.")
            return
        
        print("\nVideo URLs:")
        for url in video_urls:
            print(url)
        
        save_option = input("\nSave to .m3u file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = input("Enter filename (default: playlist.m3u): ").strip()
            if not filename:
                filename = "playlist.m3u"
            if not filename.endswith('.m3u'):
                filename += '.m3u'
            save_to_m3u(video_info, filename)
        
    except ValueError as e:
        print(f"Error: {e}")
    except requests.RequestException as e:
        print(f"Error fetching playlist: {e}")
    except ET.ParseError as e:
        print(f"Error parsing RSS feed: {e}")

if __name__ == "__main__":
    main()