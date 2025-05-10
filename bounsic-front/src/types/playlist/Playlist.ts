import Song from "../Song";

interface Playlist {
    id: number;
    name: string;
    desc: string;
    updated_at: Date;
    songs: Song[];
}
export default Playlist;