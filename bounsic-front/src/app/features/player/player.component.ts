import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';
import { PlayerSong } from './info/song/song.component';
import { PlayerLyricsComponent } from './lyrics/lyrics.component';
import { PlayerBarComponent } from "./bar/player-bar.component";
import { SongListComponent } from "./info/song_list/song-list.component";
@Component({
  selector: 'app-player',
  standalone: true,
  imports: [NavbarAppComponent, PlayerSong, PlayerLyricsComponent, PlayerBarComponent, SongListComponent],
  templateUrl: './player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerComponent { 
  public song = {
    mp3:"https://bounsic1imgs.blob.core.windows.net/bounsic-songs-imgs/Adele%20-%20Rolling%20in%20the%20Deep%20(Official%20Music%20Video).mp3?sp=r&st=2025-03-22T18:54:02Z&se=2025-03-23T02:54:02Z&spr=https&sv=2024-11-04&sr=b&sig=AUMA7DV6aAHGaux9MyYvWaxsWHa%2F1HmEw9I8359duuI%3D"
  }
}
