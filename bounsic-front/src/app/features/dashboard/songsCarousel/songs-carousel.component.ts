// search-filter.component.ts
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { LucideAngularModule, ChevronRight, ChevronLeft } from 'lucide-angular';

@Component({
  selector: 'dashboard-songsCarousel',
  templateUrl: 'songs-carousel.component.html',
  imports: [CommonModule, LucideAngularModule],
})
export class SongsCarouselComponent {
  readonly ChevronRight = ChevronRight;
  readonly ChevronLeft = ChevronLeft;
  public albums = [
    {
      "id": 1,
      "title": "Like You Do",
      "artist": "Joji",
      "cover": "https://i.pinimg.com/736x/b6/e5/6e/b6e56e823610424007e409a658445338.jpg"
    },
    {
      "id": 2,
      "title": "Blinding Lights",
      "artist": "The Weeknd",
      "cover": "https://i.pinimg.com/736x/d8/2d/b1/d82db192bfa37d3a0ca8594bf22f018f.jpg"
    },
    {
      "id": 3,
      "title": "After Hours",
      "artist": "The Weeknd",
      "cover": "https://i.pinimg.com/736x/04/26/97/042697ed3bf0ad7876683527bb33bcbb.jpg"
    },
    {
      "id": 4,
      "title": "Good Days",
      "artist": "SZA",
      "cover": "https://i.pinimg.com/736x/60/6e/42/606e42c9c46dac97d8a318f4af23c92e.jpg "
    },
    {
      "id": 5,
      "title": "Maria",
      "artist": "Blondie",
      "cover": "https://i.pinimg.com/736x/cd/4f/15/cd4f1528fbe6d5c1e9b89012fd7394b4.jpg"
    }
  ]

}