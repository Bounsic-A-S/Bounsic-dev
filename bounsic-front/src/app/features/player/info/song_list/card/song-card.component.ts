import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from "@angular/common"
import DashboardSong from 'src/types/dashboard/DashboardSong';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'player-song-card-ui',
    standalone: true,
    imports: [CommonModule, RouterModule],
    templateUrl: './song-card.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerSongCardUi {
    @Input() song!: DashboardSong
    @Input() showActions = false
}


