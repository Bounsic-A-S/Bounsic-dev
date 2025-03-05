import { ChangeDetectionStrategy, Component } from '@angular/core';
@Component({
  selector: 'player-song-card',
  standalone: true,
  templateUrl: './song.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerSongCard {}
