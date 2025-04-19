import { CommonModule } from '@angular/common';
import { Component, HostListener, Input } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'dashboard-safe-choice-list',
  templateUrl: 'safe-choices-list.component.html',
  imports: [CommonModule, RouterModule],
})
export class SafeChoiceListComponent {

  @Input() songs!: any[] | null;
  public safeChoiceSongs = [
    {
      id: 1,
      title: 'Yellow',
      artist: 'Coldplay',
      album: 'Parachutes',
      img_url:
        'https://i.pinimg.com/736x/9a/5d/ec/9a5dec457d79fb2916fda52c6f831652.jpg',
    },
    {
      id: 2,
      title: 'Creep',
      artist: 'Radiohead',
      album: 'Pablo Honey',
      img_url:
        'https://i.pinimg.com/736x/4c/b9/78/4cb9781154d0dd1a316d5b45124f0912.jpg',
    },
    {
      id: 3,
      title: 'Boulevard of Broken Dreams',
      artist: 'Green Day',
      album: 'American Idiot',
      img_url:
        'https://i.pinimg.com/736x/ae/b9/70/aeb970e9c064d436bda11462fc889489.jpg',
    },
    {
      id: 4,
      title: 'Take Me to Church',
      artist: 'Hozier',
      album: 'Hozier',
      img_url:
        'https://i.pinimg.com/736x/a6/47/91/a64791f712cb10397610c83aa2612895.jpg',
    },
    {
      id: 5,
      title: 'Believer',
      artist: 'Imagine Dragons',
      album: 'Evolve',
      img_url:
        'https://i.pinimg.com/736x/5b/4c/ed/5b4ced22923bd1c1353d28213bffad03.jpg',
    },
    {
      id: 6,
      title: 'Uptown Funk',
      artist: 'Mark Ronson ft. Bruno Mars',
      album: 'Uptown Special',
      img_url:
        'https://i.pinimg.com/736x/6c/f6/7f/6cf67f7ed6227a20b15035bd57d8927f.jpg',
    },
    {
      id: 7,
      title: "Can't Stop",
      artist: 'Red Hot Chili Peppers',
      album: 'By the Way',
      img_url:
        'https://i.pinimg.com/736x/c7/dc/60/c7dc60cfeaab1c085d3bba491826a06b.jpg',
    },
    {
      id: 1,
      title: 'Yellow',
      artist: 'Coldplay',
      album: 'Parachutes',
      img_url:
        'https://i.pinimg.com/736x/9a/5d/ec/9a5dec457d79fb2916fda52c6f831652.jpg',
    },
    {
      id: 2,
      title: 'Creep',
      artist: 'Radiohead',
      album: 'Pablo Honey',
      img_url:
        'https://i.pinimg.com/736x/4c/b9/78/4cb9781154d0dd1a316d5b45124f0912.jpg',
    },
    {
      id: 3,
      title: 'Boulevard of Broken Dreams',
      artist: 'Green Day',
      album: 'American Idiot',
      img_url:
        'https://i.pinimg.com/736x/ae/b9/70/aeb970e9c064d436bda11462fc889489.jpg',
    },
    {
      id: 4,
      title: 'Take Me to Church',
      artist: 'Hozier',
      album: 'Hozier',
      img_url:
        'https://i.pinimg.com/736x/a6/47/91/a64791f712cb10397610c83aa2612895.jpg',
    },
    {
      id: 5,
      title: 'Believer',
      artist: 'Imagine Dragons',
      album: 'Evolve',
      img_url:
        'https://i.pinimg.com/736x/5b/4c/ed/5b4ced22923bd1c1353d28213bffad03.jpg',
    },
    {
      id: 6,
      title: 'Uptown Funk',
      artist: 'Mark Ronson ft. Bruno Mars',
      album: 'Uptown Special',
      img_url:
        'https://i.pinimg.com/736x/6c/f6/7f/6cf67f7ed6227a20b15035bd57d8927f.jpg',
    },
    {
      id: 7,
      title: "Can't Stop",
      artist: 'Red Hot Chili Peppers',
      album: 'By the Way',
      img_url:
        'https://i.pinimg.com/736x/c7/dc/60/c7dc60cfeaab1c085d3bba491826a06b.jpg',
    },
  ];
  public maxSongsToShow: number = 3;

  ngOnInit() {
    this.updateMaxSongsToShow();
  }

  @HostListener('window:resize', [])
  onResize() {
    this.updateMaxSongsToShow();
  }

  private updateMaxSongsToShow() {
    if (window.innerWidth < 640) {
      this.maxSongsToShow = 3;
    }
    if (window.innerWidth >= 640 && window.innerWidth <= 1280) {
      this.maxSongsToShow = 8;
    }
    if (window.innerWidth > 1280) {
      this.maxSongsToShow = 12;
    }
  }
}
