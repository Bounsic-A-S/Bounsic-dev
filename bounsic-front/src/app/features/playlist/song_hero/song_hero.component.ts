import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { formatDuration } from '../utils/format-song-duration';

@Component({
  selector: 'app-song-hero',
  standalone: true,
  templateUrl: './song_hero.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SongHeroComponent {
  @Input() totalSongs!: number;
  @Input() totalDuration!: string;

  get formattedDuration(): string {
    return formatDuration(this.totalDuration)
  }
}
