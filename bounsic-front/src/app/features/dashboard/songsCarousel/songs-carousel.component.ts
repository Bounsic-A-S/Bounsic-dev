// search-filter.component.ts
import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  Input,
  ViewChild,
} from '@angular/core';
import { LucideAngularModule, ChevronRight, ChevronLeft } from 'lucide-angular';
import DashboardSong from 'src/types/dashboard/DashboardSong';

@Component({
  selector: 'dashboard-songsCarousel',
  templateUrl: 'songs-carousel.component.html',
  imports: [CommonModule, LucideAngularModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SongsCarouselComponent {
  @ViewChild('scrollContainer', { static: false }) scrollContainer!: ElementRef;
  readonly ChevronRight = ChevronRight;
  readonly ChevronLeft = ChevronLeft;
  @Input() songs!: DashboardSong[] | null;
  public albums : DashboardSong[] = [
    {
      _id: '1',
      title: 'Like You Do',
      artist: 'Joji',
      img_url:
        'https://i.pinimg.com/736x/93/43/93/9343933fad669973700724344ff45003.jpg',
      album: '',
    },
    {
      _id: '2',
      title: 'Blinding Lights',
      artist: 'The Weeknd',
      img_url:
        'https://i.pinimg.com/736x/94/a6/c9/94a6c97dbe731ed13e3bcf7e392f0960.jpg',
      album: '',
    },
    {
      _id: '3',
      title: 'After Hours',
      artist: 'The Weeknd',
      img_url:
        'https://i.pinimg.com/736x/f6/66/12/f66612351e98a1e260221cdcba336ab1.jpg',
      album: '',
    },
    {
      _id: "4",
      title: 'Good Days',
      artist: 'SZA',
      img_url:
        'https://i.pinimg.com/736x/0a/e2/09/0ae20923c372768058244213dfdc90a9.jpg',
      album: '',
    },
    {
      _id: '5',
      title: 'Maria',
      artist: 'Blondie',
      img_url:
        'https://i.pinimg.com/736x/cd/4f/15/cd4f1528fbe6d5c1e9b89012fd7394b4.jpg',
      album: '',
    },
    {
      _id: '6',
      title: 'Daylight',
      artist: 'Taylor Swift',
      img_url:
        'https://i.pinimg.com/736x/a0/89/72/a08972f11ad0daed9a74d7058c730c26.jpg',
      album: '',
    },
    {
      _id: '7',
      title: 'A donde vamos',
      artist: 'Morat',
      img_url:
        'https://i.pinimg.com/736x/27/64/0c/27640c8e00774a9081534486b8488ab4.jpg',
      album: '',
    },
  ];
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
