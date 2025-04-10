import { CommonModule } from '@angular/common';
import { Component, HostListener, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'dashboard-last-month-songs',
  templateUrl: './last-month-songs.component.html',
  imports: [CommonModule, RouterModule],
})
export class LastMonthSongsComponent implements OnInit {
  public safeChoiceSongs = [
    {
      id: 1,
      title: 'For What Its Worth',
      artist: 'Buffalo Springfield',
      album: 'Buffalo Springfield',
      cover: 'https://i.pinimg.com/736x/f1/51/b7/f151b768ca4c0b64e52a95d977de7f25.jpg'
    },
    {
      id: 2,
      title: 'Monday, Monday',
      artist: 'The Mamas & The Papas',
      album: 'If You Can Believe Your Eyes and Ears',
      cover: 'https://i.pinimg.com/736x/7d/ac/16/7dac161ab214c23a8a04acbbda07c10d.jpg'
    },    
    {
      id: 3,
      title: 'Blinding Lights',
      artist: 'The Weeknd',
      album: 'After Hours',
      cover: 'https://i.pinimg.com/736x/94/a6/c9/94a6c97dbe731ed13e3bcf7e392f0960.jpg'
    },
    {
      id: 4,
      title: 'Paint It Black',
      artist: 'The Rolling Stones',
      album: 'Aftermath',
      cover: 'https://i.pinimg.com/736x/f0/38/6f/f0386f0a0f39dc1dbf83bc3c26bf8ac0.jpg'
    },
    {
      id: 5,
      title: 'Something',
      artist: 'The Beatles',
      album: 'Abbey Road',
      cover: 'https://i.pinimg.com/736x/ff/dd/f2/ffddf21cc3a16a0dba241f145ce0822a.jpg'
    },
    {
      id: 6,
      title: 'Here Comes the Sun',
      artist: 'The Beatles',
      album: 'Abbey Road',
      cover: 'https://i.pinimg.com/736x/ff/dd/f2/ffddf21cc3a16a0dba241f145ce0822a.jpg'
    },
    {
      id: 7,
      title: 'The Sound of Silence',
      artist: 'Simon & Garfunkel',
      album: 'Sounds of Silence',
      cover: 'https://i.pinimg.com/736x/eb/3c/43/eb3c438ad5e717cad320dba138b24a6d.jpg'
    },
    {
      id: 8,
      title: 'Mrs. Robinson',
      artist: 'Simon & Garfunkel',
      album: 'Bookends',
      cover: 'https://i.pinimg.com/736x/ee/3c/78/ee3c78bc5084658f3557b70e2b804d56.jpg'
    },
    {
      id: 9,
      title: 'Take Me to Church',
      artist: 'Hozier',
      album: 'Hozier',
      cover: 'https://i.pinimg.com/736x/a6/47/91/a64791f712cb10397610c83aa2612895.jpg'
    },
    {
      id: 10,
      title: 'Uptown Funk',
      artist: 'Mark Ronson ft. Bruno Mars',
      album: 'Uptown Special',
      cover: 'https://i.pinimg.com/736x/6c/f6/7f/6cf67f7ed6227a20b15035bd57d8927f.jpg'
    },
    {
      id: 11,
      title: 'Believer',
      artist: 'Imagine Dragons',
      album: 'Evolve',
      cover: 'https://i.pinimg.com/736x/5b/4c/ed/5b4ced22923bd1c1353d28213bffad03.jpg'
    },
    {
      id: 12,
      title: 'Like You Do',
      artist: 'Joji',
      album: 'Nectar',
      cover: 'https://i.pinimg.com/736x/93/43/93/9343933fad669973700724344ff45003.jpg'
    }
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
