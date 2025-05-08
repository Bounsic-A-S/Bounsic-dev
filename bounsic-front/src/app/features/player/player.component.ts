import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { map, switchMap, forkJoin } from 'rxjs';

import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { PlayerLyricsComponent } from './lyrics/lyrics.component';
import { SongListComponent } from "./info/song_list/song-list.component";
import { PlayerMusicComponent } from "./music/music-player.component";
import { PlayerSong } from './info/song/song.component';

import { SongService } from '@app/services/song.service';
import { BackgroundService } from '@app/services/background.service';
import { AuthService } from '@app/services/auth/auth.service';
import { UserService } from '@app/services/auth/user.service';

@Component({
  selector: 'app-player',
  standalone: true,
  imports: [
    CommonModule,
    NavbarAppComponent,
    PlayerLyricsComponent,
    PlayerSong,
    PlayerMusicComponent,
    SongListComponent
  ],
  templateUrl: './player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerComponent {
  private route = inject(ActivatedRoute);
  private songService = inject(SongService);
  private authService = inject(AuthService);
  private userService = inject(UserService);
  private backgroundService = inject(BackgroundService);

  bg$ = this.backgroundService.background$;

  song$ = this.route.paramMap.pipe(
    map(params => params.get('id')),
    switchMap(id => {
      if (!id) throw new Error('ID de canción no encontrado');

      return this.authService.userProfile$.pipe(
        switchMap(user => {
          if (!user.id_user) return this.songService.getById(id);

          return forkJoin({
            song: this.songService.getById(id),
            liked: this.userService.isSongLikedByUser(user.id_user, id)
          }).pipe(
            map(({ song, liked }) => ({
              ...song,
              isLiked: liked
            }))
          );
        })
      );
    })
  );


  mp3Url$ = this.song$.pipe(
    map(song => song?.mp3_url ?? '')
  );
}
