import { CommonModule } from '@angular/common';
import { Component, HostListener, Input, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import { SkeletonSongInRowComponent } from "../../../shared/ui/skeletons/song_in_row/skeleton-song-card-row.component";

@Component({
  selector: 'dashboard-last-month-songs',
  templateUrl: './last-month-songs.component.html',
  imports: [CommonModule, RouterModule, SkeletonSongInRowComponent],
})
export class LastMonthSongsComponent implements OnInit {
  private _songs!: DashboardSong[] | null;
  public loading = true
  @Input() 
  set songs(value: DashboardSong[] | null) {
    this._songs = value;
    this.loading = !value || value.length === 0;
  }
  get songs(): DashboardSong[] | null {
    return this._songs;
  }
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
