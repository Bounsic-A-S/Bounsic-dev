import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { PlayListSongItemComponent } from './playlist_song_item/playlist_song.component';
import { CommonModule } from '@angular/common';
import { SongHeroComponent } from './song_hero/song_hero.component';
import { ActivatedRoute } from '@angular/router';
import { PlaylistService } from '@app/services/playlist.service';
import { Observable, of, from } from 'rxjs';
import { catchError, switchMap, tap } from 'rxjs/operators';
import { BackgroundService } from '@app/services/background.service';
import Playlist from 'src/types/playlist/Playlist';
import PlaylistDetail from 'src/types/playlist/PlaylistDetailed';

@Component({
  selector: 'app-playlist',
  standalone: true,
  templateUrl: './playlist.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [SongHeroComponent, PlayListSongItemComponent, CommonModule, NavbarAppComponent],
})
export class PlaylistComponent {
  private route = inject(ActivatedRoute);
  private playlistService = inject(PlaylistService);
  private backgroundService = inject(BackgroundService);
  bg$: Observable<string> = this.backgroundService.background$;

  public loading = true;

  playlist$: Observable<PlaylistDetail | undefined> = this.route.paramMap.pipe(
    switchMap((params) => {
      const playlistId = params.get('id');
      if (!playlistId) return of(undefined);

      return this.playlistService.getPlaylistById(playlistId).pipe(
        switchMap((response) => from(this.mapPlaylistResponse(response))),
        tap(() => {
          this.loading = false;
        }),
        catchError(() => {
          this.loading = false;
          return of(undefined);
        })
      );
    })
  );

  private async mapPlaylistResponse(response: Playlist): Promise<PlaylistDetail> {
    const songsWithDurations = await Promise.all(
      (response.songs || []).map(async (song) => ({
        ...song,
        duration: await this.getAudioDuration(song.mp3_url)
      }))
    );
    return {
      ...response,
      songs: songsWithDurations,
      totalSongs: songsWithDurations.length,
      totalDuration: songsWithDurations.reduce((acc, s) => acc + s.duration, 0)
    };
  }

  private getAudioDuration(url: string): Promise<number> {
    return new Promise((resolve) => {
      const audio = new Audio(url);
      audio.addEventListener('loadedmetadata', () => resolve(audio.duration));
      audio.addEventListener('error', () => resolve(0));
    });
  }
}
