import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { PlayListSongItemComponent } from './playlist_song_item/playlist_song.component';
import { CommonModule } from '@angular/common';
import { SongHeroComponent } from './song_hero/song_hero.component';
import { ActivatedRoute } from '@angular/router';
import { PlaylistService } from '@app/services/playlist.service';
import { Observable, of } from 'rxjs';
import { catchError, map, switchMap, tap } from 'rxjs/operators';

interface Song {
  id: number;
  title: string;
  artist: string;
  album: string;
  cover: string;
  duration: string;
  mp3Url:string;
}

interface PlaylistDetail {
  id: number | string;
  name: string;
  description: string;
  imageUrl: string;
  totalSongs: number;
  totalDuration: string;
  songs: Song[];
}

@Component({
  selector: 'app-playlist',
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
  private route: ActivatedRoute = inject(ActivatedRoute);
  private playlistService = inject(PlaylistService);

  playlistId$: Observable<string | null> = this.route.paramMap.pipe(
    map(params => params.get('id'))
  );

  album$: Observable<PlaylistDetail | undefined> = this.playlistId$.pipe(
    tap(id => console.log('Playlist ID:', id)),
    switchMap(playlistId => {
      if (!playlistId) {
        console.log('No playlist ID provided');
        return of(undefined);
      }
      console.log('Fetching playlist with ID:', playlistId);
      return this.playlistService.getPlaylistById(playlistId).pipe(
        tap(response => console.log('API Response:', response)),
        map(response => ({
          id: response.id,
          name: response.name || response.title || 'Untitled Playlist',
          description: response.description ?? '',
          imageUrl: response.img_url || '',
          totalSongs: response.songs?.length || 0,
          totalDuration: this.calculateTotalDuration(response.songs || []),
          songs: (response.songs || []).map((song: { _id: any; id: any; title: any; artist: any; album: any; img_url: any; mp3_url:any, cover: any; duration: any; },i: number) => ({
            id:i+1,
            title: song.title || '',
            artist: song.artist || '',
            album: song.album || '',
            cover: song.img_url || song.cover || '',
            mp3Url: song.mp3_url || '',
            duration: song.duration || '0:00'
          }))
        })),
        catchError(error => {
          console.error('Error fetching playlist:', error);
          return of(undefined);
        })
      );
    })
  );

  private calculateTotalDuration(songs: any[]): string {
    if (!songs || songs.length === 0) return '0:00';
    const totalSeconds = songs.reduce((acc, song) => {
      const duration = song.duration || '0:00';
      const [minutes, seconds] = duration.split(':').map(Number);
      return acc + (minutes * 60 + (seconds || 0));
    }, 0);
    
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }

  ngOnInit(): void {
    // The subscription is handled automatically by the async pipe in the template
  }
}