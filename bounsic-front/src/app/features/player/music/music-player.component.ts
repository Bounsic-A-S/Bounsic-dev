import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  ElementRef,
  signal,
  ViewChild,
} from '@angular/core';
import { LucideAngularModule, Heart, MoreVertical } from 'lucide-angular';
import { PlayerBarComponent } from './playbar/playbar.component';
import { PlayerBarControllersComponent } from './controllers/playbar-controllers.component';
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
export class PlayerMusicComponent {
  readonly Heart = Heart;
  readonly MoreVertical = MoreVertical;
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
