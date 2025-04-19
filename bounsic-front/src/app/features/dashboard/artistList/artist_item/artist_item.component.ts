import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  Input,
  OnInit,
} from '@angular/core';
@Component({
  selector: 'dashboard-artist-list-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './artist_item.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ArtistListItemComponent implements OnInit {
  ngOnInit(): void {}
  @Input() artist!: {
    artist_name: string;
    img: string;
  };
}
