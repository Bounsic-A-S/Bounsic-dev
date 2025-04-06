import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

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
    imports: [CommonModule],
    changeDetection: ChangeDetectionStrategy.OnPush
})

export class LibraryItemComponent {
    @Input() playlist!: Playlist;
}