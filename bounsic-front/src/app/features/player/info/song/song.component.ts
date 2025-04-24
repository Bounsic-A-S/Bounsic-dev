import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import Song from 'src/types/Song';
@Component({
  selector: 'player-song',
  standalone: true,
  templateUrl: './song.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerSong {
  @Input() song!: Song;
}
