function run() {
	const itunes = Application('iTunes')
	const music = itunes.playlists[1];
	const tracks = music.tracks.properties();
	return JSON.stringify(tracks);
}

<!--使い方

osascript - l JavaScript - e "Application('iTunes').playlists.name()"
osascript - l JavaScript getAllTracks.js > tracks.json

-->