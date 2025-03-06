import { ChangeDetectionStrategy, Component } from '@angular/core';
@Component({
  selector: 'player-song',
  standalone: true,
  templateUrl: './song.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerSong {}
