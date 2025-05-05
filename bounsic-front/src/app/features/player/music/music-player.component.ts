import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  ElementRef,
  Input,
  OnChanges,
  SimpleChanges,
  ViewChild,
  AfterViewInit,
  signal,
  inject,
} from '@angular/core';
import { Heart, LucideAngularModule, MoreVertical } from 'lucide-angular';
import { PlayerBarComponent } from './playbar/playbar.component';
import { PlayerBarControllersComponent } from './controllers/playbar-controllers.component';
import Song from 'src/types/Song';
import { AudioStreamService } from '@app/services/streaming.service';

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
export class PlayerMusicComponent implements OnChanges, AfterViewInit {
  @Input() song!: Song;

  readonly Heart = Heart;
  readonly MoreVertical = MoreVertical;

  isPlaying = signal(false);
  isMuted = signal(false);
  volume = signal(1);
  duration = signal(0);
  currentTime = signal(0);
  lastVolume = 0; 

  @ViewChild('audio') audioRef?: ElementRef<HTMLAudioElement>;
  private audioStreamService = inject(AudioStreamService);

  
  ngAfterViewInit() {
    if (!this.audioRef) return;
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
    if (changes['song']) {
      setTimeout(() => {
        if (this.audioRef && this.song) {
          const audio = this.audioRef.nativeElement;
          console.log(this.song);
          const regex = /mp3\/(.*)/;
          const match = this.song.mp3_url.match(regex);
          audio.src = this.audioStreamService.getAudioUrl(match ? match[1] : '')
          console.log('Audio source set to:', audio.src);
          audio.load();
        }
      });
    }
  }

  togglePlayPause() {
    const audio = this.audioRef?.nativeElement;
    if (!audio) return;
    audio.paused ? audio.play() : audio.pause();
  }

  toggleMute() {
    const audio = this.audioRef?.nativeElement;
    if (!audio) return;
    this.lastVolume = audio.volume;
    audio.muted = !audio.muted;
    this.volume.set(audio.muted ? 0 : this.lastVolume);
  }
  toggleLike(){
    console.log(this.song.isLiked ? "quit like":"add like")
  }

  onVolumeChange(vol: number) {
    const audio = this.audioRef?.nativeElement;
    if (!audio) return;
    audio.volume = vol;
    this.volume.set(vol);
  }

  formatTime(time: number): string {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }

  skip(seconds: number) {
    const audio = this.audioRef?.nativeElement;
    if (!audio) return;
    audio.currentTime += seconds;
    this.currentTime.set(audio.currentTime);

  }

  onSeek(value: number) {
    const audio = this.audioRef?.nativeElement;
    if (!audio) return;
    audio.currentTime = value;
    this.currentTime.set(value);

  }
}
