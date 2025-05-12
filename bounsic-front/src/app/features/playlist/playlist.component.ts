import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { catchError, map, shareReplay, switchMap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';

import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { SongHeroComponent } from './song_hero/song_hero.component';
import { PlayListSongItemComponent } from './playlist_song_item/playlist_song.component';
import { PlaylistService } from '@app/services/playlist.service';
import { BackgroundService } from '@app/services/background.service';

import Playlist from 'src/types/playlist/Playlist';
import PlaylistDetail from 'src/types/playlist/PlaylistDetailed';

@Component({
  selector: 'app-playlist',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    CommonModule,
    NavbarAppComponent,
    SongHeroComponent,
    PlayListSongItemComponent,
    TranslateModule,
  ],
  templateUrl: './playlist.component.html',
})
export class PlaylistComponent {
  private route = inject(ActivatedRoute);
  private playlistService = inject(PlaylistService);
  private backgroundService = inject(BackgroundService);

  bg$: Observable<string> = this.backgroundService.background$;

  playlist$: Observable<PlaylistDetail | undefined> = this.route.paramMap.pipe(
    map(params => params.get('id')),
    switchMap(id => {
      if (!id) return of(undefined);
      return this.playlistService.getPlaylistById(id).pipe(
        switchMap(response => this.mapPlaylistResponse(response)),
        catchError(() => of(undefined))
      );
    }),
    shareReplay(1)
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
