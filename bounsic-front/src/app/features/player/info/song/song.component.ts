import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import Song from 'src/types/Song';
@Component({
  selector: 'player-song',
  standalone: true,
  templateUrl: './song.component.html',
  imports:[TranslateModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerSong {
  @Input() song!: Song;
}
