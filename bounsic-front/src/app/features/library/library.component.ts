import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  OnInit,
  inject,
} from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { LibraryItemComponent } from './library_item/library_item.component';
import { PlaylistService } from '@app/services/playlist.service';
import { catchError, map, of, Observable } from 'rxjs';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { BackgroundService } from '@app/services/background.service';
import LibraryPlaylist from 'src/types/playlist/LIbraryPlaylist';
import { AuthService } from '@app/services/auth/auth.service';
import User from 'src/types/user/User';
import { ModalCreatePlaylistComponent } from './modal_create_playlist/modal_create_playlist.component';

@Component({
  selector: 'app-library',
  standalone: true,
  templateUrl: './library.component.html',
  imports: [
    NavbarAppComponent,
    CommonModule,
    LibraryItemComponent,
    TranslateModule,
    ModalCreatePlaylistComponent,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LibraryComponent implements OnInit {
  private playlistService = inject(PlaylistService);
  private backgroundService = inject(BackgroundService);
  private translateService = inject(TranslateService);
  private authService = inject(AuthService);

  user: User | null = null;
  bg$: Observable<string> = this.backgroundService.background$;

  favorites$!: Observable<LibraryPlaylist>;

  playlistsT$!: Observable<LibraryPlaylist[]>;

  isModalOpen = false;

  private defaultPlaylists: LibraryPlaylist[] = [
    {
      id: '1',
      title: 'Not found',
      song_count: 0,
      isPublic: true,
      img_url:
        'https://i.pinimg.com/736x/3a/67/19/3a67194f5897030237d83289372cf684.jpg',
    },
  ];
  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
  }
  loadPlaylists() {
    if (this.user?.id_user) {
      this.playlistsT$ = this.playlistService
        .getAllPlaylist(this.user.id_user)
        .pipe(
          map((response) => response || this.defaultPlaylists),
          catchError((err) => {
            console.error('Error al obtener playlists:', err);
            return of(this.defaultPlaylists);
          })
        );
    }
  }

  ngOnInit(): void {
    this.user = this.authService.getUserProfile();
    this.loadPlaylists()
    if (this.user?.id_user) {
      this.favorites$ = this.playlistService
        .getLikesCount(this.user.id_user)
        .pipe(
          map((count) => ({
            id: 'likes',
            title: this.translateService.instant('BOUNSIC.PLAYLIST.LIKES'),
            song_count: count,
            isPublic: false,
            img_url: '/library/favorites.png',
          })),
          catchError((err) => {
            console.error('Error al obtener favoritos:', err);
            return of({
              id: 'likes',
              title: this.translateService.instant('BOUNSIC.PLAYLIST.LIKES'),
              song_count: 0,
              isPublic: false,
              img_url: '/library/favorites.png',
            });
          })
        );
    }
  }
}
