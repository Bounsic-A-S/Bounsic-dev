import { Component } from "@angular/core"
import { CommonModule } from "@angular/common"
import { PlayerSongCardUi, Song} from "./card/song-card.component"

@Component({
  selector: "player-song-list",
  standalone: true,
  imports: [CommonModule, PlayerSongCardUi],
  templateUrl: "./song-list.component.html"
})
export class SongListComponent {
  songs: Song[] = [
    {
      id: "1",
      title: "Only In My Dreams",
      artist: "The Marias",
      coverUrl: "https://i.pinimg.com/736x/82/12/b3/8212b3248d1df1d735de892fe8440508.jpg",
    },
    {
      id: "2",
      title: "Lo Que Siento",
      artist: "Cuco",
      coverUrl: "https://i.pinimg.com/736x/25/34/43/253443b4e5ca530ec19420828c856315.jpg",
    },
    {
      id: "3",
      title: "Space Song",
      artist: "Beach House",
      coverUrl: "https://i.pinimg.com/736x/08/18/36/0818361884512ab1e204103f71ee8dd2.jpg",
    },
  ]

  playSong(song: Song): void {
    console.log(`Playing: ${song.title} by ${song.artist}`)
    // Implement actual playback logic here
  }
}

