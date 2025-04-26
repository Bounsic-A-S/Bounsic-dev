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
  mp3Url: string;
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
  templateUrl: './playlist.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [SongHeroComponent, PlayListSongItemComponent, CommonModule, NavbarAppComponent],
})
export class PlaylistComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private playlistService = inject(PlaylistService);

  public loading = true; // init load always tru

  playlist$: Observable<PlaylistDetail | undefined> = this.route.paramMap.pipe(
    switchMap((params) => {
      const playlistId = params.get('id');
      if (!playlistId) return of(undefined);

      return this.playlistService.getPlaylistById(playlistId).pipe(
        tap(() => {
          this.loading = false; // load ends
        }),
        map((response) => this.mapPlaylistResponse(response)),
        catchError(() => {
          this.loading = false; // load ends
          return of(undefined);
        })
      );
    })
  );

  private mapPlaylistResponse(response: any): PlaylistDetail {
    console.log(response)
    return {
      id: response.id,
      name: response.name || response.title || 'Untitled Playlist',
      description: response.description ?? '',
      imageUrl: response.img_url || '',
      totalSongs: response.songs?.length || 0,
      totalDuration: this.calculateTotalDuration(response.songs || []),
      songs: (response.songs || []).map((song: { title: any; artist: any; album: any; img_url: any; cover: any; mp3_url: any; duration: any; }, i: number) => ({
        id: i + 1,
        title: song.title || '',
        artist: song.artist || '',
        album: song.album || '',
        cover: song.img_url || song.cover || '',
        mp3Url: song.mp3_url || '',
        duration: song.duration || '0:00',
      })),
    };
  }

  private calculateTotalDuration(songs: any[]): string {
    const totalSeconds = songs.reduce((acc, song) => {
      const [minutes, seconds] = (song.duration || '0:00').split(':').map(Number);
      return acc + (minutes * 60 + (seconds || 0));
    }, 0);

    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }

  ngOnInit(): void {
  }
}
