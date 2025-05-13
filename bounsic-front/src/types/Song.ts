interface Song {
    _id: string;
    artist: string;
    title: string;
    album: string;
    img_url: string;
    mp3_url: string;
    release_year: number;
    genres: { genre: string }[];
    fingerprint: any[];
    lyrics?:string;
    isLiked?:boolean;
    duration?:number;
}
export default Song;