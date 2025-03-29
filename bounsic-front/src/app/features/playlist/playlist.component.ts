import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';
import { PlayListSongItemComponent } from './playlist_song_item/playlist_song.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-playlist-detail',
  standalone: true,
  imports: [NavbarAppComponent, PlayListSongItemComponent, CommonModule],
  templateUrl: './playlist.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlaylistComponent {
  public album = {
    id: 1,
    name: 'Top Hits',
    description: 'Top Hits of the Week',
    imageUrl: '',
    totalSongs: 7,
    totalDuration: '30:00',
    songs: [
      {
        id: 1,
        title: 'Yellow',
        artist: 'Coldplay',
        album: 'Parachutes',
        cover: 'https://i.pinimg.com/736x/9a/5d/ec/9a5dec457d79fb2916fda52c6f831652.jpg',
        duration: '4:30',
      },
      {
        id: 2,
        title: 'Creep',
        artist: 'Radiohead',
        album: 'Pablo Honey',
        cover: 'https://i.pinimg.com/736x/4c/b9/78/4cb9781154d0dd1a316d5b45124f0912.jpg',
        duration: '3:59',
      },
      {
        id: 3,
        title: 'Boulevard of Broken Dreams',
        artist: 'Green Day',
        album: 'American Idiot',
        cover: 'https://i.pinimg.com/736x/ae/b9/70/aeb970e9c064d436bda11462fc889489.jpg',
        duration: '4:20',
      },
      {
        id: 4,
        title: 'Take Me to Church',
        artist: 'Hozier',
        album: 'Hozier',
        cover: 'https://i.pinimg.com/736x/a6/47/91/a64791f712cb10397610c83aa2612895.jpg',
        duration: '4:01',
      },
      {
        id: 5,
        title: 'Believer',
        artist: 'Imagine Dragons',
        album: 'Evolve',
        cover: 'https://i.pinimg.com/736x/5b/4c/ed/5b4ced22923bd1c1353d28213bffad03.jpg',
        duration: '3:24',
      },
      {
        id: 6,
        title: 'Uptown Funk',
        artist: 'Mark Ronson ft. Bruno Mars',
        album: 'Uptown Special',
        cover: 'https://i.pinimg.com/736x/6c/f6/7f/6cf67f7ed6227a20b15035bd57d8927f.jpg',
        duration: '4:30',
      },
      {
        id: 7,
        title: "Can't Stop",
        artist: 'Red Hot Chili Peppers',
        album: 'By the Way',
        cover: 'https://i.pinimg.com/736x/c7/dc/60/c7dc60cfeaab1c085d3bba491826a06b.jpg',
        duration: '4:29',
      }
    ]
  };
}

