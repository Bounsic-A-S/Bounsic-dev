import { CommonModule } from '@angular/common';
import {
  Component,
  ElementRef,
  ViewChild,
  ChangeDetectionStrategy,
} from '@angular/core';
import { LucideAngularModule, ChevronRight, ChevronLeft } from 'lucide-angular';
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
  public trendingSongs = [
    {
      id: 1,
      title: 'Dance the Night',
      artist: 'Dua Lipa',
      cover:
        'https://i.pinimg.com/736x/7b/3b/76/7b3b76163d8177d98873fcabed9abb49.jpg',
    },
    {
      id: 2,
      title: 'Shivers',
      artist: 'Ed Sheeran',
      cover:
        'https://i.pinimg.com/736x/85/45/8b/85458b686b514e9aad47d6a58cbb8b2e.jpg',
    },
    {
      id: 3,
      title: 'Enemy',
      artist: 'Imagine Dragons',
      cover:
        'https://i.pinimg.com/736x/27/c2/54/27c254f72d431b459494d7ff186b59ad.jpg',
    },
    {
      id: 4,
      title: 'Super Freaky Girl',
      artist: 'Nicki Minaj',
      cover:
        'https://i.pinimg.com/736x/7c/35/10/7c35103a6cd5dfc5df8171b586000320.jpg',
    },
    {
      id: 5,
      title: 'Monaco',
      artist: 'Bad Bunny',
      cover:
        'https://i.pinimg.com/736x/df/b2/84/dfb284474c672785f732178923657cf2.jpg',
    },
    {
      id: 6,
      title: 'Watermelon Sugar',
      artist: 'Harry Styles',
      cover:
        'https://i.pinimg.com/736x/38/21/94/382194fbaf52fe4a3242fc96aa34fd34.jpg',
    },
    {
      id: 7,
      title: 'Flowers',
      artist: 'Miley Cyrus',
      cover:
        'https://i.pinimg.com/736x/60/b0/1b/60b01bb65e59e15fee63f73f375b60b5.jpg',
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
