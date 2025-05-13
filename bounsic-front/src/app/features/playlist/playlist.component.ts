import { ChangeDetectionStrategy, Component, inject, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { catchError, distinctUntilChanged, map, shareReplay, switchMap, takeUntil } from 'rxjs/operators';
import { Observable, combineLatest, from, of, Subject } from 'rxjs';

import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { SongHeroComponent } from './song_hero/song_hero.component';
import { PlayListSongItemComponent } from './playlist_song_item/playlist_song.component';
import { PlaylistService } from '@app/services/playlist.service';
import { BackgroundService } from '@app/services/background.service';

import Playlist from 'src/types/playlist/Playlist';
import PlaylistDetail from 'src/types/playlist/PlaylistDetailed';
import { AuthService } from '@app/services/auth/auth.service';

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
export class PlaylistComponent implements OnDestroy {
  private route = inject(ActivatedRoute);
  private playlistService = inject(PlaylistService);
  private backgroundService = inject(BackgroundService);
  private authService = inject(AuthService);
  private translateService = inject(TranslateService);
  private cdr = inject(ChangeDetectorRef);

  private readonly destroy$ = new Subject<void>();

  bg$: Observable<string> = this.backgroundService.background$;
  private readonly user$ = this.authService.userProfile$;

  private readonly playlistId$ = this.route.paramMap.pipe(
    map(params => params.get('id')),
    distinctUntilChanged()
  );

  playlist$: Observable<PlaylistDetail | undefined> = combineLatest([
    this.playlistId$,
    this.user$
  ]).pipe(
    takeUntil(this.destroy$),
    switchMap(([id, user]) => {
      if (!id) return of(undefined);

      if (id !== 'likes') {
        this.cdr.markForCheck()

        return this.playlistService.getPlaylistById(id).pipe(
          switchMap((playlist) => from(this.mapPlaylistResponse(playlist))),
          catchError(() => of(undefined))
        );
      }
      if (!user?.id_user) return of(undefined);

      return this.playlistService.getLikesPlaylist(user.id_user).pipe(
        switchMap((songs) => {
          const playlist: Playlist = {
            id: 'likes',
            title: this.translateService.instant('BOUNSIC.PLAYLIST.LIKES'),
            isPublic: false,
            img_url: '/library/favorites.png',
            songs,
            updated_at: new Date(),
          };
          this.cdr.markForCheck()

          return from(this.mapPlaylistResponse(playlist));
        }),
        catchError(() => of(undefined))
      );

    }),
    shareReplay(1)
  );

  private async mapPlaylistResponse(response: Playlist): Promise<PlaylistDetail> {
    const songsWithDurations = await Promise.all(
      (response.songs || []).map(async (song) => ({
        ...song,
        // duration: await this.getAudioDuration(song.mp3_url),
        duration: 0
      }))
    );

    const result: PlaylistDetail = {
      ...response,
      songs: songsWithDurations,
      totalSongs: songsWithDurations.length,
      totalDuration: songsWithDurations.reduce((acc, s) => acc + s.duration, 0),
    };

    this.cdr.markForCheck();
    return result;
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
