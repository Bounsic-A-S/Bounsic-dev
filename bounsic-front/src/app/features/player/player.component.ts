import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { PlayerLyricsComponent } from './lyrics/lyrics.component';
import { SongListComponent } from "./info/song_list/song-list.component";
import { PlayerMusicComponent } from "./music/music-player.component";
import { SongService } from '@app/services/song.service';
import { map, Observable, switchMap } from 'rxjs';
import { CommonModule } from '@angular/common';
import { PlayerSong } from './info/song/song.component';
import Song from 'src/types/Song';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-player',
  standalone: true,
  imports: [NavbarAppComponent, PlayerLyricsComponent, PlayerSong, PlayerMusicComponent, SongListComponent, CommonModule],
  templateUrl: './player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerComponent {
  private songService = inject(SongService);
  private route = inject(ActivatedRoute);

  song$: Observable<Song> = this.route.paramMap.pipe(
    map(params => params.get('id')),
    switchMap(id => this.songService.getById(id!))
  );

  mp3Url$ = this.song$.pipe(
    map(song => song?.mp3_url ?? '')
  );
}


