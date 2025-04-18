import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { EllipsisVertical, LucideAngularModule, Play } from 'lucide-angular';
@Component({
  selector: 'playlist-item',
  standalone: true,
  imports: [LucideAngularModule],
  templateUrl: './playlist_song_item.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlayListSongItemComponent {
  readonly Play = Play;
  readonly Options = EllipsisVertical;
  @Input() id!: number;
  @Input() title!: string;
  @Input() artist!: string;
  @Input() album!: string;
  @Input() duration!: string;
  @Input() imageUrl!: string;
  @Input() mp3Url!: string;

  playMusic() {
    console.log('Play music');
    console.log('mp3Url:', this.mp3Url);
    const mySound = new Audio(this.mp3Url);
    mySound.play();
  }
}
