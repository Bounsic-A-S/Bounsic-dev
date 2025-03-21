// search-filter.component.ts
import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, ViewChild } from '@angular/core';
import { LucideAngularModule, ChevronRight, ChevronLeft } from 'lucide-angular';

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
  public albums = [
    {
      id: 1,
      title: 'Like You Do',
      artist: 'Joji',
      cover:
        'https://i.pinimg.com/736x/93/43/93/9343933fad669973700724344ff45003.jpg',
    },
    {
      id: 2,
      title: 'Blinding Lights',
      artist: 'The Weeknd',
      cover:
        'https://i.pinimg.com/736x/94/a6/c9/94a6c97dbe731ed13e3bcf7e392f0960.jpg',
    },
    {
      id: 3,
      title: 'After Hours',
      artist: 'The Weeknd',
      cover:
        'https://i.pinimg.com/736x/f6/66/12/f66612351e98a1e260221cdcba336ab1.jpg',
    },
    {
      id: 4,
      title: 'Good Days',
      artist: 'SZA',
      cover:
        'https://i.pinimg.com/736x/0a/e2/09/0ae20923c372768058244213dfdc90a9.jpg',
    },
    {
      id: 5,
      title: 'Maria',
      artist: 'Blondie',
      cover:
        'https://i.pinimg.com/736x/cd/4f/15/cd4f1528fbe6d5c1e9b89012fd7394b4.jpg',
    },
    {
      id: 6,
      title: 'Daylight',
      artist: 'Taylor Swift',
      cover:
        'https://i.pinimg.com/736x/a0/89/72/a08972f11ad0daed9a74d7058c730c26.jpg',
    },
    {
      id: 7,
      title: 'A donde vamos',
      artist: 'Morat',
      cover:
        'https://i.pinimg.com/736x/27/64/0c/27640c8e00774a9081534486b8488ab4.jpg',
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
