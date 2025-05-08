import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-skeleton-song-card-col',
  standalone: true,
  imports:[CommonModule],
  templateUrl: './skeleton-song-card-col.component.html',
})
export class SkeletonSongInColComponent {

  @Input() size!: string
}
