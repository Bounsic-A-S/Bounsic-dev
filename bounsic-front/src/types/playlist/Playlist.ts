import Song from "../Song";

interface Playlist {
    id: number;
    title: string;
    img_url:string;
    updated_at: Date;
    songs: Song[];
}
export default Playlist;