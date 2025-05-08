// search-filter.component.ts
import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  Input,
  ViewChild,
} from '@angular/core';
import { RouterModule } from '@angular/router';
import { SkeletonSongInColComponent } from '@app/shared/ui/skeletons/song_in_col/skeleton-song-card-col.component';
import { LucideAngularModule, ChevronRight, ChevronLeft } from 'lucide-angular';
import DashboardSong from 'src/types/dashboard/DashboardSong';

@Component({
  selector: 'dashboard-songsCarousel',
  templateUrl: 'songs-carousel.component.html',
  imports: [CommonModule, LucideAngularModule,SkeletonSongInColComponent,RouterModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SongsCarouselComponent {
  @ViewChild('scrollContainer', { static: false }) scrollContainer!: ElementRef;
  readonly ChevronRight = ChevronRight;
  readonly ChevronLeft = ChevronLeft;
  private _songs!: DashboardSong[] | null;
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
