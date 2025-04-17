import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { LucideAngularModule, Heart, MoreVertical, SkipBack, SkipForward, Play, Pause, List, Volume2 } from 'lucide-angular';
import { PlayerBarComponent } from "./playbar/playbar.component";
@Component({
  selector: 'player-music',
  standalone: true,
  imports: [LucideAngularModule, CommonModule, PlayerBarComponent],
  templateUrl: './music-player.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerMusicComponent {
  // @ViewChild('audio') audioRef!: ElementRef<HTMLAudioElement>;
  readonly Heart = Heart;
  readonly MoreVertical = MoreVertical;
  readonly SkipBack = SkipBack;
  readonly SkipForward = SkipForward;
  readonly Play = Play;
  readonly Pause = Pause;
  readonly List = List
  readonly Volume2 = Volume2;


  isPlaying = false;
  progress = 0;
  currentTime = 0;
  duration = 0;

  togglePlay() {
    // const audio = this.audioRef.nativeElement;
    // this.isPlaying ? audio.pause() : audio.play();
    this.isPlaying = !this.isPlaying;
  }

  // updateTime() {
  //   const audio = this.audioRef.nativeElement;
  //   this.currentTime = audio.currentTime;
  //   this.progress = (audio.currentTime / audio.duration) * 100;
  // }

  // setDuration() {
  //   this.duration = this.audioRef.nativeElement.duration;
  // }

  // seek(event: any) {
  //   const audio = this.audioRef.nativeElement;
  //   const newTime = (event.target.value / 100) * audio.duration;
  //   audio.currentTime = newTime;
  // }

  nextSong() {
    console.log('Siguiente canción');
  }

  prevSong() {
    console.log('Canción anterior');
  }

}


