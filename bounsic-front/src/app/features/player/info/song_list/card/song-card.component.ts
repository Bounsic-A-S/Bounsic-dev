import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from "@angular/common"

@Component({
    selector: 'player-song-card-ui',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './song-card.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerSongCardUi {
    @Input() song!: Song
    @Input() showActions = false
}

export interface Song {
    id: string
    title: string
    artist: string
    coverUrl: string
}


