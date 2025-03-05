import { ChangeDetectionStrategy, Component } from '@angular/core';
@Component({
  selector: 'player-lyrics',
  standalone: true,
  templateUrl: './lyrics.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerLyricsComponent {}
