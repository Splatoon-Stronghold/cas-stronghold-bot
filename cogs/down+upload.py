

from pytube import YouTube
from datetime import datetime
import moviepy.editor as mpe
from pathlib import Path
import re
import os


from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

def download_vid(link : str, folder_path : Path): 
		'''
		download_vid
		----------
		Parameters
		link : str
				The link to the youtube video to be downloaded
		folder_path : pathlib.Path
				The path to the folder in which the file should be downloaded
		-------
		Returns
		final_path : pathlib.Path
				The path to the final file which was requested to be downloaded
		'''
		yt = YouTube(link)
		streams = yt.streams.order_by('resolution') # This is lowest to highest
		vid_stream = streams[-1] # Gets the highest resolution one, since it is at the end
		aud_stream = yt.streams.get_audio_only() # Just the separate audio file

		fps = vid_stream.fps

		res = float(re.sub("[^0-9]", "", vid_stream.resolution)) # The re.sub removes all characters that aren't numbers (Ex. 720p --> 720)

		kbitrate = float(re.sub("[^0-9]", "",aud_stream.abr)) # The re.sub removes all characters that aren't numbers (Ex. 128kbps --> 128)
		bpf = (kbitrate * 1000)/fps

		# Custom filename

		vid_filename = "_".join(['vid' + vid_stream.title + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.mp4']) # Creates a filename in the format of "[youtube video title]_[date in ymdhms]_.mp4 Ex. Playing A Guitar_2022-12-26 21:20:35_.mp4"
		aud_filename = "_".join(['aud' + aud_stream.title + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.wav']) # Creates a filename in the format of "[youtube video title]_[date in ymdhms]_.wav Ex. Playing A Guitar_2022-12-26 21:20:35_.wav"

		vid_path = vid_stream.download(folder_path, vid_filename)
		aud_path = aud_stream.download(folder_path, aud_filename)

		vid = mpe.VideoFileClip(vid_path)
		aud = mpe.AudioFileClip(aud_path)

		final_path = folder_path / f'final_{vid_stream.title}_{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.mp4'
		video = vid.set_audio(aud)
		video.write_videofile(str(final_path),fps=int(fps), audio=aud_path, codec='mpeg4')
		video.close()

		os.remove(vid_path)
		os.remove(aud_path)
		return final_path

def upload_vid(vid_path : Path, thumbnail_path : Path, title : str, description : str, tags : [str], privacy : str, client_secrets_path : Path, login_storage_path : Path):
	'''
	upload_vid - Uploads local videos to YouTube
	----------
	Parameters
	vid_path : Pathlib.Path
		The Path to the local video to be uploaded
	thumbnail_path : Pathlib.Path
		The path to the image which should be used as the thumbnail
	title : str
		The title of the YouTube Video
	description : str
		The description of the Youtube Video
	tags : [str]
		The tags that the video should have. 
	privacy : str
		Privacy status of the video (private, unlisted, public)
	client_secrets_path : Pathlib.Path
		The path to the client_secret.json file from the Google Youtube API. 
	login_storage_path : Pathlib.Path
		Path to the stored login information - this is used to store the login information without having to sign in again, also useful when you can't login from where this code will be run. 
	Returns
	-------
	video_link : str
		The link to the final youtube video
	'''
	privacy_options = ['private', 'unlisted', 'public']
	if privacy not in privacy_options:
		raise ValueError(f'Error - privacy cannot be \"{privacy}\" it must be {", or ".join(privacy_options)}.')
	base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
	channel = Channel()
	channel.login(client_secrets_path, login_storage_path)

	vid = LocalVideo(file_path=vid_path, title=title, description=description, tags=tags, category='gaming')

	vid.set_embeddable(True)
	vid.set_privacy_status(privacy)
	yt_vid = channel.upload_video(vid)

	return f'https://www.youtube.com/watch?v={yt_vid.id}'


