import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';
import { PlayerSongCard } from './info/song/song.component';
import { PlayerLyricsComponent } from './lyrics/lyrics.component';
import { PlayerBarComponent } from "./bar/player_bar.component";
@Component({
  selector: 'app-player',
  standalone: true,
  imports: [NavbarAppComponent, PlayerSongCard, PlayerLyricsComponent, PlayerBarComponent],
  templateUrl: './player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerComponent { }
