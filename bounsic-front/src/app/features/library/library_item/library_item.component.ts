import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import LibraryPlaylist from 'src/types/playlist/LIbraryPlaylist';

@Component({
    selector: 'library-item',
    standalone: true,
    templateUrl: './library_item.component.html',
    imports: [CommonModule,TranslateModule],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class LibraryItemComponent {
    @Input() playlist!: LibraryPlaylist;

    constructor(private router: Router) {}

    goToPlaylist() {
        console.log(this.playlist)
        this.router.navigate(['/playlist', this.playlist.id]);
    }
}
