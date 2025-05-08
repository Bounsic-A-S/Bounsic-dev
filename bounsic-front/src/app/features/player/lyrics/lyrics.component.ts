import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, CUSTOM_ELEMENTS_SCHEMA, inject, Input } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'player-lyrics',
  standalone: true,
  templateUrl: './lyrics.component.html',
  imports:[CommonModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerLyricsComponent {
  private translateService = inject(TranslateService)
  @Input() lyrics!: string | null | undefined
  lines: string[] = [];

  getLyrics(): string[] {
    const fallback = this.translateService.instant('BOUNSIC.PLAYER.LYRIC_NOT_FOUND');
    const text = this.lyrics ?? fallback;
    this.lines = text.split('\n\n');
    return this.lines;
  }

}
