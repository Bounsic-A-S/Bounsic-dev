import { ChangeDetectionStrategy, Component } from '@angular/core';
@Component({
  selector: 'playlist-item',
  standalone: true,
  templateUrl: './playlist_song_item.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayListSongItemComponent { 
}
