import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit, inject } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { LibraryItemComponent } from './library_item/library_item.component';
import { PlaylistService } from '@app/services/playlist.service';
import { catchError, map, of, Observable } from 'rxjs';
import { TranslateModule } from '@ngx-translate/core';
import { BackgroundService } from '@app/services/background.service';
import LibraryPlaylist from 'src/types/playlist/LIbraryPlaylist';

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
  
  favorites: LibraryPlaylist = {
    id: "4",
    title: 'Lista de Me gustas',
    song_count: 156,
    isPublic:false,
    img_url: '/library/favorites.png'
  };

  likedPlaylists: LibraryPlaylist[] = [
    {
      id: "5",
      title: 'Jueves',
      song_count: 2,
      isPublic:false,
      img_url: 'https://i.pinimg.com/736x/05/28/d0/0528d0292b477ef58b027f09459fe9aa.jpg'
    }
  ];

  playlistsT$!: Observable<LibraryPlaylist[]>;

  private defaultPlaylists: LibraryPlaylist[] = [
    {
      id: "1",
      title: 'Not found',
      song_count: 0,
      isPublic:true,
      img_url: 'https://i.pinimg.com/736x/3a/67/19/3a67194f5897030237d83289372cf684.jpg'
    }
  ];


  ngOnInit(): void {
    this.playlistsT$ = this.playlistService.getAllPlaylist().pipe(
      map((response) => {
        if (response) return response
        return this.defaultPlaylists;
      }),
      catchError((err) => {
        console.error('Error al obtener playlists:', err);
        return of(this.defaultPlaylists);
      })
    );
  }
}
