import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

interface Playlist {
    id: number;
    title: string;
    songCount: number;
    coverUrl: string;
}

@Component({
    selector: 'library-item',
    standalone: true,
    templateUrl: './library_item.component.html',
    imports: [CommonModule,TranslateModule],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class LibraryItemComponent {
    @Input() playlist!: Playlist;

    constructor(private router: Router) {}

    goToPlaylist() {
        this.router.navigate(['/playlist', this.playlist.id]);
    }
}
