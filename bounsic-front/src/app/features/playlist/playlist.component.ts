import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { PlayListSongItemComponent } from './playlist_song_item/playlist_song.component';
import { CommonModule } from '@angular/common';
import { SongHeroComponent } from './song_hero/song_hero.component';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-playlist-detail',
  standalone: true,
  imports: [
    NavbarAppComponent,
    PlayListSongItemComponent,
    CommonModule,
    SongHeroComponent,
  ],
  templateUrl: './playlist.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlaylistComponent implements OnInit {
  constructor(private route: ActivatedRoute) {}
  playlistId: string = '';
  ngOnInit(): void {
    this.playlistId = this.route.snapshot.paramMap.get('id') ?? '';
    console.log(this.playlistId)
  }
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
        cover:
          'https://i.pinimg.com/736x/9a/5d/ec/9a5dec457d79fb2916fda52c6f831652.jpg',
        duration: '4:30',
      },
      {
        id: 2,
        title: 'Creep',
        artist: 'Radiohead',
        album: 'Pablo Honey',
        cover:
          'https://i.pinimg.com/736x/4c/b9/78/4cb9781154d0dd1a316d5b45124f0912.jpg',
        duration: '3:59',
      },
      {
        id: 3,
        title: 'Boulevard of Broken Dreams',
        artist: 'Green Day',
        album: 'American Idiot',
        cover:
          'https://i.pinimg.com/736x/ae/b9/70/aeb970e9c064d436bda11462fc889489.jpg',
        duration: '4:20',
      },
      {
        id: 4,
        title: 'Take Me to Church',
        artist: 'Hozier',
        album: 'Hozier',
        cover:
          'https://i.pinimg.com/736x/a6/47/91/a64791f712cb10397610c83aa2612895.jpg',
        duration: '4:01',
      },
      {
        id: 5,
        title: 'Believer',
        artist: 'Imagine Dragons',
        album: 'Evolve',
        cover:
          'https://i.pinimg.com/736x/5b/4c/ed/5b4ced22923bd1c1353d28213bffad03.jpg',
        duration: '3:24',
      },
      {
        id: 6,
        title: 'Uptown Funk',
        artist: 'Mark Ronson ft. Bruno Mars',
        album: 'Uptown Special',
        cover:
          'https://i.pinimg.com/736x/6c/f6/7f/6cf67f7ed6227a20b15035bd57d8927f.jpg',
        duration: '4:30',
      },
      {
        id: 7,
        title: "Can't Stop",
        artist: 'Red Hot Chili Peppers',
        album: 'By the Way',
        cover:
          'https://i.pinimg.com/736x/c7/dc/60/c7dc60cfeaab1c085d3bba491826a06b.jpg',
        duration: '4:29',
      }, {
        id: 8,
        title: "Smells Like Teen Spirit",
        artist: "Nirvana",
        album: "Nevermind",
        cover: "https://i.pinimg.com/736x/66/4e/1d/664e1d976aea5b6fde0c6c09f4a48572.jpg",
        duration: "5:01"
      },
      {
        id: 9,
        title: "Somebody That I Used to Know",
        artist: "Gotye ft. Kimbra",
        album: "Making Mirrors",
        cover: "https://i.pinimg.com/736x/05/90/02/05900242bf89234a36fc1d8dfd83d0de.jpg",
        duration: "4:04"
      },
      {
        id: 10,
        title: "Counting Stars",
        artist: "OneRepublic",
        album: "Native",
        cover: "https://i.pinimg.com/736x/bc/e2/0c/bce20c8a2786659b119555d45884ccd0.jpg",
        duration: "4:17"
      },
      {
        id: 11,
        title: "Clocks",
        artist: "Coldplay",
        album: "A Rush of Blood to the Head",
        cover: "https://i.pinimg.com/736x/e9/89/50/e98950fc61a295ca2c653681f6dc728e.jpg",
        duration: "5:07"
      },
      {
        id: 12,
        title: "Shape of You",
        artist: "Ed Sheeran",
        album: "÷ (Divide)",
        cover: "https://i.pinimg.com/736x/52/75/fb/5275fbf6f58f84ae522e29e434aa893d.jpg",
        duration: "3:53"
      },
      {
        id: 13,
        title: "Radioactive",
        artist: "Imagine Dragons",
        album: "Night Visions",
        cover: "https://i.pinimg.com/736x/62/ec/04/62ec049bb30969e8ef154d6aca5bd274.jpg",
        duration: "3:06"
      }
    ],
  };
}
