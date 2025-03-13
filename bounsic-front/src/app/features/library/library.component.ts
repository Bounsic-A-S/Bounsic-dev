import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';

interface Playlist {
    id: number;
    title: string;
    songCount: number;
    coverUrl: string;
}
@Component({
    selector: 'app-library', // name of the component
    standalone: true, // not module
    templateUrl: './library.component.html', // render
    imports: [NavbarAppComponent, CommonModule],
    changeDetection: ChangeDetectionStrategy.OnPush
})

export class LibraryComponent {
    playlists: Playlist[] = [
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

    likedPlaylists: Playlist[] = [
        {
            id: 4,
            title: 'Lista de Me gustas',
            songCount: 156,
            coverUrl: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-zPe2si1GE8dvlMhks4FqZw6lawdjES.png'
        },
        {
            id: 5,
            title: 'Jueves',
            songCount: 2,
            coverUrl: 'https://i.pinimg.com/736x/05/28/d0/0528d0292b477ef58b027f09459fe9aa.jpg'
        }
    ];
}