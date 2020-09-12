# Intro

A simple Pygame-based menu system: it scans folders and collects the single
image/movie pair within each folder. It then shows the collected pictures,
allowing you to navigate with up/down cursors; and when you hit ENTER,
it plays the related movie.

# Setup

The configuration of folders, resolutions, players, etc is done with a
simple 'settings.ini' file:

    VideoFolder=c:\Tmp\Videos
    FullScreen=yes
    WidthInPixels=1920
    HeightInPixels=1080
    ImageExtensions=jpg,jpeg,gif,png,webp
    MovieExtensions=mkv,mp4,flv,avi,mov,opus,mp3,wma,aac
    Command=C:\Program Files\VideoLAN\VLC\vlc.exe

The `VideoFolder` and `Command` options are mandatory; the rest have
auto-set defaults to your monitor's resolution.

# Why?

I know this is no Kodi :-) 

I built it at the request of two friends at ESTEC.
It does have two factors in its favor - it's insanely simple,
relatively fast, and it's easy to see it is respecting privacy;
there's no connections of any sort made to the web :-)
