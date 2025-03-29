import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
@Component({
  selector: 'playlist-item',
  standalone: true,
  templateUrl: './playlist_song_item.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlayListSongItemComponent {
  @Input() id!: number;
  @Input() title!: string;
  @Input() artist!: string;
  @Input() album!: string;
  @Input() duration!: string;
  @Input() imageUrl!: string;
}
