import { CommonModule } from '@angular/common';
import {
  Component,
  ElementRef,
  ViewChild,
  ChangeDetectionStrategy,
  Input,
} from '@angular/core';
import { LucideAngularModule, ChevronRight, ChevronLeft } from 'lucide-angular';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import { SkeletonSongInColComponent } from "../../../shared/ui/skeletons/song_in_col/skeleton-song-card-col.component";
import { RouterModule } from '@angular/router';
@Component({
  selector: 'dashboard-trending-songs',
  standalone: true,
  imports: [CommonModule, LucideAngularModule, SkeletonSongInColComponent,RouterModule],
  templateUrl: './trending-songs.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TrendingSongsComponent {
  @ViewChild('scrollContainer', { static: false }) scrollContainer!: ElementRef;
  readonly ChevronRight = ChevronRight;
  readonly ChevronLeft = ChevronLeft;
  @Input() _songs!: DashboardSong[] | null
  public loading: boolean = true;

  @Input() 
  set songs(value: DashboardSong[] | null) {
    this._songs = value;
    this.loading = !value || value.length === 0;
  }
  get songs(): DashboardSong[] | null {
    return this._songs;
  }

  scrollLeft() {
    this.scrollContainer.nativeElement.scrollBy({
      left: -500,
      behavior: 'smooth',
    });
  }

  scrollRight() {
    this.scrollContainer.nativeElement.scrollBy({
      left: 500,
      behavior: 'smooth',
    });
  }
}
