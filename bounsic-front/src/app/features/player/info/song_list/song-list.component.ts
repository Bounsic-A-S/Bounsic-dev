import { Component, inject, Input, OnChanges, SimpleChanges } from "@angular/core"
import { CommonModule } from "@angular/common"
import { PlayerSongCardUi } from "./card/song-card.component"
import { SongService } from "@app/services/song.service"
import DashboardSong from "src/types/dashboard/DashboardSong"

@Component({
  selector: "player-song-list",
  standalone: true,
  imports: [CommonModule, PlayerSongCardUi],
  templateUrl: "./song-list.component.html"
})
export class SongListComponent implements OnChanges {
  private songService = inject(SongService)
  @Input() song_id!: string
  songs: DashboardSong[] | null = null

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['song_id'] && this.song_id) {
      this.songService.getPlayerQueue(this.song_id).subscribe({
        next: (res: DashboardSong[]) => {
          this.songs = res;
          console.log("Canciones obtenidas:", this.songs);
        },
        error: (err) => {
          console.error("Error al obtener canciones:", err);
        }
      });
    }
  }
}

