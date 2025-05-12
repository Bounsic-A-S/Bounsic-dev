import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { formatDuration } from '../utils/format-song-duration';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-song-hero',
  standalone: true,
  templateUrl: './song_hero.component.html',
  imports: [TranslateModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SongHeroComponent {
  @Input() totalSongs!: number;
  @Input() totalDuration!: number;
  @Input() updatedDate!: Date;
  @Input() isPublic!: boolean;
  @Input() img_url!: string;

  get formattedDuration(): string {
    return formatDuration(this.totalDuration)
  }
  get playlistStatus(): string {
    return this.isPublic ? "Public" : "Private" //had to change in i18n
  }
  get formattedTime(): string {
    return new Date(this.updatedDate).toLocaleString()
  }
}
