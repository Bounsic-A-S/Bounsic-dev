import Playlist from "./Playlist";

interface PlaylistDetail extends Playlist {
    totalSongs: number;
    totalDuration: number;
  }

  export default PlaylistDetail;