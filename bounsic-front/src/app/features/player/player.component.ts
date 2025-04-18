import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { PlayerSong } from './info/song/song.component';
import { PlayerLyricsComponent } from './lyrics/lyrics.component';
import { SongListComponent } from "./info/song_list/song-list.component";
import { PlayerMusicComponent } from "./music/music-player.component";
@Component({
  selector: 'app-player',
  standalone: true,
  imports: [NavbarAppComponent, PlayerSong, PlayerLyricsComponent, PlayerMusicComponent, SongListComponent],
  templateUrl: './player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerComponent { 
  public song = {
    mp3:"https://bounsic1imgs.blob.core.windows.net/bounsic-songs-imgs/Taylor Swift - Lover (Official Music Video).mp3"
  }
}
