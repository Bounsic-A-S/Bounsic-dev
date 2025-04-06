import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

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
    const [hours, minutes] = this.totalDuration.split(':').map(Number);
    return `${hours} hora${hours !== 1 ? 's' : ''} ${minutes} minuto${
      minutes !== 1 ? 's' : ''
    }`;
  }
}
