import { ChangeDetectionStrategy, Component } from '@angular/core';
@Component({
  selector: 'player-bar',
  standalone: true,
  templateUrl: './player_bar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerBarComponent { }
