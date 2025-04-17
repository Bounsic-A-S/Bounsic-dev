import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  ElementRef,
  signal,
  ViewChild,
} from '@angular/core';
import {
  LucideAngularModule,
  Minus,
  Plus,
  Pause,
  Play,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX,
  List,
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

  readonly SkipBack = SkipBack;
  readonly SkipForward = SkipForward;
  readonly Play = Play;
  readonly Pause = Pause;
  readonly Volume2 = Volume2;
  readonly VolumeX = VolumeX;
  readonly Minus = Minus;
  readonly Plus = Plus;
  readonly List = List;
  isPlaying = signal(false);
  isMuted = signal(false);
  volume = signal(1); // 1.0 = 100%
  duration = signal(0);
  currentTime = signal(0);

  @ViewChild('audio', { static: true }) audioRef!: ElementRef<HTMLAudioElement>;

  ngAfterViewInit() {
    const audio = this.audioRef.nativeElement;

    audio.addEventListener('play', () => this.isPlaying.set(true));
    audio.addEventListener('pause', () => this.isPlaying.set(false));
    audio.addEventListener('volumechange', () => this.isMuted.set(audio.muted));
    // tracker on the song
    audio.addEventListener('loadedmetadata', () => {
      this.duration.set(audio.duration);
    });
  
    // Actualiza tiempo actual cada vez que cambie
    audio.addEventListener('timeupdate', () => {
      this.currentTime.set(audio.currentTime);
    });
  }

  togglePlayPause() {
    const audio = this.audioRef.nativeElement;
    audio.paused ? audio.play() : audio.pause();
  }

  toggleMute() {
    const audio = this.audioRef.nativeElement;
    audio.muted = !audio.muted;
  }
  onVolumeChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const vol = parseFloat(input.value);
    const audio = this.audioRef.nativeElement;
    audio.volume = vol;
    this.volume.set(vol);
  }
  formatTime(time: number): string {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }
  
  skip(seconds: number) {
    const audio = this.audioRef.nativeElement;
    audio.currentTime += seconds;
  }
  onSeek(event: Event) {
    const input = event.target as HTMLInputElement;
    this.audioRef.nativeElement.currentTime = parseFloat(input.value);
  }
  
}
