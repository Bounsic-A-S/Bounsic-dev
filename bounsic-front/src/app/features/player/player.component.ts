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
export class PlayerComponent { }
