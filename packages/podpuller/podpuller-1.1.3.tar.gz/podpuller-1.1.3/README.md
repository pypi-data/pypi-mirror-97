# podpuller

### A simple python app to sync your podcasts with RSS feeds and transfer to an external MP3 player

[![PyPI version](https://badge.fury.io/py/podpuller.svg)](https://badge.fury.io/py/podpuller)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Requirements Status](https://requires.io/github/guyhoffman/podpuller/requirements.svg?branch=main)](https://requires.io/github/guyhoffman/podpuller/requirements/?branch=main)


## Quick Start
1. `pip install podpuller`
1. Copy `feeds.example.conf` to `~/.config/podpuller/feeds.conf`
1. Put in URLs of RSS feeds, using a unique section name for each feed. No need to put in title.
1. You can now use the command `podpuller`

![podpuller screenshot](https://raw.githubusercontent.com/guyhoffman/podpuller/main/screenshot.png)

## Motivation

After giving up my smartphone and buying a cheapo MP3 player I wanted a way to keep my feeds synced. 

There are many great programs for this out there, like [Greg](https://github.com/manolomartinez/greg/), but it didn't really fit my workflow, which was having a certain number of the newest episodes of each podcast, and manually marking the ones I have already listened to. 

This is that app. It was heavily inspired (and liberally copied) from the excellent [upodder](https://github.com/m3nu/upodder) which is no longer maintained. 

## Workflow

#### Config: `~/.config/podpuller/feeds.conf`

1. Choose your RSS feeds
1. Specify how many episodes you want
1. Choose serial (oldest first) or regular + optional start date

#### Run: `podpuller [opt:single_feed]`
1. Mark the ones you listened to (or skip with "quick mode") 
1. Wait for sync (only syncs single feed if specified)
1. Optionally, transfer to external drive

### Config
The config file is read from `~/.config/podpuller/feeds.conf` and you have an example [here](https://github.com/guyhoffman/podpuller/blob/main/feeds.example.conf). It is pretty straightforward:

##### Global Configs
- `data directory`: Where to store the SQL database of downloaded and listened episodes.
- `download directory`: Where to download the podcasts to.
- `mp3 player directory`: Where to sync the download directory to. 

##### Feed Configs
- Every feed goes into a directory named by its config file section (e.g., `tal` in the sample conf file).
- The `serial` config gets episodes from oldest to newest.
- `start date` ignored everything before that date (useful for `serial` podcasts).
- There's no need to provide a name for the feed, just a URL, the name will be auto-filled from the RSS feed.

### Notes
- Sync both transfers and deletes files. It basically does an exact copy.
- All defaults, including `rsync` flags, are for MacOS but can probably be easily changed for UN*X systems.

## Rant

RSS is a long-standing open standard for updated feeds. Your podcast success is built on the shoulders of many open-source and open-format developers who poured their heart into it. Please stop making your podcast available only through proprietary channels like Spotify, iTunes, etc. Give back by also publishing your RSS feed. Thanks!

## Roadmap

- ~~Tag MP3 files with info from feed~~
- ~~Put project on PyPI~~
- ~~UI improvements~~
- ~~Handle "oldest-first" workflow for serial podcasts~~
