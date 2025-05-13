import Song from "../Song";

interface Playlist {
    id: string;
    title: string;
    img_url: string;
    isPublic: boolean;
    updated_at: Date;
    songs: Song[];
}
export default Playlist;