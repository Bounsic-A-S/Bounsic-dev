import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import {
  LucideAngularModule,
  SkipBack,
  SkipForward,
  Play,
  Pause,
} from 'lucide-angular';
@Component({
  selector: 'player-music-playbar',
  standalone: true,
  imports: [LucideAngularModule, CommonModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './playbar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlayerBarComponent {
  readonly Play = Play;
  readonly Pause = Pause;
  readonly SkipBack = SkipBack;
  readonly SkipForward = SkipForward;

  @Input() isPlaying!: boolean;
  @Input() currentTime!: number;
  @Input() duration!: number;
  @Output() playPause = new EventEmitter<void>();
  @Output() seek = new EventEmitter<number>();
  @Output() skip = new EventEmitter<number>();
  
  formatTime(time: number): string {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }
  onSeek(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.seek.emit(parseFloat(value));
  }
}
