import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit, inject } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { LibraryItemComponent } from './library_item/library_item.component';
import { PlaylistService } from '@app/services/playlist.service';
import { catchError, map, of, Observable } from 'rxjs';

interface Playlist {
    id: number;
    title: string;
    songCount: number;
    coverUrl: string;
}

@Component({
    selector: 'app-library',
    standalone: true,
    templateUrl: './library.component.html',
    imports: [NavbarAppComponent, CommonModule, LibraryItemComponent],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class LibraryComponent implements OnInit {
    private playlistService = inject(PlaylistService);

    favorites: Playlist = {
        id: 4,
        title: 'Lista de Me gustas',
        songCount: 156,
        coverUrl: '/library/favorites.png'
    };

    likedPlaylists: Playlist[] = [
        {
            id: 5,
            title: 'Jueves',
            songCount: 2,
            coverUrl: 'https://i.pinimg.com/736x/05/28/d0/0528d0292b477ef58b027f09459fe9aa.jpg'
        }
    ];

    playlistsT$!: Observable<Playlist[]>;

    private defaultPlaylists: Playlist[] = [
        {
            id: 1,
            title: 'Psychedelic Beats',
            songCount: 20,
            coverUrl: 'https://i.pinimg.com/736x/8f/fe/0d/8ffe0d1ef650cfcbf114bcc48527eedc.jpg'
        },
        {
            id: 2,
            title: 'You can don omar',
            songCount: 17,
            coverUrl: 'https://i.pinimg.com/736x/62/a1/fd/62a1fdfd53b8ca8c9136af99ec6c41ed.jpg'
        },
        {
            id: 3,
            title: '# Tec',
            songCount: 79,
            coverUrl: 'https://i.pinimg.com/736x/d8/1a/31/d81a315aabbbb422b7d2501cc1702beb.jpg'
        }
    ];

    ngOnInit(): void {
        this.playlistsT$ = this.playlistService.getAllPlaylist().pipe(
            map(response => {
                if (Array.isArray(response) && response.length > 0) {
                    return response.map((item, index) => ({
                        id: item._id,
                        title: item.title || `Lista ${index + 1}`,
                        songCount: item.songs?.length || 0,
                        coverUrl: item.img_url || ''
                    }));
                }
                return this.defaultPlaylists;
            }),
            catchError(err => {
                console.error('Error al obtener playlists:', err);
                return of(this.defaultPlaylists);
            })
        );
    }
}
