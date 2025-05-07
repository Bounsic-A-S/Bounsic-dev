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
@Component({
  selector: 'dashboard-trending-songs',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  templateUrl: './trending-songs.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TrendingSongsComponent {
  @ViewChild('scrollContainer', { static: false }) scrollContainer!: ElementRef;
  readonly ChevronRight = ChevronRight;
  readonly ChevronLeft = ChevronLeft;
  @Input() songs!: DashboardSong[] | null

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
