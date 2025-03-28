import yt_dlp

def download_clip():
    ydl_opts = {
        'format': '311',
        'merge_output_format': 'mp4',
        'download_sections': "*13:00-17:00",
        'outtmpl': 'MC_Parkour.mp4'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=u7kdVe8q5zs"])

if __name__ == '__main__':
    download_clip()