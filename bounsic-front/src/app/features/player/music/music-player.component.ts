import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  ElementRef,
  Input,
  OnChanges,
  SimpleChanges,
  signal,
  ViewChild,
} from '@angular/core';
import { Heart, LucideAngularModule, MoreVertical } from 'lucide-angular';
import { PlayerBarComponent } from './playbar/playbar.component';
import { PlayerBarControllersComponent } from './controllers/playbar-controllers.component';
// ... (tus imports)

@Component({
  selector: 'player-music',
  standalone: true,
  imports: [
    LucideAngularModule,
    CommonModule,
    PlayerBarComponent,
    PlayerBarControllersComponent,
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './music-player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlayerMusicComponent implements OnChanges {
  @Input() song: string | null = null;

  readonly Heart = Heart;
  readonly MoreVertical = MoreVertical;

  isPlaying = signal(false);
  isMuted = signal(false);
  volume = signal(1);
  duration = signal(0);
  currentTime = signal(0);

  @ViewChild('audio', { static: true }) audioRef!: ElementRef<HTMLAudioElement>;

  ngAfterViewInit() {
    const audio = this.audioRef.nativeElement;

    audio.addEventListener('play', () => this.isPlaying.set(true));
    audio.addEventListener('pause', () => this.isPlaying.set(false));
    audio.addEventListener('volumechange', () => this.isMuted.set(audio.muted));
    audio.addEventListener('loadedmetadata', () => {
      this.duration.set(audio.duration);
    });
    audio.addEventListener('timeupdate', () => {
      this.currentTime.set(audio.currentTime);
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['song'] && this.song && this.audioRef) {
      const audio = this.audioRef.nativeElement;
      audio.src = this.song;
      audio.load();
      // Opcional: auto play
      // audio.play();
    }
  }

  togglePlayPause() {
    const audio = this.audioRef.nativeElement;
    audio.paused ? audio.play() : audio.pause();
  }

  toggleMute() {
    const audio = this.audioRef.nativeElement;
    audio.muted = !audio.muted;
  }

  onVolumeChange(vol: number) {
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

  onSeek(value: number) {
    this.audioRef.nativeElement.currentTime = value;
  }
}
