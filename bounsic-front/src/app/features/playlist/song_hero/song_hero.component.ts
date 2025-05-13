import { ChangeDetectionStrategy, Component, inject, Input } from '@angular/core';
import { formatDuration } from '../utils/format-song-duration';
import { TranslateModule, TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-song-hero',
  standalone: true,
  templateUrl: './song_hero.component.html',
  imports: [TranslateModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SongHeroComponent {
  private translateService = inject(TranslateService)

  @Input() totalSongs!: number;
  @Input() totalDuration!: number;
  @Input() updatedDate!: Date;
  @Input() isPublic!: boolean;
  @Input() img_url!: string;

  get formattedDuration(): string {
    return formatDuration(this.totalDuration)
  }
  get playlistStatus(): string {
    return this.isPublic ? this.translateService.instant('BOUNSIC.PLAYLIST.PRIVACY.PUBLIC') : this.translateService.instant('BOUNSIC.PLAYLIST.PRIVACY.PRIVATE')
  }
  get formattedTime(): string {
    return new Date(this.updatedDate).toLocaleString()
  }
}
