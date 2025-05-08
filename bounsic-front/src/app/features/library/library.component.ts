import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit, inject } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { LibraryItemComponent } from './library_item/library_item.component';
import { PlaylistService } from '@app/services/playlist.service';
import { catchError, map, of, Observable } from 'rxjs';
import { TranslateModule } from '@ngx-translate/core';
import { BackgroundService } from '@app/services/background.service';
interface Playlist {
  playlist_id: string;
  title: string;
  songCount: number;
  img_url: string;
}

@Component({
  selector: 'app-library',
  standalone: true,
  templateUrl: './library.component.html',
  imports: [NavbarAppComponent, CommonModule, LibraryItemComponent, TranslateModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LibraryComponent implements OnInit {
  private playlistService = inject(PlaylistService);
  private backgroundService = inject(BackgroundService)
  bg$: Observable<string> = this.backgroundService.background$;
  
  favorites: Playlist = {
    playlist_id: "4",
    title: 'Lista de Me gustas',
    songCount: 156,
    img_url: '/library/favorites.png'
  };

  likedPlaylists: Playlist[] = [
    {
      playlist_id: "5",
      title: 'Jueves',
      songCount: 2,
      img_url: 'https://i.pinimg.com/736x/05/28/d0/0528d0292b477ef58b027f09459fe9aa.jpg'
    }
  ];

  playlistsT$!: Observable<Playlist[]>;

  private defaultPlaylists: Playlist[] = [
    {
      playlist_id: "1",
      title: 'Not found',
      songCount: 0,
      img_url: 'https://i.pinimg.com/736x/3a/67/19/3a67194f5897030237d83289372cf684.jpg'
    }
  ];


  ngOnInit(): void {
    this.playlistsT$ = this.playlistService.getAllPlaylist().pipe(
      map((response) => {
        if (Array.isArray(response) && response.length > 0) {
          return response.map((item, index) => ({
            playlist_id: item.playlist_id,
            title: item.title || `Lista ${index + 1}`,
            songCount: item.songs?.length || 0,
            img_url: item.img_url || ''
          }));
        }
        return this.defaultPlaylists;
      }),
      catchError((err) => {
        console.error('Error al obtener playlists:', err);
        return of(this.defaultPlaylists);
      })
    );
  }
}
